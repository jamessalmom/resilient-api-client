import time

import pytest

from resilient_api_client.circuit_breaker import (
    CircuitBreaker,
    CircuitOpenError,
    CircuitState,
)


def test_stays_closed_while_calls_succeed():
    cb = CircuitBreaker(failure_threshold=3)
    for _ in range(5):
        assert cb.call(lambda: "ok") == "ok"
    assert cb.state == CircuitState.CLOSED


def test_opens_after_threshold_failures():
    cb = CircuitBreaker(failure_threshold=2)

    def fail():
        raise RuntimeError("down")

    for _ in range(2):
        with pytest.raises(RuntimeError):
            cb.call(fail)

    assert cb.state == CircuitState.OPEN
    with pytest.raises(CircuitOpenError):
        cb.call(lambda: "should not run")


def test_half_opens_after_recovery_timeout():
    cb = CircuitBreaker(failure_threshold=1, recovery_timeout_seconds=0.05)
    with pytest.raises(RuntimeError):
        cb.call(lambda: (_ for _ in ()).throw(RuntimeError("down")))
    assert cb.state == CircuitState.OPEN

    time.sleep(0.06)
    assert cb.state == CircuitState.HALF_OPEN

    # a success while half-open closes the circuit again
    assert cb.call(lambda: "recovered") == "recovered"
    assert cb.state == CircuitState.CLOSED
