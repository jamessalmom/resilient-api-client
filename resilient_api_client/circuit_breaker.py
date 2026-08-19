"""A minimal circuit breaker: stop hammering a partner API once it is
clearly down, and give it time to recover before trying again.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import TypeVar

T = TypeVar("T")


class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitOpenError(RuntimeError):
    """Raised when a call is rejected because the circuit is open."""


@dataclass
class CircuitBreaker:
    failure_threshold: int = 5
    recovery_timeout_seconds: float = 30.0
    _state: CircuitState = field(default=CircuitState.CLOSED, init=False)
    _failure_count: int = field(default=0, init=False)
    _opened_at: float = field(default=0.0, init=False)

    @property
    def state(self) -> CircuitState:
        if self._state == CircuitState.OPEN and self._recovery_elapsed():
            self._state = CircuitState.HALF_OPEN
        return self._state

    def _recovery_elapsed(self) -> bool:
        return (time.monotonic() - self._opened_at) >= self.recovery_timeout_seconds

    def call(self, func: Callable[[], T]) -> T:
        if self.state == CircuitState.OPEN:
            raise CircuitOpenError("circuit is open; refusing call")

        try:
            result = func()
        except Exception:
            self._record_failure()
            raise
        else:
            self._record_success()
            return result

    def _record_failure(self) -> None:
        self._failure_count += 1
        if self._state == CircuitState.HALF_OPEN or self._failure_count >= self.failure_threshold:
            self._state = CircuitState.OPEN
            self._opened_at = time.monotonic()

    def _record_success(self) -> None:
        self._failure_count = 0
        self._state = CircuitState.CLOSED
