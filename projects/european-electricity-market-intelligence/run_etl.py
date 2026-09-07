from __future__ import annotations

import argparse

from src.config import load_config
from src.pipeline import run_pipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="European electricity market ETL")
    parser.add_argument("--config", default="config.yml", help="Path to YAML configuration")
    parser.add_argument("--start", help="Inclusive start date, YYYY-MM-DD")
    parser.add_argument("--end", help="Exclusive end date, YYYY-MM-DD")
    parser.add_argument(
        "--sources",
        nargs="+",
        choices=["entsoe", "jao", "open_meteo"],
        default=["entsoe", "jao", "open_meteo"],
        help="Sources to extract",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    config = load_config(args.config)
    run_pipeline(
        config=config,
        start=args.start,
        end=args.end,
        sources=args.sources,
    )
