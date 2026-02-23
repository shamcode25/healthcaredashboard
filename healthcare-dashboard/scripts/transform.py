"""
Healthcare Analytics Dashboard - Data Transform Script
Cleans and normalizes data for analytics and Tableau exports.
"""

import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "healthcare.db"


def get_connection():
    """Create SQLite database connection."""
    return sqlite3.connect(DB_PATH)


def parse_date(val):
    """Parse date string to YYYY-MM-DD format."""
    if pd.isna(val) or val == "" or val is None:
        return None
    try:
        # Extract date part (handle datetime strings like 2020-01-15T00:00:00)
        s = str(val).strip()
        if "T" in s:
            s = s.split("T")[0]
        if "." in s:
            s = s.split(".")[0]
        parsed = pd.to_datetime(s)
        return parsed.strftime("%Y-%m-%d") if pd.notna(parsed) else None
    except Exception:
        return None


def calculate_age(birth_date_str):
    """Calculate age from birth_date (YYYY-MM-DD)."""
    if pd.isna(birth_date_str) or not birth_date_str:
        return None
    try:
        birth = pd.to_datetime(birth_date_str)
        today = pd.Timestamp.now()
        age = (today - birth).days / 365.25
        return int(age) if age >= 0 else None
    except Exception:
        return None


def get_age_group(age):
    """Map age to age_group category."""
    if age is None or pd.isna(age):
        return "Unknown"
    if age <= 17:
        return "Pediatric"
    if age <= 34:
        return "Young Adult"
    if age <= 64:
        return "Adult"
    return "Senior"


def standardize_gender(val):
    """Standardize gender to Male / Female / Other."""
    if pd.isna(val) or val == "" or val is None:
        return "Other"
    v = str(val).strip().lower()
    if v in ("male", "m"):
        return "Male"
    if v in ("female", "f"):
        return "Female"
    return "Other"


def main():
    print("🔄 Healthcare Analytics Dashboard - Data Transform")
    print("=" * 50)

    if not DB_PATH.exists():
        print(f"❌ Database not found: {DB_PATH}")
        print("   Run scripts/load_data.py first.")
        return

    conn = get_connection()
    stats = {
        "patients_before": 0,
        "patients_after": 0,
        "patients_duplicates": 0,
        "diagnoses_before": 0,
        "diagnoses_after": 0,
        "diagnoses_null_dropped": 0,
        "procedures_before": 0,
        "procedures_after": 0,
        "procedures_null_dropped": 0,
    }

    try:
        # ----- PATIENTS -----
        df_patients = pd.read_sql_query("SELECT * FROM patients", conn)
        stats["patients_before"] = len(df_patients)

        # Remove duplicate patient records
        before_dedup = len(df_patients)
        df_patients = df_patients.drop_duplicates(subset=["patient_id"], keep="first")
        stats["patients_duplicates"] = before_dedup - len(df_patients)

        # Convert birth_date to proper DATE format
        df_patients["birth_date"] = df_patients["birth_date"].apply(
            lambda x: parse_date(x) if pd.notna(x) else None
        )

        # Calculate age and age_group
        df_patients["age"] = df_patients["birth_date"].apply(calculate_age)
        df_patients["age_group"] = df_patients["age"].apply(get_age_group)

        # Standardize gender
        df_patients["gender"] = df_patients["gender"].apply(standardize_gender)

        stats["patients_after"] = len(df_patients)
        df_patients.to_sql("patients", conn, if_exists="replace", index=False)

        # ----- DIAGNOSES -----
        df_diagnoses = pd.read_sql_query("SELECT * FROM diagnoses", conn)
        stats["diagnoses_before"] = len(df_diagnoses)

        # Drop rows where icd10_code is NULL or empty
        before_drop = len(df_diagnoses)
        df_diagnoses = df_diagnoses[
            df_diagnoses["icd10_code"].notna() & (df_diagnoses["icd10_code"].astype(str).str.strip() != "")
        ]
        stats["diagnoses_null_dropped"] = before_drop - len(df_diagnoses)

        # Convert diagnosed_date to proper DATE format
        df_diagnoses["diagnosed_date"] = df_diagnoses["diagnosed_date"].apply(
            lambda x: parse_date(x) if pd.notna(x) else None
        )

        stats["diagnoses_after"] = len(df_diagnoses)
        df_diagnoses.to_sql("diagnoses", conn, if_exists="replace", index=False)

        # ----- PROCEDURES -----
        df_procedures = pd.read_sql_query("SELECT * FROM procedures", conn)
        stats["procedures_before"] = len(df_procedures)

        # Drop rows where cpt_code is NULL or empty
        before_drop = len(df_procedures)
        df_procedures = df_procedures[
            df_procedures["cpt_code"].notna() & (df_procedures["cpt_code"].astype(str).str.strip() != "")
        ]
        stats["procedures_null_dropped"] = before_drop - len(df_procedures)

        # Convert procedure_date to proper DATE format
        df_procedures["procedure_date"] = df_procedures["procedure_date"].apply(
            lambda x: parse_date(x) if pd.notna(x) else None
        )

        stats["procedures_after"] = len(df_procedures)
        df_procedures.to_sql("procedures", conn, if_exists="replace", index=False)

        # ----- ENCOUNTERS - date formatting -----
        df_encounters = pd.read_sql_query("SELECT * FROM encounters", conn)
        df_encounters["start_date"] = df_encounters["start_date"].apply(
            lambda x: parse_date(x) if pd.notna(x) else None
        )
        df_encounters["end_date"] = df_encounters["end_date"].apply(
            lambda x: parse_date(x) if pd.notna(x) else None
        )
        df_encounters.to_sql("encounters", conn, if_exists="replace", index=False)

        # ----- MEDICATIONS - date formatting -----
        df_medications = pd.read_sql_query("SELECT * FROM medications", conn)
        df_medications["start_date"] = df_medications["start_date"].apply(
            lambda x: parse_date(x) if pd.notna(x) else None
        )
        df_medications["stop_date"] = df_medications["stop_date"].apply(
            lambda x: parse_date(x) if pd.notna(x) else None
        )
        df_medications.to_sql("medications", conn, if_exists="replace", index=False)

        conn.commit()

        # ----- DATA QUALITY SUMMARY -----
        print("\n📊 Data Quality Summary")
        print("-" * 40)
        print(f"  Patients:")
        print(f"    Before cleaning:     {stats['patients_before']:,}")
        print(f"    After cleaning:      {stats['patients_after']:,}")
        print(f"    Duplicates removed:  {stats['patients_duplicates']:,}")
        print(f"  Diagnoses:")
        print(f"    Before cleaning:     {stats['diagnoses_before']:,}")
        print(f"    After cleaning:      {stats['diagnoses_after']:,}")
        print(f"    Null/empty dropped:  {stats['diagnoses_null_dropped']:,}")
        print(f"  Procedures:")
        print(f"    Before cleaning:     {stats['procedures_before']:,}")
        print(f"    After cleaning:      {stats['procedures_after']:,}")
        print(f"    Null/empty dropped:  {stats['procedures_null_dropped']:,}")
        print("\n✅ Transform complete!")

    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
