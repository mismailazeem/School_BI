# Product Requirements Document (PRD)
## School BI Dashboard — Interactive Analytics Platform

**Version:** 2.0 | **Date:** 2026-02-22 | **Status:** Production-Ready

---

## 1. Overview

An enterprise-grade Business Intelligence dashboard for a Pakistani school system (Classes 1–10, Sections A & B, ~611 students). Built with **Streamlit + Plotly**, it transforms 5 raw CSV datasets into actionable insights across academics, attendance, finance, and parent engagement.

## 2. Problem Statement

School administrators lack a unified view of student performance, attendance risks, fee collection gaps, and parent satisfaction. Data lives in separate CSV files with no cross-analysis or visualization capability.

## 3. Objectives

| # | Objective | Success Metric |
|---|---|---|
| 1 | Unified KPI dashboard | All 5 data sources in one view |
| 2 | Individual student tracking | Lookup by ID with exportable report |
| 3 | Risk identification | At-risk students flagged (<75% attendance) |
| 4 | Financial oversight | Fee defaulters identified (>=3 unpaid months) |
| 5 | Parent communication | Progress reports with SMS-ready templates |

## 4. Data Sources

| File | Rows | Description |
|---|---|---|
| `Students_Master_Table.csv` | 611 | Student demographics, guardian info, fee/scholarship status |
| `Exam_Results_Table.csv` | ~48,801 | Monthly test (50), midterm (100), final (100) per subject |
| `Attendance_Table.csv` | ~6,101 | Monthly attendance percentages |
| `Fee_Collection_Table.csv` | ~6,101 | Monthly fee, amount paid, payment status |
| `Teacher_Table.csv` | 80 | Teacher assignments by subject and class |
| `Dropout_Log.csv` | 42 | Simulated dropout records with risk scores |
| `Transfer_Log.csv` | 19 | Section transfer records |
| `Parent_Survey_Table.csv` | 610 | 5-dimension satisfaction ratings + NPS |
| `School_Comparison_Table.csv` | 5 | Multi-school ranking comparison |

## 5. Feature Specifications

### 5.1 Dashboard Pages (7 Tabs)

| Tab | Features |
|---|---|
| 🏠 **Executive** | 6 KPI cards, monthly trend line, fee donut, gender bar chart, class stats table |
| 📊 **Academic** | Subject×Month heatmap, Section A vs B, top/bottom 5 students, grade distribution |
| 📋 **Attendance** | Risk identification, scatter plot with Pearson correlation, category donut, at-risk table |
| 💰 **Financial** | Revenue expected vs collected, collection rate trend, class revenue, fee defaulters list |
| 🔎 **Student Lookup** | ID-based search, profile card, 4-panel progress chart, progress bars, export & SMS |
| 📤 **Upload Data** | CSV upload for any dataset, preview, apply to dashboard, data status monitor |
| 📈 **Rankings** | School comparison bar chart, parent survey ratings, NPS distribution, dropout analysis |

### 5.2 Advanced Features

| Feature | Detail |
|---|---|
| **Dark/Light Mode** | Sidebar toggle; 30+ CSS variables switch between navy-blue light theme and slate dark theme |
| **Interactive Filters** | Class, Section, Month, Gender — applied globally across all tabs |
| **Student Progress Export** | PNG, JPEG, SVG, PDF image export + HTML report download |
| **Parent Notification** | Contact number input, 4 message templates (Full, Academic, Attendance, Fee), SMS preview |
| **CSV Upload** | Upload any of 5 datasets; live-replace dashboard data; reset to originals |
| **Calculated Metrics** | Total Score, Percentage, Grade (A+–F), Performance Band, Risk flags, Pearson r |

### 5.3 Computed KPIs

| Category | KPIs |
|---|---|
| Academic | Avg %, Pass Rate (>=33%), Grade Distribution, Subject Averages, Monthly Trend |
| Attendance | Avg %, At-Risk Count (<75%), Excellent Rate (>=90%), Critical Rate (<60%), Pearson Correlation |
| Financial | Expected/Collected Revenue, Collection %, Outstanding Amount, Defaulter Count (>=3 months) |
| Survey | NPS Score, Satisfaction by Category (Teaching, Discipline, Communication, Fee), Promoters/Detractors |
| Dropout | Dropout Rate, Transfer Count, Reason Distribution, Class-wise Distribution |

## 6. Technical Architecture

### Stack
| Layer | Technology |
|---|---|
| Frontend | Streamlit 1.54+ with custom CSS |
| Charting | Plotly 6.x (interactive, exportable) |
| Data | Pandas, NumPy |
| Image Export | Kaleido (optional) |
| Language | Python 3.13 |

### File Structure
```
Schhol_Dashboard/
├── app.py                         # Main dashboard (7 tabs)
├── dashboard_utils.py             # Theme engine, helpers
├── Students_Master_Table.csv      # Source data
├── Exam_Results_Table.csv
├── Attendance_Table.csv
├── Fee_Collection_Table.csv
├── Teacher_Table.csv
├── Dropout_Log.csv                # Generated
├── Transfer_Log.csv
├── MidYear_Admissions.csv
├── Parent_Survey_Table.csv
├── School_Comparison_Table.csv
├── generate_simulation_data.py    # Data generators
├── generate_survey_data.py
├── generate_school_comparison.py
├── School_BI_Data_Model.md        # Star Schema docs
├── DAX_Measures_Library.dax       # Power BI DAX
├── SQL_Schema_and_Queries.sql     # T-SQL scripts
├── Dashboard_Wireframe.md         # UX specification
├── PowerBI_Implementation_Guide.md
├── PRD.md                         # This document
└── README.md                      # GitHub readme
```

## 7. Star Schema Data Model

```
Dim_Student ──┐
Dim_Subject ──┤
Dim_Month ────┼──► Fact_Exam_Results
Dim_Teacher ──┘    Fact_Attendance
                   Fact_Fee_Collection
Dim_School ──────► Fact_School_Comparison
Dim_Survey_Response
```

Detailed model: see `School_BI_Data_Model.md`

## 8. Non-Functional Requirements

| Requirement | Target |
|---|---|
| Load time | < 3 seconds for 48K rows |
| Browser support | Chrome, Edge, Firefox |
| Responsiveness | Works on 1280px+ screens |
| Data privacy | All data stays local (no external API calls) |
| Extensibility | CSV upload allows new data without code changes |

## 9. Future Enhancements

- [ ] Twilio/WhatsApp API integration for real SMS delivery
- [ ] PDF report generation with charts embedded
- [ ] Multi-year comparison (academic year selector)
- [ ] Teacher performance analytics tab
- [ ] Student photo upload and ID card generation
- [ ] Role-based access (Admin / Teacher / Parent views)
