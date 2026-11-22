# EU-Flex Explorer

**An unofficial, open-source web interface for exploring results of [EU-Flex](https://github.com/EU-ACER/eu-flex-model), ACER's electricity flexibility needs assessment model.**

> ⚠️ **Unofficial project.** EU-Flex Explorer is a community project. It is not developed, endorsed or maintained by ACER or Open Energy Transition. See [DISCLAIMER.md](DISCLAIMER.md).

<!-- TODO: screenshot / GIF of the explorer -->
<!-- ![EU-Flex Explorer screenshot](docs/img/screenshot.png) -->

**Live demo:** _coming soon_ <!-- TODO: link -->

---

## Why

EU-Flex is a powerful open model, but exploring its results today requires a conda environment, Snakemake and Python/NetCDF skills. EU-Flex Explorer makes the outputs accessible in the browser — no installation — for regulators, TSOs/DSOs, associations, analysts and anyone following the EU-wide flexibility needs assessment.

## Features

**Phase 1 — Results explorer (MVP)**
- Map of flexibility needs (daily / weekly / seasonal) by bidding zone
- Technology and cross-border contributions to flexibility
- Residual load, ramping and short-term needs time series
- Side-by-side scenario comparison (e.g. with vs. without cross-border sharing)
- Runs fully in the browser on pre-computed teaser results (DuckDB-WASM)

**Phase 2 — Scenario runs** _(planned)_
- Edit a limited set of parameters and run the flexibility-indicator workflow on a server

**Phase 3 — Sharing** _(planned)_
- Shareable scenario links, run diffs, chart export

## Architecture

```
web/  ──►  api/  ──►  queue  ──►  worker/ (adapter → EU-Flex Snakemake → model_outputs.nc)
 ▲                                     │
 └──────────── Parquet + DuckDB ◄── etl/ (NetCDF DataTree → tidy Parquet)
```

All knowledge of EU-Flex internals lives in `adapter/` so that model updates touch one module only. Details: [docs/architecture.md](docs/architecture.md).

## Repository layout

| Path | Purpose |
|---|---|
| `adapter/` | Python package: config overlay, Snakemake invocation, NetCDF → Parquet export |
| `etl/` | Scripts to convert run outputs into the explorer's data format |
| `api/` | FastAPI service (Phase 2) |
| `worker/` | Docker image running EU-Flex from its official conda lock file (Phase 2) |
| `web/` | Frontend (MapLibre, ECharts, DuckDB-WASM) |
| `data/` | Pre-computed teaser results (Parquet) — see `data/README.md` |
| `docs/` | Architecture, data schema, decisions |

## Quick start

### Explore pre-computed results (frontend only)

```bash
cd web
npm install
npm run dev
```

### Export your own EU-Flex run

Requires a working [EU-Flex](https://github.com/EU-ACER/eu-flex-model) run.

```bash
pip install -e ./adapter
euflex-export runs/teaser/results/assessment/model_outputs.nc --out data/teaser
```

## Compatibility

| EU-Flex Explorer | EU-Flex model commit | Notes |
|---|---|---|
| 0.1.x | `TODO` | Pre-release (public consultation, Nov–Dec 2026) |

EU-Flex is in pre-release; output variable names may change. Each exported run records the model commit it was produced with.

## Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). Feedback on the **model itself** belongs in the [EU-Flex repository](https://github.com/EU-ACER/eu-flex-model/issues), not here.

## Accessibility

The explorer targets public-sector users. Every chart has a text description and a table alternative, all controls work with the keyboard, and colours meet WCAG 2.1 AA contrast. Accessibility issues are treated as bugs.

## License and attribution

- Code: [MIT](LICENSE)
- EU-Flex model code (MIT), documentation and teaser model (CC-BY-4.0) and input data (CC0-1.0) © ACER / Open Energy Transition. Results derived from the teaser case are redistributed under CC-BY-4.0 with attribution. See [NOTICE.md](NOTICE.md).

The teaser dataset is **illustrative only**; results must not be read as market forecasts or conclusions about actual flexibility needs.

## Author

<!-- TODO: your name, LinkedIn -->
