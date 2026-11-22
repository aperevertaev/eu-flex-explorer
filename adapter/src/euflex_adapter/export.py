"""Export EU-Flex ``model_outputs.nc`` (xarray DataTree) into tidy Parquet files.

Each data variable becomes one Parquet file in long format (one column per
dimension + ``value``). A ``manifest.json`` records provenance and a catalogue
of exported variables.

Layout follows Section 3.5.2.4 of the EU-Flex Public Modelling Specification:
groups ``/base`` and ``/dummy_storage_optimization``.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import xarray as xr

from . import __version__


@dataclass
class VariableEntry:
    group: str
    name: str
    kind: str | None
    dims: list[str]
    units: str | None
    path: str
    rows: int


@dataclass
class Manifest:
    run_id: str
    exported_at: str
    exporter_version: str
    euflex_commit: str | None = None
    config_file: str | None = None
    source_file: str | None = None
    variables: list[VariableEntry] = field(default_factory=list)


def _group_name(path: str) -> str:
    """'/base' -> 'base', '/' -> 'root'."""
    name = path.strip("/")
    return name.replace("/", "__") or "root"


def _matches(name: str, patterns: list[str] | None) -> bool:
    return not patterns or any(fnmatch.fnmatch(name, p) for p in patterns)


def variable_to_frame(da: xr.DataArray):
    """Convert a DataArray to a tidy DataFrame with a ``value`` column."""
    name = "value"
    if da.ndim == 0:
        import pandas as pd

        return pd.DataFrame({name: [da.item()]})
    df = da.rename(name).to_dataframe().reset_index()
    # Drop non-dimension coordinates that xarray may carry along.
    keep = list(da.dims) + [name]
    return df[[c for c in df.columns if c in keep]]


def export_datatree(
    tree: xr.DataTree,
    out_dir: Path,
    run_id: str,
    groups: list[str] | None = None,
    include: list[str] | None = None,
    dropna: bool = True,
    **provenance,
) -> Manifest:
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = Manifest(
        run_id=run_id,
        exported_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        exporter_version=__version__,
        **provenance,
    )

    for node in tree.subtree:
        group = _group_name(node.path)
        if groups and group not in groups:
            continue
        ds = node.to_dataset(inherit=False)
        for var_name, da in ds.data_vars.items():
            if not _matches(str(var_name), include):
                continue
            df = variable_to_frame(da)
            if dropna:
                df = df.dropna(subset=["value"])
            rel = Path(group) / f"{var_name}.parquet"
            (out_dir / rel).parent.mkdir(parents=True, exist_ok=True)
            df.to_parquet(out_dir / rel, index=False)
            manifest.variables.append(
                VariableEntry(
                    group=group,
                    name=str(var_name),
                    kind=da.attrs.get("kind"),
                    dims=[str(d) for d in da.dims],
                    units=da.attrs.get("units"),
                    path=rel.as_posix(),
                    rows=len(df),
                )
            )

    (out_dir / "manifest.json").write_text(
        json.dumps(asdict(manifest), indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return manifest


def export_file(nc_path: Path, out_dir: Path, run_id: str | None = None, **kwargs) -> Manifest:
    tree = xr.open_datatree(nc_path)
    try:
        return export_datatree(
            tree,
            out_dir,
            run_id=run_id or nc_path.parent.parent.parent.name or "run",
            source_file=str(nc_path),
            **kwargs,
        )
    finally:
        tree.close()


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description="Export EU-Flex model_outputs.nc to tidy Parquet.")
    p.add_argument("nc_path", type=Path, help="Path to model_outputs.nc")
    p.add_argument("--out", type=Path, required=True, help="Output directory")
    p.add_argument("--run-id", help="Run identifier (default: derived from path)")
    p.add_argument("--groups", nargs="*", help="Groups to export, e.g. base")
    p.add_argument("--include", action="append", help="Glob for variable names (repeatable)")
    p.add_argument("--keep-nan", action="store_true", help="Keep rows with NaN values")
    p.add_argument("--euflex-commit", help="EU-Flex git commit the run was produced with")
    p.add_argument("--config-file", help="EU-Flex config file used for the run")
    a = p.parse_args(argv)

    m = export_file(
        a.nc_path,
        a.out,
        run_id=a.run_id,
        groups=a.groups,
        include=a.include,
        dropna=not a.keep_nan,
        euflex_commit=a.euflex_commit,
        config_file=a.config_file,
    )
    print(f"Exported {len(m.variables)} variables to {a.out}")


if __name__ == "__main__":
    main()
