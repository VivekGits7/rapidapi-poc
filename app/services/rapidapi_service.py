from typing import Any, Optional

import httpx

from app.config import settings
from app.error import ExternalServiceException
from app.logger import get_logger
from app.services.api_key_manager import api_key_manager

logger = get_logger(__name__)

_QUOTA_COOLDOWN_SEC = 3600


class RapidAPIService:
    """Shared async HTTP client for RapidAPI (Auto Parts Catalog).

    Rotates across all configured RapidAPI keys via APIKeyManager. On 403
    (quota exhausted) or 429 (rate limit) the current key is locked and the
    request is retried with the next available key. Gives up cleanly once
    every key has been tried for the same request.
    """

    def __init__(self) -> None:
        self._client: Optional[httpx.AsyncClient] = None

    def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=settings.RAPIDAPI_BASE_URL,
                headers={"x-rapidapi-host": settings.RAPIDAPI_HOST},
                timeout=settings.RAPIDAPI_TIMEOUT,
            )
        return self._client

    async def close(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def _request(
        self,
        method: str,
        path: str,
        params: Optional[dict] = None,
        json_body: Optional[dict] = None,
        tried_keys: Optional[set[str]] = None,
    ) -> Any:
        if tried_keys is None:
            tried_keys = set()

        api_key_manager.setup()
        key = api_key_manager.get_next_key()
        if not key:
            logger.error(f"All RapidAPI keys rate-limited or exhausted for {path}")
            raise ExternalServiceException(
                f"All RapidAPI keys rate-limited or exhausted for {path}"
            )
        tried_keys.add(key)

        try:
            response = await self._get_client().request(
                method,
                path,
                params=params,
                json=json_body,
                headers={"x-rapidapi-key": key},
            )

            if response.status_code in (429, 403):
                body = response.text[:200]
                logger.warning(
                    f"RapidAPI {method} {path} HTTP {response.status_code} | key=...{key[-8:]} | body={body}"
                )
                cooldown = _QUOTA_COOLDOWN_SEC if response.status_code == 403 else 60
                api_key_manager.mark_rate_limited(key, cooldown_sec=cooldown)

                total_keys = len(settings.rapidapi_keys)
                if len(tried_keys) >= total_keys:
                    logger.error(
                        f"All {total_keys} RapidAPI keys exhausted for {path}"
                    )
                    raise ExternalServiceException(
                        f"RapidAPI returned {response.status_code} for {path} (all keys exhausted)"
                    )
                return await self._request(method, path, params, json_body, tried_keys)

            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            body = e.response.text[:200] if e.response is not None else ""
            logger.error(f"RapidAPI {method} {path} failed: {e.response.status_code} {body}")
            raise ExternalServiceException(
                f"RapidAPI returned {e.response.status_code} for {path}"
            )
        except httpx.HTTPError as e:
            logger.error(f"RapidAPI {method} {path} network error: {str(e)}")
            raise ExternalServiceException("RapidAPI request failed")

    async def get(self, path: str, params: Optional[dict] = None) -> Any:
        return await self._request("GET", path, params=params)

    async def post(self, path: str, json: Optional[dict] = None) -> Any:
        return await self._request("POST", path, json_body=json)


rapidapi_service = RapidAPIService()
