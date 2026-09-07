from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Callable

import pandas as pd
from entsoe import EntsoePandasClient
from entsoe.exceptions import NoMatchingDataError

from src.io_utils import pandas_object_to_frame, write_parquet


def _client() -> EntsoePandasClient:
    api_key = os.getenv("ENTSOE_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "ENTSOE_API_KEY is missing. Copy .env.example to .env and add your Transparency Platform token."
        )
    return EntsoePandasClient(api_key=api_key)


def _safe_query(
    label: str,
    query: Callable[[], pd.Series | pd.DataFrame],
    output_path: Path,
    metadata: dict[str, str],
) -> None:
    try:
        result = query()
    except NoMatchingDataError:
        print(f"[ENTSO-E] No matching data: {label}")
        return

    frame = pandas_object_to_frame(result)
    for key, value in metadata.items():
        frame[key] = value
    write_parquet(frame, output_path)
    print(f"[ENTSO-E] {label}: {len(frame):,} rows -> {output_path}")


def extract_all_entsoe(config: dict[str, Any], start: str, end: str, raw_dir: str | Path) -> None:
    client = _client()
    entsoe_config = config["entsoe"]
    output_dir = Path(raw_dir) / "entsoe"

    start_ts = pd.Timestamp(start, tz="UTC")
    end_ts = pd.Timestamp(end, tz="UTC")

    for zone in entsoe_config["zones"]:
        zone_dir = output_dir / "zones" / zone

        zone_queries: dict[str, Callable[[], pd.Series | pd.DataFrame]] = {
            "day_ahead_prices": lambda zone=zone: client.query_day_ahead_prices(zone, start=start_ts, end=end_ts),
            "actual_load": lambda zone=zone: client.query_load(zone, start=start_ts, end=end_ts),
            "load_forecast": lambda zone=zone: client.query_load_forecast(zone, start=start_ts, end=end_ts),
            "actual_generation": lambda zone=zone: client.query_generation(zone, start=start_ts, end=end_ts),
            "generation_forecast": lambda zone=zone: client.query_generation_forecast(zone, start=start_ts, end=end_ts),
            "wind_solar_forecast": lambda zone=zone: client.query_wind_and_solar_forecast(zone, start=start_ts, end=end_ts),
        }

        for dataset, query in zone_queries.items():
            _safe_query(
                label=f"{zone}/{dataset}",
                query=query,
                output_path=zone_dir / f"{dataset}_{start}_{end}.parquet",
                metadata={"zone": zone, "dataset": dataset, "source": "ENTSO-E"},
            )

    for country_from, country_to in entsoe_config["borders"]:
        border = f"{country_from}__{country_to}"
        border_dir = output_dir / "borders" / border

        border_queries: dict[str, Callable[[], pd.Series | pd.DataFrame]] = {
            "physical_flows": lambda country_from=country_from, country_to=country_to: client.query_crossborder_flows(
                country_from, country_to, start=start_ts, end=end_ts
            ),
            "scheduled_exchanges": lambda country_from=country_from, country_to=country_to: client.query_scheduled_exchanges(
                country_from, country_to, start=start_ts, end=end_ts, dayahead=True
            ),
            "day_ahead_ntc": lambda country_from=country_from, country_to=country_to: client.query_net_transfer_capacity_dayahead(
                country_from, country_to, start=start_ts, end=end_ts
            ),
        }

        for dataset, query in border_queries.items():
            _safe_query(
                label=f"{border}/{dataset}",
                query=query,
                output_path=border_dir / f"{dataset}_{start}_{end}.parquet",
                metadata={
                    "country_from": country_from,
                    "country_to": country_to,
                    "dataset": dataset,
                    "source": "ENTSO-E",
                },
            )
