"""
main.py

A small FastAPI service exposing curated payments pipeline output.

Design choices worth being able to explain in an interview:
- `/v1/...` prefix: versioning from day one, so a breaking change later
  doesn't have to break existing consumers.
- Pagination on the list endpoint: returning all rows unpaginated is fine
  for 10 sample rows, but it's the kind of thing that quietly becomes a
  production incident at scale, so I built it in even though it isn't
  strictly needed here.
- 404 (not the default 200-with-null) when a resource genuinely doesn't
  exist — this is a small thing that a lot of hand-rolled APIs get wrong.
"""

from fastapi import FastAPI, HTTPException, Query

from app.data import load_transactions
from app.models import CustomerSummary, Transaction, TransactionList

app = FastAPI(
    title="Payments Pipeline API",
    description=(
        "Serves curated output from the Payments Event Data Platform. "
        "Practice project — see README.md for scope and limitations."
    ),
    version="1.0.0",
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/v1/transactions", response_model=TransactionList)
def list_transactions(
    status: str | None = Query(default=None, description="Filter by status"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
) -> TransactionList:
    transactions = load_transactions()

    if status is not None:
        transactions = [t for t in transactions if t["status"] == status]

    start = (page - 1) * page_size
    end = start + page_size
    page_items = transactions[start:end]

    return TransactionList(
        total=len(transactions),
        page=page,
        page_size=page_size,
        items=[Transaction(**t) for t in page_items],
    )


@app.get("/v1/transactions/{transaction_id}", response_model=Transaction)
def get_transaction(transaction_id: str) -> Transaction:
    transactions = load_transactions()
    for t in transactions:
        if t["transaction_id"] == transaction_id:
            return Transaction(**t)
    raise HTTPException(status_code=404, detail=f"Transaction {transaction_id} not found")


@app.get("/v1/customers/{customer_id}/summary", response_model=CustomerSummary)
def customer_summary(customer_id: str) -> CustomerSummary:
    transactions = [t for t in load_transactions() if t["customer_id"] == customer_id]
    if not transactions:
        raise HTTPException(status_code=404, detail=f"No transactions for customer {customer_id}")

    return CustomerSummary(
        customer_id=customer_id,
        transaction_count=len(transactions),
        total_amount=round(sum(t["amount"] for t in transactions), 2),
        flagged_count=sum(1 for t in transactions if t["status"] == "flagged"),
        high_velocity_count=sum(1 for t in transactions if t["velocity_flag"] == "high"),
    )
