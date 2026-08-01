"""
test_api.py

Uses FastAPI's TestClient (built on httpx), so these tests run against the
app in-process — no server needs to be started separately.
"""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_transactions_default_pagination():
    response = client.get("/v1/transactions")
    assert response.status_code == 200
    body = response.json()
    assert body["page"] == 1
    assert body["page_size"] == 10
    assert len(body["items"]) <= 10
    assert body["total"] >= len(body["items"])


def test_list_transactions_filter_by_status():
    response = client.get("/v1/transactions", params={"status": "flagged"})
    assert response.status_code == 200
    body = response.json()
    assert all(item["status"] == "flagged" for item in body["items"])


def test_get_transaction_by_id():
    response = client.get("/v1/transactions/TXN-1001")
    assert response.status_code == 200
    assert response.json()["transaction_id"] == "TXN-1001"


def test_get_transaction_not_found_returns_404():
    response = client.get("/v1/transactions/TXN-9999")
    assert response.status_code == 404


def test_customer_summary_aggregates_correctly():
    response = client.get("/v1/customers/CUST-502/summary")
    assert response.status_code == 200
    body = response.json()
    assert body["customer_id"] == "CUST-502"
    assert body["transaction_count"] == 3
    assert body["flagged_count"] == 2
    assert body["high_velocity_count"] == 2


def test_customer_summary_unknown_customer_returns_404():
    response = client.get("/v1/customers/CUST-999/summary")
    assert response.status_code == 404


def test_pagination_page_size_respected():
    response = client.get("/v1/transactions", params={"page_size": 3})
    assert response.status_code == 200
    assert len(response.json()["items"]) == 3
