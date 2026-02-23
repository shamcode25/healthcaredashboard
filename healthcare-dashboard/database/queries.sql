-- ============================================================
-- Healthcare Analytics Dashboard - Analysis Queries
-- Tableau-ready SQL for reporting and visualization
-- ============================================================

-- ------------------------------------------------------------
-- Query 1 — Top 10 Most Common Diagnoses
-- Powers: Bar chart / horizontal bar chart of top diagnoses
-- ------------------------------------------------------------
SELECT 
  icd10_code,
  description,
  COUNT(*) as patient_count,
  ROUND(COUNT(*) * 100.0 / 
    (SELECT COUNT(*) FROM diagnoses), 2) 
    as percentage
FROM diagnoses
GROUP BY icd10_code, description
ORDER BY patient_count DESC
LIMIT 10;

-- ------------------------------------------------------------
-- Query 2 — Monthly Procedure Volume & Revenue
-- Powers: Line chart / area chart of procedure trends over time
-- ------------------------------------------------------------
SELECT
  strftime('%Y-%m', procedure_date) as month,
  COUNT(*) as procedure_count,
  ROUND(SUM(base_cost), 2) as total_revenue,
  ROUND(AVG(base_cost), 2) as avg_cost
FROM procedures
WHERE procedure_date IS NOT NULL
GROUP BY month
ORDER BY month;

-- ------------------------------------------------------------
-- Query 3 — Patient Demographics by Age Group & Gender
-- Powers: Stacked bar chart / heatmap of demographics
-- ------------------------------------------------------------
SELECT
  age_group,
  gender,
  COUNT(*) as patient_count,
  ROUND(AVG(age), 1) as avg_age
FROM patients
WHERE age_group IS NOT NULL AND age_group != 'Unknown'
GROUP BY age_group, gender
ORDER BY age_group, gender;

-- ------------------------------------------------------------
-- Query 4 — Top 10 Most Performed Procedures
-- Powers: Bar chart of procedure frequency and cost
-- ------------------------------------------------------------
SELECT
  cpt_code,
  description,
  COUNT(*) as frequency,
  ROUND(SUM(base_cost), 2) as total_cost,
  ROUND(AVG(base_cost), 2) as avg_cost
FROM procedures
GROUP BY cpt_code, description
ORDER BY frequency DESC
LIMIT 10;

-- ------------------------------------------------------------
-- Query 5 — Encounter Volume by Type & Class
-- Powers: Treemap / stacked bar of encounter breakdown
-- ------------------------------------------------------------
SELECT
  encounter_class,
  encounter_type,
  COUNT(*) as encounter_count,
  ROUND(AVG(total_cost), 2) as avg_cost,
  ROUND(SUM(total_cost), 2) as total_cost
FROM encounters
GROUP BY encounter_class, encounter_type
ORDER BY encounter_count DESC;

-- ------------------------------------------------------------
-- Query 6 — Diagnosis Trends by Quarter
-- Powers: Time series / trend analysis by quarter
-- ------------------------------------------------------------
SELECT
  strftime('%Y', diagnosed_date) as year,
  CASE 
    WHEN strftime('%m', diagnosed_date) 
         BETWEEN '01' AND '03' THEN 'Q1'
    WHEN strftime('%m', diagnosed_date) 
         BETWEEN '04' AND '06' THEN 'Q2'
    WHEN strftime('%m', diagnosed_date) 
         BETWEEN '07' AND '09' THEN 'Q3'
    ELSE 'Q4'
  END as quarter,
  icd10_code,
  description,
  COUNT(*) as case_count
FROM diagnoses
WHERE diagnosed_date IS NOT NULL
GROUP BY year, quarter, icd10_code, description
ORDER BY year, quarter, case_count DESC;

-- ------------------------------------------------------------
-- Query 7 — Patient Cost Analysis
-- Powers: Scatter plot / summary table of patient-level costs
-- ------------------------------------------------------------
SELECT
  p.patient_id,
  p.age_group,
  p.gender,
  p.state,
  COUNT(DISTINCT pr.procedure_id) as procedure_count,
  COUNT(DISTINCT d.diagnosis_id) as diagnosis_count,
  ROUND(SUM(pr.base_cost), 2) as total_procedure_cost,
  ROUND(SUM(e.total_cost), 2) as total_encounter_cost
FROM patients p
LEFT JOIN procedures pr ON p.patient_id = pr.patient_id
LEFT JOIN diagnoses d ON p.patient_id = d.patient_id
LEFT JOIN encounters e ON p.patient_id = e.patient_id
GROUP BY p.patient_id, p.age_group, p.gender, p.state
ORDER BY total_procedure_cost DESC;

-- ------------------------------------------------------------
-- Query 8 — Medication Usage Summary
-- Powers: Bar chart of top prescribed medications
-- ------------------------------------------------------------
SELECT
  description,
  medication_code,
  COUNT(*) as prescription_count,
  ROUND(AVG(base_cost), 2) as avg_cost,
  ROUND(SUM(base_cost), 2) as total_cost
FROM medications
GROUP BY medication_code, description
ORDER BY prescription_count DESC
LIMIT 15;

-- ------------------------------------------------------------
-- Query 9 — Payer Coverage Analysis
-- Powers: Grouped bar chart of coverage rates by year/class
-- ------------------------------------------------------------
SELECT
  strftime('%Y', start_date) as year,
  encounter_class,
  ROUND(AVG(total_cost), 2) as avg_total_cost,
  ROUND(AVG(payer_coverage), 2) as avg_covered,
  ROUND(AVG(total_cost - payer_coverage), 
        2) as avg_patient_responsibility,
  ROUND(AVG(payer_coverage) * 100.0 / 
    NULLIF(AVG(total_cost), 0), 2) as coverage_rate
FROM encounters
WHERE start_date IS NOT NULL
GROUP BY year, encounter_class
ORDER BY year, encounter_class;

-- ------------------------------------------------------------
-- Query 10 — State-Level Patient Distribution
-- Powers: Choropleth map / bar chart by state
-- ------------------------------------------------------------
SELECT
  state,
  COUNT(DISTINCT patient_id) as patient_count,
  COUNT(DISTINCT 
    CASE WHEN gender = 'Male' 
    THEN patient_id END) as male_count,
  COUNT(DISTINCT 
    CASE WHEN gender = 'Female' 
    THEN patient_id END) as female_count,
  ROUND(AVG(age), 1) as avg_age
FROM patients
WHERE state IS NOT NULL
GROUP BY state
ORDER BY patient_count DESC;
