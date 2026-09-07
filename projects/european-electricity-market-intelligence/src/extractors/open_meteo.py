from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import requests

from src.io_utils import write_parquet


def extract_location_weather(
    api_url: str,
    zone: str,
    location: dict[str, Any],
    hourly_variables: list[str],
    start: str,
    end: str,
    output_dir: str | Path,
) -> Path:
    # Open-Meteo end_date is inclusive, whereas this project treats `end` as exclusive.
    inclusive_end = (pd.Timestamp(end) - pd.Timedelta(days=1)).strftime("%Y-%m-%d")

    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "start_date": pd.Timestamp(start).strftime("%Y-%m-%d"),
        "end_date": inclusive_end,
        "hourly": ",".join(hourly_variables),
        "timezone": "UTC",
    }

    response = requests.get(api_url, params=params, timeout=60)
    response.raise_for_status()
    payload = response.json()

    hourly = payload.get("hourly")
    if not hourly or "time" not in hourly:
        raise ValueError(f"Open-Meteo returned no hourly data for {zone}")

    df = pd.DataFrame(hourly)
    df["time"] = pd.to_datetime(df["time"], utc=True)
    df["zone"] = zone
    df["location_name"] = location["name"]
    df["latitude"] = location["latitude"]
    df["longitude"] = location["longitude"]
    df["source"] = "Open-Meteo"

    output_path = Path(output_dir) / f"weather_{zone}_{start}_{end}.parquet"
    write_parquet(df, output_path)
    print(f"[Open-Meteo] {zone}: {len(df):,} rows -> {output_path}")
    return output_path


def extract_all_open_meteo(config: dict[str, Any], start: str, end: str, raw_dir: str | Path) -> None:
    source_config = config["open_meteo"]
    output_dir = Path(raw_dir) / "open_meteo"

    for zone, location in source_config["locations"].items():
        extract_location_weather(
            api_url=source_config["url"],
            zone=zone,
            location=location,
            hourly_variables=list(source_config["hourly"]),
            start=start,
            end=end,
            output_dir=output_dir,
        )
