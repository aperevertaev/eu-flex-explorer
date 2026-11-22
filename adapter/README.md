# euflex-explorer-adapter

The only part of EU-Flex Explorer that knows about EU-Flex internals.

- `export.py`: converts `model_outputs.nc` (xarray DataTree) into tidy Parquet + `manifest.json`
- `runner.py` _(Phase 2)_: builds config overlays and invokes the EU-Flex Snakemake workflow

```bash
pip install -e ".[dev]"
euflex-export path/to/model_outputs.nc --out ../data/teaser --run-id teaser \
    --euflex-commit $(git -C path/to/eu-flex-model rev-parse --short HEAD) \
    --config-file config/teaser.yaml
```

Options:
- `--groups base` exports only selected groups
- `--include 'daily_*' --include '*_aggregated'` exports only matching variables (glob)

`export.py` is a candidate for upstream contribution to EU-Flex. It has no dependency on the explorer.
