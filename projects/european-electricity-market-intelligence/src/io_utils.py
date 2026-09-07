from __future__ import annotations

from pathlib import Path

import pandas as pd


def flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    if isinstance(result.columns, pd.MultiIndex):
        result.columns = [
            "__".join(str(part) for part in column if str(part) not in {"", "None"})
            for column in result.columns
        ]
    else:
        result.columns = [str(column) for column in result.columns]
    return result


def pandas_object_to_frame(obj: pd.Series | pd.DataFrame, value_name: str = "value") -> pd.DataFrame:
    if isinstance(obj, pd.Series):
        frame = obj.rename(value_name).to_frame()
    elif isinstance(obj, pd.DataFrame):
        frame = obj.copy()
    else:
        raise TypeError(f"Unsupported pandas object: {type(obj)!r}")

    frame = flatten_columns(frame)
    frame = frame.reset_index()

    if len(frame.columns) > 0 and frame.columns[0] in {"index", "level_0"}:
        frame = frame.rename(columns={frame.columns[0]: "timestamp"})

    for column in frame.columns:
        if "time" in column.lower() or "date" in column.lower():
            try:
                frame[column] = pd.to_datetime(frame[column], utc=True)
            except (ValueError, TypeError):
                pass

    return frame


def write_parquet(df: pd.DataFrame, path: str | Path) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)
    return output_path
