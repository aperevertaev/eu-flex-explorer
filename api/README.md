# api/ (Phase 2)

FastAPI service. Planned endpoints:

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/runs` | List available runs (from Postgres metadata) |
| `GET` | `/runs/{run_id}/manifest` | Run manifest |
| `GET` | `/runs/{run_id}/query` | Aggregated query via DuckDB over Parquet |
| `POST` | `/scenarios` | Validate a scenario overlay (Pydantic), enqueue a run |
| `GET` | `/jobs/{job_id}` | Job status (polling or SSE) |

Only the flexibility-indicator workflow can be launched publicly, with per-user quotas.
