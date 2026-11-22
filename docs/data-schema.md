# Data schema (draft)

Based on Section 3.5.2.4 of the EU-Flex Public Modelling Specification v1.0 (26/10/2026). **Verify against a real `model_outputs.nc` before relying on it.**

## Export layout

```
data/<run_id>/
├── manifest.json                 # provenance + variable catalogue
├── base/
│   ├── daily_flexibility_need.parquet
│   ├── residual_load.parquet
│   └── ...
└── dummy_storage_optimization/
    └── ...
```

Each Parquet file is in **long (tidy) format**: one column per dimension plus a `value` column.

Example `base/daily_flexibility_need.parquet`:

| TY | CY | BZ | day | value |
|---|---|---|---|---|
| 2030 | 2009 | DE00 | 0 | 1234.5 |

## manifest.json

```json
{
  "run_id": "teaser",
  "exported_at": "2026-11-20T10:00:00Z",
  "euflex_commit": "abc1234",
  "config_file": "config/teaser.yaml",
  "exporter_version": "0.1.0",
  "variables": [
    {
      "group": "base",
      "name": "daily_flexibility_need",
      "kind": "flexibility_indicator",
      "dims": ["TY", "CY", "BZ", "day"],
      "units": "MWh",
      "path": "base/daily_flexibility_need.parquet",
      "rows": 36500
    }
  ]
}
```

## Common dimensions (from the spec)

| Dimension | Meaning |
|---|---|
| `TY` | Target year |
| `CY` | Climate year |
| `BZ` / `bidding_zone` | Bidding zone |
| `carrier` | Technology / carrier |
| `hour` | Hour of year (0–8759) |
| `day`, `week` | Day / week index |
| `iteration` | EVA iteration |
| `generator`, `asset` | Asset names |

## Variable kinds

- `flexibility_indicator`: curtailment, residual load, daily/weekly/seasonal needs, ramping, short-term needs, technology and cross-border contributions
- `market_output`: prices, supply/withdrawal, generation, reserves, demand, energy not served
- `eva_output`: capacities, commissioned/decommissioned capacity, NPV per MW

## Size strategy

Hourly variables with `carrier` and `BZ` dimensions (e.g. `curtailment`, `supply`) can be large. For the browser:
- ship `*_aggregated` variables and daily/weekly series by default;
- load hourly series lazily, per bidding zone, via DuckDB-WASM HTTP range requests.
