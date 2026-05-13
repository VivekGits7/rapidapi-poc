import asyncio
import time
from typing import Optional

from app.config import settings
from app.logger import get_logger

logger = get_logger(__name__)

_RATE_LIMIT_COOLDOWN = 60  # seconds to wait after a 429


class APIKeyManager:
    """Round-robin rotation across 3 RapidAPI keys.

    Tracks total calls and per-key usage. On 429, locks the key for 60s
    and immediately switches to the next available key.
    """

    def __init__(self) -> None:
        self._keys: list[str] = []
        self._index: int = 0
        self._call_counts: dict[str, int] = {}
        self._locked_until: dict[str, float] = {}

    def setup(self) -> None:
        if self._keys:
            return
        self._keys = settings.rapidapi_keys
        self._call_counts = {k: 0 for k in self._keys}
        self._locked_until = {k: 0.0 for k in self._keys}
        logger.info(f"APIKeyManager: {len(self._keys)} keys loaded")

    def get_next_key(self) -> Optional[str]:
        """Return next available key (round-robin). Returns None if all locked."""
        now = time.time()
        tried = 0
        while tried < len(self._keys):
            key = self._keys[self._index % len(self._keys)]
            self._index += 1
            if self._locked_until.get(key, 0) <= now:
                self._call_counts[key] = self._call_counts.get(key, 0) + 1
                return key
            tried += 1
        return None  # all keys are rate-limited

    async def wait_for_available_key(self) -> str:
        """Block until at least one key is available, then return it."""
        while True:
            key = self.get_next_key()
            if key:
                return key
            # find soonest unlock time
            now = time.time()
            wait = min(self._locked_until.values()) - now
            wait = max(0.1, wait)
            logger.warning(f"All keys rate-limited. Waiting {wait:.1f}s...")
            await asyncio.sleep(wait)

    def mark_rate_limited(self, key: str, cooldown_sec: int = _RATE_LIMIT_COOLDOWN) -> None:
        self._locked_until[key] = time.time() + cooldown_sec
        logger.warning(f"Key ...{key[-8:]} locked for {cooldown_sec}s")

    def total_calls(self) -> int:
        return sum(self._call_counts.values())

    def calls_per_key(self) -> dict[str, int]:
        return {
            f"key_{i + 1}": self._call_counts.get(k, 0)
            for i, k in enumerate(self._keys)
        }

    def remaining_budget(self) -> int:
        return max(0, settings.DUMP_BUDGET - self.total_calls())


api_key_manager = APIKeyManager()
