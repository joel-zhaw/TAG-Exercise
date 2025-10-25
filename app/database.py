import os
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import Engine

# --- 1. Database Setup ---

# Assumes the notebook's setup code is run once to create the database file
DB_PATH = Path("demo.db")
DB_URI = f"sqlite:///file:{DB_PATH.resolve()}?mode=ro&uri=true"
engine: Engine = create_engine(DB_URI, connect_args={"uri": True})


# --- 2. Schema Extraction (for LLM Grounding) ---
insp = inspect(engine)
SCHEMA_STR = "\n".join(
    f"CREATE TABLE {t} ({', '.join(c['name'] for c in insp.get_columns(t))});"
    for t in insp.get_table_names()
)
schema = SCHEMA_STR

# --- 3. SQL Execution Function ---
def run_sql(engine: Engine, sql: str) -> pd.DataFrame:
    with engine.connect() as conn:
        df = pd.read_sql_query(sql, conn)
    return df