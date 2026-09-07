from __future__ import annotations

from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from src.extractors.entsoe import extract_all_entsoe
from src.extractors.jao import extract_all_jao
from src.extractors.open_meteo import extract_all_open_meteo


def run_pipeline(
    config: dict[str, Any],
    start: str | None = None,
    end: str | None = None,
    sources: list[str] | None = None,
) -> None:
    load_dotenv()

    project = config["project"]
    start = start or project["start"]
    end = end or project["end"]
    raw_dir = Path(project["raw_dir"])
    sources = sources or ["entsoe", "jao", "open_meteo"]

    if str(start) >= str(end):
        raise ValueError("`start` must be earlier than `end`")

    print(f"ETL period: {start} -> {end} (end exclusive)")
    print(f"Sources: {', '.join(sources)}")

    if "entsoe" in sources:
        extract_all_entsoe(config, start, end, raw_dir)

    if "jao" in sources:
        extract_all_jao(config, start, end, raw_dir)

    if "open_meteo" in sources:
        extract_all_open_meteo(config, start, end, raw_dir)

    print("ETL extraction finished.")
