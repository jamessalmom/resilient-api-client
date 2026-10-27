# resilient-api-client

A thin wrapper around `requests` that adds a circuit breaker and structured logging, for partner or ERP REST APIs that sometimes go down or become very slow. When an endpoint is dead, the client stops calling it for a while instead of piling up timeouts.

## Why a circuit breaker and not only retries

Retries handle a single failure well. When the service is actually down, they make it worse, because every caller keeps hitting it. The breaker opens after N consecutive failures and rejects calls right away during a cooldown. After that it lets one test call through (half-open) and closes again if it succeeds.

## Usage

```python
from resilient_api_client import ApiClient, CircuitBreaker, CircuitOpenError

client = ApiClient(
    base_url="https://partner.example.com",
    breaker=CircuitBreaker(failure_threshold=5, recovery_timeout_seconds=30),
)

try:
    response = client.get("/orders/123")
except CircuitOpenError:
    # fail fast instead of waiting on a dead service
    ...
```

## Development

```bash
pip install -r requirements.txt
pip install pytest ruff
pytest
ruff check .
```

## License

MIT, see [LICENSE](LICENSE).
