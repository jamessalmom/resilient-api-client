"""ApiClient: requests + circuit breaker + structured logging."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

import requests

from .circuit_breaker import CircuitBreaker

logger = logging.getLogger("resilient_api_client")


class ApiClient:
    def __init__(
        self,
        base_url: str,
        timeout_seconds: float = 10.0,
        breaker: CircuitBreaker | None = None,
        session: requests.Session | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.breaker = breaker or CircuitBreaker()
        self.session = session or requests.Session()

    def get(self, path: str, params: Mapping[str, Any] | None = None) -> requests.Response:
        def _do_call() -> requests.Response:
            url = f"{self.base_url}{path}"
            logger.info("api_get", extra={"url": url})
            response = self.session.get(url, params=params, timeout=self.timeout_seconds)
            response.raise_for_status()
            return response

        return self.breaker.call(_do_call)
