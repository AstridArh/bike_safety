"""Update the shared LTS-segment-count CSV without replacing other regions."""
from pathlib import Path
from tempfile import NamedTemporaryFile
import math
import pandas as pd


def setting_label(setting):
    if str(setting).strip() in ("include all segments", "include all parts"):
        return "include all segments"
    value = float(setting)
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"Invalid segment length: {setting!r}")
    return f"{value:g}"


def save_region_segment_counts(data_output_dir, region, counts):
    """Upsert this region's supplied settings; preserve all other saved cells.

    Counts are numbers of LTS segments (including unmatched segments). Repeated runs
    replace existing values rather than appending duplicate region rows. A
    single-setting notebook updates only that setting's column.
    """
    path = Path(data_output_dir) / "lts_segments_by_region.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    region = str(region).strip()
    if not region or not counts:
        raise ValueError("Provide a region and at least one setting/count.")
    incoming = {}
    for setting, count in counts.items():
        label = setting_label(setting)
        if label in incoming:
            raise ValueError(f"Duplicate setting: {label}")
        if pd.isna(count) or not math.isfinite(float(count)) or float(count) < 0 or int(count) != float(count):
            raise ValueError(f"Invalid segment count for {label}: {count!r}")
        incoming[label] = int(count)
    legacy_path = path.with_name("lts_parts_by_region.csv")
    source_path = path if path.exists() else legacy_path
    if source_path.exists():
        table = pd.read_csv(source_path, index_col="Region")
        table.columns = [setting_label(column) for column in table.columns]
        if table.columns.duplicated().any():
            raise ValueError("The shared CSV has duplicate setting columns.")
        table.index = table.index.astype(str).str.strip()
        if table.index.str.casefold().duplicated().any():
            raise ValueError("The shared CSV has duplicate region rows.")
        matches = table.index[table.index.str.casefold() == region.casefold()]
        if len(matches):
            table = table.rename(index={matches[0]: region})
    else:
        table = pd.DataFrame(index=pd.Index([], name="Region"))
    columns = set(table.columns) | set(incoming)
    columns = sorted(columns, key=lambda value: (0, 0) if value == "include all segments" else (1, float(value)))
    index = list(table.index) if region in table.index else [*table.index, region]
    table = table.reindex(index=index, columns=columns)
    for label, count in incoming.items():
        table.loc[region, label] = count
    table = table.apply(pd.to_numeric, errors="raise").astype("Int64")
    table = table.sort_index(key=lambda values: values.str.casefold())
    table.index.name = "Region"
    temporary = None
    try:
        with NamedTemporaryFile(mode="w", dir=path.parent, prefix=path.name + ".", suffix=".tmp", newline="", delete=False) as handle:
            temporary = Path(handle.name)
            table.to_csv(handle, index_label="Region")
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return table, path


def save_region_part_counts(data_output_dir, region, counts):
    """Compatibility entry point for region notebooks using the earlier name."""
    return save_region_segment_counts(data_output_dir, region, counts)
