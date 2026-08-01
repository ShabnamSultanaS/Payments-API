# Payments Pipeline API (Practice Project)

**Status: learning-in-progress.** A small REST API built with FastAPI that
serves curated output from my
[Payments Event Data Platform](https://github.com/ShabnamSultanaS), so I
could practise API design instead of only ever handing pipeline output
over as a file. This is a self-directed study project, not a production
service.

## Why this project exists

Every project I've built ends with data landing in a table or a file.
Several roles I'm applying for name API development as a requirement — this
is where I learned what it actually takes to expose data as a service
instead: resource naming, status codes, response models, and versioning,
not just "write a function that returns JSON."

## What's here

```
payments-api/
├── app/
│   ├── main.py       # route definitions
│   ├── models.py     # Pydantic response models
│   └── data.py       # loads sample curated output (simulates reading from the real pipeline)
├── data/
│   └── sample_transactions.json
├── tests/
│   └── test_api.py
├── STUDY_NOTES.md
├── requirements.txt
└── README.md
```

## Running it

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000/docs` — FastAPI generates interactive
API documentation automatically, which is itself one of the reasons I
picked it to learn with.

## Running the tests

```bash
pytest tests/ -v
```

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Basic liveness check |
| GET | `/v1/transactions` | List transactions, paginated, with optional status filter |
| GET | `/v1/transactions/{transaction_id}` | A single transaction by ID |
| GET | `/v1/customers/{customer_id}/summary` | Aggregated spend summary for a customer — reads from the SCD Type 2 customer dimension idea in the underlying pipeline |

## What I'm getting out of this

See `STUDY_NOTES.md` for specifics, but the headline: designing the
`/v1/customers/{id}/summary` endpoint is what made me actually think about
API design rather than just plumbing. It could have just returned the raw
customer dimension row — instead it aggregates the same fraud-signal
features (velocity windows, totals) my pipeline already computes, so the
API is a genuinely useful consumer of that work, not a demo wrapper around
it.

