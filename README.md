# Semiconductor Fabrication Yield & Sensor Optimization Analysis

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![SQL](https://img.shields.io/badge/Database-SQLite-orange.svg)](https://www.sqlite.org/)
[![Power BI](https://img.shields.io/badge/BI-Power%20BI-yellow.svg)](https://powerbi.microsoft.com/)
[![Excel](https://img.shields.io/badge/Reports-Excel-green.svg)](https://www.microsoft.com/en-us/microsoft-365/excel)
[![Status](https://img.shields.io/badge/Status-Portfolio%20Ready-brightgreen.svg)]()

## 📌 Project Overview
A semiconductor fabrication plant manufacturing 90nm wafers is experiencing increased **Post-Etch defect rates** and declining **wafer yield**. This project performs a complete data analytics investigation to identify:

- Which **fabrication machines** produce the most defects
- Whether **Chamber Pressure, Voltage, or Gas Flow** correlate with yield loss
- Which **wafer batches** fail most often
- The **financial cost** of yield degradation

The workflow simulates a real-world semiconductor MES (Manufacturing Execution System) analytics pipeline, similar to environments at **NVIDIA, Intel, Qualcomm, and Texas Instruments**.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python (Pandas, NumPy) | Data cleaning, statistical analysis |
| Matplotlib & Seaborn | EDA visualizations |
| SQLite + SQL | Database schema and analytical queries |
| Microsoft Excel | Cost of Quality financial modeling |
| Power BI | Interactive executive dashboards |

---

## 📂 Project Structure

```
WaferSense/
├── datasets/
│   ├── generate_data.py       # Synthetic data generator (5,500 wafer records)
│   ├── load_data.py           # Loads CSVs into SQLite database
│   ├── wafers.csv             # Wafer manufacturing records
│   ├── telemetry.csv          # Sensor telemetry readings (25,000 records)
│   └── maintenance.csv        # Machine maintenance logs
├── sql/
│   ├── schema.sql             # Database schema (tables, indexes, views)
│   └── analytics_queries.sql  # 8 analytical queries (JOINs, CTEs, CASE, HAVING)
├── notebooks/
│   ├── eda_analysis.py        # Full EDA pipeline (cleaning + visualizations)
│   └── semiconductor_analysis.ipynb  # Interactive Jupyter Notebook
├── excel/
│   ├── generate_excel_report.py     # Script to generate Excel workbook
│   └── Cost_of_Quality_Analysis.xlsx # Financial impact workbook
├── screenshots/               # All generated charts and visualizations
├── docs/
│   └── interview_qa.md        # Interview Q&A preparation guide
└── README.md
```

---

## 🚀 How to Run the Project

### Prerequisites
```bash
pip install pandas numpy matplotlib seaborn xlsxwriter
```

### Step 1 — Generate Datasets
```bash
python datasets/generate_data.py
```

### Step 2 — Load into SQLite Database
```bash
python datasets/load_data.py
```

### Step 3 — Run Python EDA Analysis
```bash
python notebooks/eda_analysis.py
```
Charts saved to `screenshots/`

### Step 4 — Generate Excel Report
```bash
python excel/generate_excel_report.py
```

### Step 5 — Run SQL Queries
Open `sql/analytics_queries.sql` in DB Browser for SQLite or any SQL client connected to `wafersense.db`.

---

## 📊 Key Findings

| Finding | Detail |
|---------|--------|
| **Root Cause Machine** | `MACH_002` — highest defect count, chamber pressure consistently above 52 mTorr |
| **Pressure Correlation** | Pearson r = **0.934** between Chamber Pressure and Gate Oxide Thickness |
| **Yield Impact** | MACH_002 has a **~35% higher failure rate** than other machines |
| **Financial Impact** | Every 1% yield drop → ~**$27,500 scrap cost** per production run |
| **Cleaning Result** | IQR method removed **72 sensor noise outliers** from 5,500 records |

---

## 📝 Resume Bullet Points

- **Built a Semiconductor Manufacturing Analytics Pipeline** using Python (Pandas, NumPy, Seaborn) and SQL to analyze 5,500+ wafer records, uncovering a chamber pressure drift in MACH_002 as the root cause of Post-Etch yield degradation.
- **Designed and queried a SQLite MES database** using advanced SQL (CTEs, Window Functions, CASE statements, HAVING filters) to rank machines by defect rate and sensor drift frequency.
- **Generated 6 professional EDA visualizations** (correlation heatmaps, box plots, scatter plots, time-series trends) using Matplotlib and Seaborn to communicate process anomalies to stakeholders.
- **Modeled financial impact of yield loss** in Excel, estimating $27,500+ scrap cost per 1% yield drop using Cost of Quality analysis with pivot tables and conditional formatting.

---

## ❓ Interview Q&A

**Q: What was your biggest finding in this project?**
> Machine `MACH_002` showed a Chamber Pressure drift of ~4 mTorr above spec. A Pearson correlation of 0.934 between Pressure and Gate Oxide Thickness confirmed this as the root cause of yield failures — exactly the kind of insight a process engineer would act on immediately.

**Q: Why did you use the IQR method for outlier removal?**
> IQR is non-parametric and robust to extreme values — ideal for sensor data that may spike due to calibration resets rather than real process changes. This prevented misleading our correlation analysis.

**Q: How does Chamber Pressure affect Gate Oxide quality?**
> During plasma etching, pressure controls plasma density. Higher-than-spec pressure increases the etch rate, thinning the Gate Oxide below the 90nm target and causing electrical failures. This is a known failure mode in CMOS fabrication.

See full Q&A in [docs/interview_qa.md](docs/interview_qa.md)

---

## 🏗️ Architecture

```
Raw Data Generation
        │
        ▼
CSV Files (wafers, telemetry, maintenance)
        │
        ▼
SQLite Database (schema.sql + load_data.py)
        │
   ┌────┴────┐
   ▼         ▼
SQL Queries  Python EDA Pipeline
(analytics   (eda_analysis.py)
_queries.sql)     │
                  ▼
           Visualizations
           (screenshots/)
                  │
   ┌──────────────┤
   ▼              ▼
Excel Report  Power BI Dashboard
(Cost of      (Executive + Machine
 Quality)      Analytics Views)
```

---

*Built as a portfolio project for Data Analyst and Semiconductor Analytics roles.*
