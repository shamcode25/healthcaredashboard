-- Healthcare Analytics Dashboard - Database Schema
-- Compatible with SQLite (used for local development and Tableau data prep)

-- ============================================
-- 1. PATIENTS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS patients (
    patient_id TEXT PRIMARY KEY,
    birth_date DATE,
    gender TEXT,
    race TEXT,
    ethnicity TEXT,
    city TEXT,
    state TEXT,
    zip TEXT,
    age INTEGER,
    age_group TEXT
);

-- ============================================
-- 2. DIAGNOSES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS diagnoses (
    diagnosis_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT,
    icd10_code TEXT,
    description TEXT,
    diagnosed_date DATE,
    encounter_id TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);

-- ============================================
-- 3. PROCEDURES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS procedures (
    procedure_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT,
    cpt_code TEXT,
    description TEXT,
    procedure_date DATE,
    base_cost DECIMAL,
    encounter_id TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);

-- ============================================
-- 4. ENCOUNTERS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS encounters (
    encounter_id TEXT PRIMARY KEY,
    patient_id TEXT,
    encounter_class TEXT,
    encounter_type TEXT,
    start_date DATE,
    end_date DATE,
    total_cost DECIMAL,
    payer_coverage DECIMAL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);

-- ============================================
-- 5. MEDICATIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS medications (
    medication_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT,
    medication_code TEXT,
    description TEXT,
    start_date DATE,
    stop_date DATE,
    base_cost DECIMAL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);

-- ============================================
-- 6. ICD10 MASTER TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS icd10_master (
    code TEXT PRIMARY KEY,
    description TEXT,
    category TEXT,
    chapter TEXT
);

-- ============================================
-- 7. CPT MASTER TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS cpt_master (
    code TEXT PRIMARY KEY,
    description TEXT,
    category TEXT
);

-- Create indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_diagnoses_patient ON diagnoses(patient_id);
CREATE INDEX IF NOT EXISTS idx_diagnoses_icd10 ON diagnoses(icd10_code);
CREATE INDEX IF NOT EXISTS idx_diagnoses_date ON diagnoses(diagnosed_date);
CREATE INDEX IF NOT EXISTS idx_procedures_patient ON procedures(patient_id);
CREATE INDEX IF NOT EXISTS idx_procedures_date ON procedures(procedure_date);
CREATE INDEX IF NOT EXISTS idx_encounters_patient ON encounters(patient_id);
CREATE INDEX IF NOT EXISTS idx_medications_patient ON medications(patient_id);
