"""
Healthcare Analytics Dashboard - Data Loading Script
Loads Synthea CSV files into SQLite database (healthcare.db)
"""

import os
import sqlite3
import pandas as pd
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_RAW = BASE_DIR / "data" / "raw"
DB_PATH = BASE_DIR / "healthcare.db"
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"


def get_connection():
    """Create SQLite database connection."""
    return sqlite3.connect(DB_PATH)


def run_schema(conn):
    """Execute schema.sql to create tables."""
    if SCHEMA_PATH.exists():
        with open(SCHEMA_PATH, "r") as f:
            conn.executescript(f.read())
        conn.commit()
        print("📋 Schema applied successfully.")
    else:
        print("⚠️  schema.sql not found. Run schema.sql first to create tables.")


def _normalize_columns(df, mapping):
    """Rename columns using mapping, with case-insensitive fallback for Synthea."""
    col_map = {}
    for old, new in mapping.items():
        if old in df.columns:
            col_map[old] = new
        else:
            # Synthea may use different casing (e.g. BirthDate vs BIRTHDATE)
            for c in df.columns:
                if c.upper() == old.upper():
                    col_map[c] = new
                    break
    return df.rename(columns=col_map)


def load_patients(conn):
    """Load patients.csv into patients table."""
    filepath = DATA_RAW / "patients.csv"
    if not filepath.exists():
        print(f"⚠️  Skipping patients: {filepath} not found")
        return 0

    column_mapping = {
        "Id": "patient_id",
        "BIRTHDATE": "birth_date",
        "GENDER": "gender",
        "RACE": "race",
        "ETHNICITY": "ethnicity",
        "CITY": "city",
        "STATE": "state",
        "ZIP": "zip",
    }
    df = pd.read_csv(filepath)
    df = _normalize_columns(df, column_mapping)
    df = df[[c for c in column_mapping.values() if c in df.columns]]
    df.to_sql("patients", conn, if_exists="replace", index=False)
    count = len(df)
    print(f"   patients: {count:,} rows loaded")
    return count


def load_conditions(conn):
    """Load conditions.csv into diagnoses table."""
    filepath = DATA_RAW / "conditions.csv"
    if not filepath.exists():
        print(f"⚠️  Skipping conditions: {filepath} not found")
        return 0

    column_mapping = {
        "PATIENT": "patient_id",
        "CODE": "icd10_code",
        "DESCRIPTION": "description",
        "START": "diagnosed_date",
        "ENCOUNTER": "encounter_id",
    }
    df = pd.read_csv(filepath)
    df = _normalize_columns(df, column_mapping)
    df = df[[c for c in column_mapping.values() if c in df.columns]]
    df.insert(0, "diagnosis_id", range(1, len(df) + 1))
    df.to_sql("diagnoses", conn, if_exists="replace", index=False)
    count = len(df)
    print(f"   diagnoses: {count:,} rows loaded")
    return count


def load_procedures(conn):
    """Load procedures.csv into procedures table."""
    filepath = DATA_RAW / "procedures.csv"
    if not filepath.exists():
        print(f"⚠️  Skipping procedures: {filepath} not found")
        return 0

    column_mapping = {
        "PATIENT": "patient_id",
        "CODE": "cpt_code",
        "DESCRIPTION": "description",
        "DATE": "procedure_date",
        "BASE_COST": "base_cost",
        "ENCOUNTER": "encounter_id",
    }
    df = pd.read_csv(filepath)
    if "DATE" not in df.columns and "Start" in df.columns:
        df = df.rename(columns={"Start": "DATE"})
    df = _normalize_columns(df, column_mapping)
    df = df[[c for c in column_mapping.values() if c in df.columns]]
    df.insert(0, "procedure_id", range(1, len(df) + 1))
    df.to_sql("procedures", conn, if_exists="replace", index=False)
    count = len(df)
    print(f"   procedures: {count:,} rows loaded")
    return count


def load_encounters(conn):
    """Load encounters.csv into encounters table."""
    filepath = DATA_RAW / "encounters.csv"
    if not filepath.exists():
        print(f"⚠️  Skipping encounters: {filepath} not found")
        return 0

    column_mapping = {
        "Id": "encounter_id",
        "PATIENT": "patient_id",
        "ENCOUNTERCLASS": "encounter_class",
        "DESCRIPTION": "encounter_type",
        "START": "start_date",
        "STOP": "end_date",
        "TOTAL_CLAIM_COST": "total_cost",
        "PAYER_COVERAGE": "payer_coverage",
    }
    df = pd.read_csv(filepath)
    df = _normalize_columns(df, column_mapping)
    df = df[[c for c in column_mapping.values() if c in df.columns]]
    df.to_sql("encounters", conn, if_exists="replace", index=False)
    count = len(df)
    print(f"   encounters: {count:,} rows loaded")
    return count


def load_medications(conn):
    """Load medications.csv into medications table."""
    filepath = DATA_RAW / "medications.csv"
    if not filepath.exists():
        print(f"⚠️  Skipping medications: {filepath} not found")
        return 0

    column_mapping = {
        "PATIENT": "patient_id",
        "CODE": "medication_code",
        "DESCRIPTION": "description",
        "START": "start_date",
        "STOP": "stop_date",
        "BASE_COST": "base_cost",
    }
    df = pd.read_csv(filepath)
    df = _normalize_columns(df, column_mapping)
    df = df[[c for c in column_mapping.values() if c in df.columns]]
    df.insert(0, "medication_id", range(1, len(df) + 1))
    df.to_sql("medications", conn, if_exists="replace", index=False)
    count = len(df)
    print(f"   medications: {count:,} rows loaded")
    return count


def main():
    print("🏥 Healthcare Analytics Dashboard - Data Loader")
    print("=" * 50)

    if not DATA_RAW.exists():
        print(f"❌ Data directory not found: {DATA_RAW}")
        print("   Create data/raw/ and add Synthea CSV files.")
        return

    conn = get_connection()
    try:
        run_schema(conn)
        print("\n📂 Loading CSV files from data/raw/:")
        load_patients(conn)
        load_conditions(conn)
        load_procedures(conn)
        load_encounters(conn)
        load_medications(conn)
        conn.commit()
        print("\n✅ Database loaded successfully!")
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
