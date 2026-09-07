# European Electricity Market Intelligence

Initial ETL scaffold for a Master's thesis / portfolio project focused on **day-ahead electricity prices and cross-border power flows in Europe**.

## Research scope

Initial bidding zones:

- DE-LU
- FR
- BE
- NL
- PL
- CZ

Core targets for later modelling:

1. `day_ahead_price`
2. `physical_crossborder_flow_mw`

The pipeline is intentionally split into source-specific extractors so each source can be validated independently before the modelling layer is built.

## Current data sources

### ENTSO-E Transparency Platform
Primary market/system source. The ETL currently extracts:

- day-ahead prices
- actual total load
- day-ahead load forecast
- actual generation by type
- day-ahead generation forecast
- wind/solar forecast
- physical cross-border flows
- scheduled commercial exchanges
- day-ahead net transfer capacity

The implementation uses `entsoe-py`, which wraps the official ENTSO-E Transparency API.

### JAO Core Publication Tool
Cross-border capacity / flow-based market source. The first version extracts:

- Max Exchanges (MaxBex)
- Max Net Positions
- Final Computation / flow-based domain

JAO endpoints are configurable in `config.yml`, because JAO occasionally changes Publication Tool routes between versions.

### Open-Meteo
Historical hourly weather features:

- 2 m temperature
- 100 m wind speed
- shortwave radiation
- cloud cover

**Important:** historical realised weather is suitable for EDA and retrospective analysis, but must not be used as if it were known at day-ahead prediction time. A later modelling phase should use archived forecasts / previous model runs to avoid data leakage.

## Project structure

```text
projects/european-electricity-market-intelligence/
├── .env.example
├── .gitignore
├── config.yml
├── requirements.txt
├── run_etl.py
└── src/
    ├── __init__.py
    ├── config.py
    ├── io_utils.py
    ├── pipeline.py
    └── extractors/
        ├── __init__.py
        ├── entsoe.py
        ├── jao.py
        └── open_meteo.py
```

Raw output is written to `data/raw/<source>/` as Parquet files and is excluded from Git.

## Setup

```bash
cd projects/european-electricity-market-intelligence
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy the environment template:

```bash
copy .env.example .env
```

Add your ENTSO-E API token to `.env`:

```text
ENTSOE_API_KEY=...
```

JAO token is currently optional for the configured public endpoints, but support is included through `JAO_API_TOKEN` if authentication becomes mandatory.

## Run a small smoke test

The default configuration intentionally covers only a short period so the pipeline can be checked cheaply before requesting years of hourly data.

```bash
python run_etl.py --start 2024-01-01 --end 2024-01-08
```

Run selected sources only:

```bash
python run_etl.py --start 2024-01-01 --end 2024-01-03 --sources jao open_meteo
```

## Planned next ETL iterations

- archived weather forecasts instead of realised weather for strict day-ahead backtesting
- ECB FX rates for non-EUR bidding-zone prices
- EUA / CO2 price history
- gas and coal market factors
- source-level quality checks and schema tests
- staging layer with a unified hourly UTC grain
- modelling tables for price forecasting and cross-border-flow forecasting

## Data policy

Do not commit raw bulk datasets, API keys, passwords, or access tokens to Git. Keep secrets in `.env` and raw data under `data/`, both excluded by `.gitignore`.
