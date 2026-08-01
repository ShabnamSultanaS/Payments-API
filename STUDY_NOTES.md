# Study Notes — REST API Design

| Concept | What it is | Where it shows up in this project |
|---|---|---|
| Resource naming | URLs should name things (nouns), not actions (verbs) | `/v1/transactions/{id}`, not `/getTransaction?id=` |
| Versioning | Prefixing routes with a version so future breaking changes don't break existing consumers | `/v1/...` on every route |
| Status codes | Using the right HTTP status to mean the right thing | 404 on a genuinely missing resource, not 200 with an empty body |
| Response models | A schema-validated, documented response shape, not "whatever dict I return" | `Transaction`, `TransactionList`, `CustomerSummary` in `models.py` |
| Pagination | Limiting response size and giving the client a way to page through more | `page` / `page_size` params on `/v1/transactions` |
| Auto-generated docs | FastAPI builds interactive docs from the route signatures and Pydantic models | Visit `/docs` when running locally |

## Questions I should be able to answer after finishing this project

- Why does `/v1/customers/{id}/summary` do aggregation server-side instead of just returning the raw transactions and letting the client sum them?
- What would need to change to support a `date_from` / `date_to` filter on `/v1/transactions`?
- If this needed authentication, where would that fit into FastAPI's request lifecycle?
- What's the actual difference between `response_model` validation and just returning a dict?

## Honest self-assessment

This is a well-designed toy API, not evidence of building APIs at scale —
no auth, no rate limiting, no real database behind it, no deployment. The
value of this project is that I can talk through real design decisions
(versioning, pagination, status codes, response modelling) with a working
example, rather than reciting REST principles abstractly.
