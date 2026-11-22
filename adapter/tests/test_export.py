import json

import numpy as np
import pandas as pd
import xarray as xr

from euflex_adapter.export import export_datatree


def _fake_tree() -> xr.DataTree:
    """Minimal DataTree mimicking the EU-Flex output layout (spec 3.5.2.4)."""
    base = xr.Dataset(
        {
            "daily_flexibility_need": (
                ("TY", "CY", "BZ", "day"),
                np.arange(2 * 1 * 2 * 3, dtype=float).reshape(2, 1, 2, 3),
                {"kind": "flexibility_indicator", "units": "MWh"},
            ),
            "seasonal_flexibility_need": (
                ("TY", "CY", "BZ"),
                np.array([[[1.0, np.nan]], [[3.0, 4.0]]]),
                {"kind": "flexibility_indicator", "units": "MWh"},
            ),
        },
        coords={"TY": [2030, 2035], "CY": [2009], "BZ": ["DE00", "FR00"], "day": [0, 1, 2]},
    )
    ds = xr.Dataset(
        {"curtailment_reduction": (("BZ",), [5.0, 6.0], {"kind": "flexibility_indicator"})},
        coords={"BZ": ["DE00", "FR00"]},
    )
    return xr.DataTree.from_dict({"/base": base, "/dummy_storage_optimization": ds})


def test_export_writes_tidy_parquet_and_manifest(tmp_path):
    m = export_datatree(_fake_tree(), tmp_path, run_id="test", euflex_commit="abc1234")

    names = {(v.group, v.name) for v in m.variables}
    assert ("base", "daily_flexibility_need") in names
    assert ("dummy_storage_optimization", "curtailment_reduction") in names

    df = pd.read_parquet(tmp_path / "base" / "daily_flexibility_need.parquet")
    assert list(df.columns) == ["TY", "CY", "BZ", "day", "value"]
    assert len(df) == 12

    # NaN rows dropped by default
    df2 = pd.read_parquet(tmp_path / "base" / "seasonal_flexibility_need.parquet")
    assert len(df2) == 3

    manifest = json.loads((tmp_path / "manifest.json").read_text())
    assert manifest["euflex_commit"] == "abc1234"
    entry = next(v for v in manifest["variables"] if v["name"] == "daily_flexibility_need")
    assert entry["units"] == "MWh" and entry["kind"] == "flexibility_indicator"


def test_filters(tmp_path):
    m = export_datatree(_fake_tree(), tmp_path, run_id="t", groups=["base"], include=["daily_*"])
    assert [v.name for v in m.variables] == ["daily_flexibility_need"]
