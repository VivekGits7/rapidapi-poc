"""HTTPX wrapper that rotates RapidAPI keys, persists cooldowns, retries transient errors.

All dumper phase code calls api_get() / api_post() — nothing else.
"""

import asyncio
from typing import Any, Optional

import httpx

from config import settings
from dumper.key_manager import api_key_manager
from logger import get_logger

logger = get_logger("dumper.http")


async def _make_request(
    method: str,
    path: str,
    params: Optional[dict] = None,
    json_body: Optional[dict] = None,
) -> Optional[Any]:
    """One HTTP call with key rotation + retry on transient errors.

    Returns parsed JSON (dict or list) on success, None if every retry failed.
    On `AllKeysExhaustedError` (from key_manager) propagates up — caller should treat as fatal.
    """
    transient_retries = 0

    while transient_retries <= settings.MAX_TRANSIENT_RETRIES:
        # Throttle: 100ms (settings.DUMP_DELAY_MS) between calls. Per-key, but we serialize via lock in key_manager.
        await asyncio.sleep(settings.DUMP_DELAY_MS / 1000)

        key_id, key_value = await api_key_manager.get_next_key()
        url = f"{settings.RAPIDAPI_BASE_URL}{path}"
        headers = {
            "x-rapidapi-key": key_value,
            "x-rapidapi-host": settings.RAPIDAPI_HOST,
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=settings.RAPIDAPI_TIMEOUT) as client:
                resp = await client.request(method, url, headers=headers, params=params, json=json_body)

            # 200 — success
            if resp.status_code == 200:
                await api_key_manager.mark_success(key_id)
                try:
                    return resp.json()
                except Exception as e:
                    logger.error(f"Failed to parse JSON from {path}: {e}")
                    return None

            # 429 / 403 — rate-limited / quota exhausted. Cooldown the key and try a different one.
            if resp.status_code in (429, 403):
                body = resp.text[:300]
                logger.warning(f"HTTP {resp.status_code} on {path} | key {key_id} | body: {body}")
                await api_key_manager.mark_rate_limited(key_id, resp.status_code)
                # Don't increment transient_retries — these aren't transient, just per-key.
                continue

            # 5xx — transient server error. Cooldown briefly, retry.
            if 500 <= resp.status_code < 600:
                logger.warning(
                    f"HTTP {resp.status_code} on {path} | key {key_id} | retry {transient_retries+1}/{settings.MAX_TRANSIENT_RETRIES}"
                )
                await api_key_manager.mark_rate_limited(key_id, resp.status_code)
                transient_retries += 1
                continue

            # 4xx other than 403/429 — request shape problem. Don't retry.
            logger.error(f"HTTP {resp.status_code} on {path} | body: {resp.text[:300]}")
            return None

        except (httpx.TimeoutException, httpx.NetworkError) as e:
            logger.warning(
                f"Network error on {path} (key {key_id}): {e} — retry {transient_retries+1}/{settings.MAX_TRANSIENT_RETRIES}"
            )
            transient_retries += 1
            continue
        except Exception as e:
            logger.error(f"Unexpected error on {path}: {e}", exc_info=True)
            return None

    logger.error(f"Exhausted {settings.MAX_TRANSIENT_RETRIES} retries on {path}")
    return None


async def api_get(path: str, params: Optional[dict] = None) -> Optional[Any]:
    return await _make_request("GET", path, params=params)


async def api_post(path: str, json_body: Optional[dict] = None) -> Optional[Any]:
    return await _make_request("POST", path, json_body=json_body)
