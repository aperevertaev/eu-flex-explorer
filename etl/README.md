# etl/

Scripts that turn EU-Flex runs into explorer-ready data.

Phase 1 workflow (run locally, results committed to `data/`):

```bash
# in the eu-flex-model repo, with the eu-flex conda env active
for cfg in teaser teaser-ds-cross-border teaser-ds-no-cross-border teaser-eva; do
  snakemake -c 2 --configfile config/$cfg.yaml --directory runs/$cfg
done

# in this repo
for cfg in teaser teaser-ds-cross-border teaser-ds-no-cross-border teaser-eva; do
  euflex-export ../eu-flex-model/runs/$cfg/results/assessment/model_outputs.nc \
    --out data/$cfg --run-id $cfg --config-file config/$cfg.yaml \
    --euflex-commit $(git -C ../eu-flex-model rev-parse --short HEAD)
done
```

Note: `teaser-eva` takes several hours. The `teaser-ds-*` runs produce about 9 GB, so export only the variables the explorer needs (`--include`).

TODO: `build_web_data.py`, which precomputes browser-friendly aggregates (per BZ, per season) from the exported Parquet.
