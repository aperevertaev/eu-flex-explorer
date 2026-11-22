# Architecture

## Overview

```
┌────────────┐   HTTP    ┌──────────┐  enqueue  ┌─────────────┐
│  web/      │ ────────► │  api/    │ ────────► │ Redis + Arq │
│ MapLibre   │           │ FastAPI  │           └──────┬──────┘
│ ECharts    │ ◄──────── │ Pydantic │                  │
│ DuckDB-WASM│  Parquet  └────┬─────┘                  ▼
└────────────┘                │ read          ┌─────────────────────┐
                              ▼               │ worker/             │
                   ┌─────────────────────┐    │ adapter → snakemake │
                   │ storage             │ ◄──│ → model_outputs.nc  │
                   │ Parquet + DuckDB    │ etl│ → Parquet           │
                   │ Postgres (metadata) │    └─────────────────────┘
                   └─────────────────────┘
```

**Phase 1 (MVP)** ships only `web/` + pre-computed Parquet in `data/`, as a static site with no server.

## Key decisions

### 1. Adapter isolates EU-Flex
EU-Flex is pre-release and will change after the consultation. All model-specific knowledge (config keys, Snakemake targets, NetCDF group and variable names) lives in `adapter/`. Everything downstream consumes a stable tidy schema (`docs/data-schema.md`).

### 2. Runs = Snakemake invocations
EU-Flex runs as a Snakemake workflow driven by YAML configs. A scenario is a small overlay on a base config (e.g. `config/teaser.yaml`):

```
scenario (UI) → overlay YAML → hash → snakemake --configfile <hash>.yaml --directory runs/<hash>
```

The run directory keyed by config hash doubles as a cache.

### 3. Only light runs are public
| Workflow | Approx. runtime | Public? |
|---|---|---|
| Flexibility indicators (`teaser.yaml`) | ~10 min | Yes, with quotas |
| Economic viability assessment (`teaser-eva.yaml`) | hours | No, pre-computed |
| Dummy storage sizing (`teaser-ds-*.yaml`) | ~1 h, ~9 GB output | No, pre-computed |

Each optimisation can use up to 2 GB RAM → limit worker concurrency accordingly.

### 4. Storage
- `model_outputs.nc` (xarray DataTree: `/base`, `/dummy_storage_optimization`) → tidy Parquet, one file per variable.
- DuckDB (server) / DuckDB-WASM (browser) for aggregation queries.
- Postgres only for metadata: scenarios, run status, provenance.

### 5. Worker image
Built from EU-Flex's official `envs/linux-64.lock.yaml` with micromamba, pinned to a specific EU-Flex commit.

## Decision log

Record significant decisions in `docs/decisions/NNNN-title.md` (ADR format).
