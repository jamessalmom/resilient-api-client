from unittest.mock import MagicMock

from resilient_api_client.client import ApiClient


def test_get_returns_response_on_success():
    session = MagicMock()
    session.get.return_value.raise_for_status.return_value = None
    session.get.return_value.status_code = 200

    client = ApiClient(base_url="https://example.com", session=session)
    response = client.get("/status")

    session.get.assert_called_once()
    assert response.status_code == 200
