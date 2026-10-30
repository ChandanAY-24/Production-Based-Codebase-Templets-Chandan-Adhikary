"""
In-Memory Rate Limiter using Sliding Window Counter.
Reference: Spec/001-Spec-Security-guide.md (API-02, AUTH-06)
Protects API endpoints against brute force, denial of service, and resource exhaustion.
"""

import time
from collections import defaultdict
from typing import Tuple

class SlidingWindowRateLimiter:
    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        # Maps client_id -> list of timestamps
        self._requests = defaultdict(list)

    def is_allowed(self, client_id: str) -> Tuple[bool, int]:
        """
        Check if request from client_id is permitted under rate limit.
        Returns: (is_allowed: bool, retry_after_seconds: int)
        """
        now = time.time()
        window_start = now - self.window_seconds
        timestamps = self._requests[client_id]

        # Prune timestamps outside current window
        self._requests[client_id] = [t for t in timestamps if t > window_start]

        if len(self._requests[client_id]) >= self.max_requests:
            # Exceeded limit; calculate wait time
            oldest_in_window = self._requests[client_id][0]
            retry_after = max(1, int(oldest_in_window + self.window_seconds - now))
            return False, retry_after

        # Record this request
        self._requests[client_id].append(now)
        return True, 0

    def reset(self):
        """Reset all rate limiter state (useful for tests)."""
        self._requests.clear()
