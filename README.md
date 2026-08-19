# resilient-api-client

A small `requests` wrapper adding a **circuit breaker** and structured
logging for integrating with partner/ERP REST APIs that occasionally go
down or slow to a crawl. Stops retrying (and stops flooding) a dead
endpoint instead of piling up timeouts.

## Why a circuit breaker instead of just retries

Retries alone are fine for a single blip; they make things worse when the
downstream service is actually down, since every caller keeps hammering
it. The breaker trips open after N consecutive failures, rejects calls
immediately for a cooldown window, then allows a single probe call
(half-open) before fully closing again.

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

MIT — see [LICENSE](LICENSE).
