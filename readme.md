# NYC Taxi ETL Pipeline

This project loads NYC Yellow Taxi data into PostgreSQL through an ETL pipeline.

The entry point is `src/etl.py`, which orchestrates:

- `extract.fetch_taxi_file(...)`
- `transform.transform(...)`
- `load.init_db()`, `load.delete_existing_month(...)`, `load.load_dataframe(...)`

## 1) Prerequisites

- Python 3.10+
- A reachable PostgreSQL instance
- Target schema: `dwh` (created by `sql/ddl.sql`)

## 2) Configuration `.env`

The project automatically loads `.env` from the project root (`etl-nyc-taxi/.env`).

1. Create your local file:

```bash
cp .env.example .env
```

2. Fill in the variables:

```env
PG_HOST=localhost
PG_PORT=5432
PG_USER=postgres
PG_PASSWORD=postgres
PG_DB=nyc_taxi
```

Description:

- `PG_HOST`: PostgreSQL host
- `PG_PORT`: PostgreSQL port
- `PG_USER`: PostgreSQL user
- `PG_PASSWORD`: PostgreSQL password
- `PG_DB`: target database name

## 3) Install Dependencies

From the project root:

```bash
pip install pandas requests pyarrow sqlalchemy psycopg2-binary python-dotenv
```

## 4) Run the Pipeline

From the project root:

```bash
python src/etl.py -m 01 -y 2025
```

Options:

- `-m, --month` (required): month in `mm` format (example: `01`)
- `-y, --year` (required): year in `yyyy` format (example: `2025`)
- `-f, --force` (optional): force file download even if it already exists

Example with force:

```bash
python src/etl.py -m 01 -y 2025 -f
```

## 5) What `src/etl.py` Does

1. Downloads the monthly parquet file from the NYC Taxi source (`extract.py`)
2. Selects/cleans/enriches the data (`transform.py`)
3. Initializes the table (DDL), deletes existing rows for the given month/year, then inserts the new rows (`load.py`)

## 6) Data and Logs

- Downloaded raw files: `data/bronze/`
- SQL table creation script: `sql/ddl.sql`
- Runtime logs: `logs/info.log`

## 7) Data Quality Rules

Data quality rules used by the cleaning step are documented in:

- `data-quality-rules.md`
