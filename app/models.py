"""
models.py

Pydantic models define both the response shape and the auto-generated
API documentation. Keeping these separate from the raw data dicts in
data.py is deliberate: it means the API's public contract is explicit
and versioned, not just "whatever the JSON file happens to contain."
"""

from typing import Literal

from pydantic import BaseModel, Field


class Transaction(BaseModel):
    transaction_id: str
    customer_id: str
    amount: float = Field(..., ge=0)
    currency: str
    status: Literal["settled", "pending", "flagged"]
    timestamp: str
    velocity_flag: Literal["normal", "high"]


class TransactionList(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[Transaction]


class CustomerSummary(BaseModel):
    customer_id: str
    transaction_count: int
    total_amount: float
    flagged_count: int
    high_velocity_count: int
