"""
data.py

Loads the sample transaction data. In a real deployment this would read
from the actual output of the Payments Event Data Platform (a table or a
curated file) instead of a static JSON file — the API layer wouldn't
change, only this module would.
"""

import json
import pathlib
from functools import lru_cache

DATA_PATH = pathlib.Path(__file__).resolve().parent.parent / "data" / "sample_transactions.json"


@lru_cache
def load_transactions() -> list[dict]:
    with open(DATA_PATH) as f:
        return json.load(f)
