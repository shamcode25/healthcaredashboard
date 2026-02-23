# Healthcare Analytics Dashboard



## Description

This project ingests synthetic healthcare data (Synthea), loads it into a SQLite database, cleans and transforms it, and exports analysis-ready CSV files for visualization in Tableau. It showcases end-to-end data pipeline skills relevant to hospital analytics and clinical reporting.

## Tech Stack

- **Python** — Data loading, transformation, export
- **SQLite** — Relational database
- **SQL** — Schema design, analysis queries
- **Tableau** — Visualization (connect to exported CSVs)
- **Synthea** — Synthetic patient data generator

## Dataset

[Synthea](https://github.com/synthetichealth/synthea) is an open-source synthetic patient generator that creates realistic (but fake) healthcare records. Download the CSV export and place the required files in `data/raw/`.

### Required CSV Files

- `patients.csv`
- `conditions.csv`
- `procedures.csv`
- `encounters.csv`
- `medications.csv`

## Installation

1. **Clone or download** this project.

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

### Step 1: Download Synthea Data

1. Clone [Synthea](https://github.com/synthetichealth/synthea) and run it with `exporter.csv.export = true` in `synthea.properties`, or download a pre-built CSV export from the [Synthea Sample Data](https://synthetichealth.github.io/synthea-sample-data/) (if available).
2. Place the following files in `data/raw/`:
   - `patients.csv`
   - `conditions.csv`
   - `procedures.csv`
   - `encounters.csv`
   - `medications.csv`

### Step 2: Place CSVs in data/raw/

Ensure all 5 CSV files are in the `healthcare-dashboard/data/raw/` directory.

### Step 3: Load Data

```bash
python scripts/load_data.py
```

Creates `healthcare.db` and loads all CSV data into the database.

### Step 4: Transform Data

```bash
python scripts/transform.py
```

Cleans data: removes duplicates, drops nulls, standardizes dates, adds age/age_group, standardizes gender.

### Step 5: Export Reports

```bash
python scripts/export.py
```

Runs all 10 analysis queries and saves CSVs to `reports/output/`.

### Step 6: Open in Tableau

Connect Tableau to the CSV files in `reports/output/` to build dashboards and visualizations.

## SQL Analysis Queries

| # | Query | Output File | What It Analyzes |
|---|-------|-------------|------------------|
| 1 | Top 10 Most Common Diagnoses | `top_diagnoses.csv` | ICD-10 diagnosis frequency and percentage |
| 2 | Monthly Procedure Volume & Revenue | `monthly_procedures.csv` | Procedure trends over time, revenue |
| 3 | Patient Demographics by Age Group & Gender | `patient_demographics.csv` | Demographics breakdown |
| 4 | Top 10 Most Performed Procedures | `top_procedures.csv` | CPT procedure frequency and cost |
| 5 | Encounter Volume by Type & Class | `encounter_summary.csv` | Encounter mix and costs |
| 6 | Diagnosis Trends by Quarter | `diagnosis_trends.csv` | Quarterly diagnosis trends |
| 7 | Patient Cost Analysis | `patient_cost_analysis.csv` | Per-patient procedure and encounter costs |
| 8 | Medication Usage Summary | `medication_summary.csv` | Top 15 prescribed medications |
| 9 | Payer Coverage Analysis | `payer_coverage.csv` | Coverage rates by year and encounter class |
| 10 | State-Level Patient Distribution | `state_distribution.csv` | Geographic patient distribution |

## Project Structure

```
healthcare-dashboard/
├── data/
│   └── raw/              ← Synthea CSVs go here
├── database/
│   ├── schema.sql        ← CREATE TABLE statements
│   └── queries.sql      ← Analysis queries
├── scripts/
│   ├── load_data.py      ← Load CSVs into SQLite
│   ├── transform.py     ← Clean and normalize data
│   └── export.py        ← Export for Tableau
├── reports/
│   └── output/          ← Final CSV exports
├── requirements.txt
└── README.md
```

## Web Dashboard (No Tableau Required)

A single-page HTML dashboard visualizes all 10 reports in the browser.

**Run locally:**
```bash
cd healthcare-dashboard
python3 -m http.server 8080
```
Then open http://localhost:8080/dashboard.html

**Note:** The dashboard loads CSVs via fetch, so it must be served over HTTP (not opened as `file://`).

## Screenshots

*(Add Table<img width="329" height="555" alt="Screenshot 2026-02-22 at 7 11 49 PM" src="https://github.com/user-attachments/assets/2257ce62-39bf-433c-b75b-5ed32364ac53" />
au dashboard screenshots here for your portfolio)*
<img width="728" height="602" alt="Screenshot 2026-02-22 at 7 11 29 PM" src="https://github.com/user-attachments/assets/8aa903dc-0a6c-48a1-bc9c-b7743df66c40" />

---<img width="637" height="560" alt="Screenshot 2026-02-22 at 7 12 12 PM" src="https://github.com/user-attachments/assets/10ca0064-0e35-4032-9869-e1b76d4534a0" />
<img width="814" height="523" alt="Screenshot 2026-02-22 at 7 12 52 PM" src="https://github.com/user-attachments/assets/b3d50b80-e708-44fb-ae80-5ad9e4151c1f" />


Built for portfolio use. Ideal for BI/Epic IT roles at healthcare organizations like NewYork-Presbyterian.
