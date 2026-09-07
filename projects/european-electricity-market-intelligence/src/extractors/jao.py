from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any

import pandas as pd
import requests

from src.io_utils import write_parquet


def _records_from_payload(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]

    if isinstance(payload, dict):
        for key in ("data", "items", "results", "value"):
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
        return [payload]

    return []


def _headers() -> dict[str, str]:
    token = os.getenv("JAO_API_TOKEN", "").strip()
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def extract_jao_dataset(
    name: str,
    endpoint: str,
    start: str,
    end: str,
    output_dir: str | Path,
    timeout_seconds: int = 60,
    sleep_seconds: float = 0.15,
) -> Path | None:
    """Extract a JAO Core dataset one business day at a time.

    Current Core Publication Tool documentation exposes GET endpoints that
    accept a UTC `date` query parameter. Iterating by day keeps requests small
    and makes partial reruns straightforward.
    """
    start_ts = pd.Timestamp(start, tz="UTC")
    end_ts = pd.Timestamp(end, tz="UTC")

    session = requests.Session()
    rows: list[dict[str, Any]] = []

    for day in pd.date_range(start_ts.normalize(), end_ts.normalize(), inclusive="left"):
        date_param = day.strftime("%Y-%m-%dT00:00:00.000Z")
        response = session.get(
            endpoint,
            params={"date": date_param},
            headers=_headers(),
            timeout=timeout_seconds,
        )

        if response.status_code in {204, 404}:
            continue

        response.raise_for_status()
        payload = response.json()
        day_rows = _records_from_payload(payload)
        for row in day_rows:
            row.setdefault("requested_business_date_utc", day.date().isoformat())
        rows.extend(day_rows)
        time.sleep(sleep_seconds)

    if not rows:
        print(f"[JAO] No rows returned for {name}")
        return None

    df = pd.json_normalize(rows)
    for column in df.columns:
        if "date" in column.lower() or "time" in column.lower():
            try:
                df[column] = pd.to_datetime(df[column], utc=True)
            except (ValueError, TypeError):
                pass

    output_path = Path(output_dir) / f"{name}_{start}_{end}.parquet"
    write_parquet(df, output_path)
    print(f"[JAO] {name}: {len(df):,} rows -> {output_path}")
    return output_path


def extract_all_jao(config: dict[str, Any], start: str, end: str, raw_dir: str | Path) -> None:
    jao_config = config["jao"]
    output_dir = Path(raw_dir) / "jao"

    for name, endpoint in jao_config["endpoints"].items():
        extract_jao_dataset(
            name=name,
            endpoint=endpoint,
            start=start,
            end=end,
            output_dir=output_dir,
            timeout_seconds=int(jao_config.get("request_timeout_seconds", 60)),
            sleep_seconds=float(jao_config.get("sleep_between_requests_seconds", 0.15)),
        )
