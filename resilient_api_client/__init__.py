"""resilient_api_client

A small, dependency-light HTTP client with a circuit breaker and
structured logging on top of `requests` — for integrating with flaky
partner/ERP APIs without writing the same retry/backoff/circuit-breaker
boilerplate on every project.

Companion to (but independent from) `pix-webhook-toolkit`, generalized
for any REST integration rather than payment-specific flows.
"""

from .circuit_breaker import CircuitBreaker, CircuitOpenError
from .client import ApiClient

__all__ = ["ApiClient", "CircuitBreaker", "CircuitOpenError"]
__version__ = "0.1.0"
