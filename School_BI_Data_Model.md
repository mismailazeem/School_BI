# School BI Star Schema – Data Model Documentation

## 1. Model Overview

This document defines an enterprise-grade **Star Schema** data model for a Pakistani School System (Classes 1–10, Sections A & B). The model separates raw CSV data into clearly defined **Dimension** and **Fact** tables optimized for Power BI analytical queries.

---

## 2. Visual Model Diagram (Textual)

```
                    ┌──────────────┐
                    │  Dim_Date    │
                    │──────────────│
                    │ Date_Key (PK)│
                    │ Month        │
                    │ Month_Number │
                    │ Academic_Year│
                    │ Quarter      │
                    │ Is_Exam_Month│
                    └──────┬───────┘
                           │
           ┌───────────────┼────────────────┐
           │               │                │
           │ 1:M           │ 1:M            │ 1:M
           ▼               ▼                ▼
┌─────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ Fact_ExamResults │ │ Fact_Attendance  │ │ Fact_Fees        │
│─────────────────│ │──────────────────│ │──────────────────│
│ ExamResult_Key  │ │ Attendance_Key   │ │ Fee_Key (PK)     │
│ Student_Key(FK) │ │ Student_Key (FK) │ │ Student_Key (FK) │
│ Subject_Key(FK) │ │ Date_Key (FK)    │ │ Date_Key (FK)    │
│ Date_Key (FK)   │ │ Class_Key (FK)   │ │ Class_Key (FK)   │
│ Class_Key (FK)  │ │ Section_Key (FK) │ │ Section_Key (FK) │
│ Section_Key(FK) │ │ Attendance_%     │ │ Monthly_Fee      │
│ Monthly_Test    │ └──────────────────┘ │ Amount_Paid      │
│ Midterm_Score   │                      │ Payment_Status   │
│ Final_Score     │                      │ Outstanding_Amt  │
└────────┬────────┘                      └────────┬─────────┘
         │                                        │
         │         ┌──────────────┐               │
         │         │ Dim_Students │               │
         │         │──────────────│               │
         ├────────►│ Student_Key  │◄──────────────┤
         │         │ Student_ID   │               │
         │         │ Student_Name │               │
         │         │ Gender       │               │
         │         │ DOB          │               │
         │         │ Guardian_Name│               │
         │         │ Admission_Dt │               │
         │         │ Roll_Number  │               │
         │         │ Fee_Status   │               │
         │         │ Scholarship  │               │
         │         │ Perf_Category│               │
         │         └──────────────┘               │
         │                                        │
         │         ┌──────────────┐               │
         │         │ Dim_Class    │               │
         ├────────►│──────────────│◄──────────────┤
         │         │ Class_Key(PK)│
         │         │ Class_Number │
         │         │ Class_Label  │
         │         └──────────────┘
         │
         │         ┌──────────────┐
         ├────────►│ Dim_Section  │
         │         │──────────────│
         │         │Section_Key   │
         │         │Section_Name  │
         │         └──────────────┘
         │
         │         ┌──────────────┐
         └────────►│ Dim_Subject  │
                   │──────────────│
                   │Subject_Key   │
                   │Subject_Name  │
                   │Max_Monthly   │
                   │Max_Midterm   │
                   │Max_Final     │
                   └──────────────┘

         ┌──────────────┐
         │ Dim_Teachers │
         │──────────────│
         │ Teacher_Key  │
         │ Teacher_ID   │
         │ Teacher_Name │
         │ Subject (FK) │
         │ Class_Assign │
         │ Section      │
         └──────────────┘
```

---

## 3. Dimension Tables

### 3.1 Dim_Students

| Column | Type | Description |
|---|---|---|
| **Student_Key** (PK) | INT IDENTITY | Surrogate key |
| Student_ID | INT | Natural key from CSV |
| Student_Name | NVARCHAR(100) | Full name |
| Gender | NVARCHAR(10) | Male / Female |
| Date_of_Birth | DATE | DOB |
| Class | INT | Current class (1–10) |
| Section | CHAR(1) | A or B |
| Admission_Date | DATE | Date of admission |
| Roll_Number | NVARCHAR(20) | Roll number |
| Guardian_Name | NVARCHAR(100) | Parent/Guardian |
| Guardian_Contact | NVARCHAR(15) | Contact number |
| Fee_Status | NVARCHAR(10) | Paid / Unpaid |
| Scholarship | NVARCHAR(5) | Yes / No |
| Performance_Category | NVARCHAR(10) | High / Average / Low |

> **Source:** `Students_Master_Table.csv`

### 3.2 Dim_Teachers

| Column | Type | Description |
|---|---|---|
| **Teacher_Key** (PK) | INT IDENTITY | Surrogate key |
| Teacher_ID | INT | Natural key |
| Teacher_Name | NVARCHAR(100) | Full name |
| Subject | NVARCHAR(30) | Subject taught |
| Class_Assigned | INT | Class assigned (1–10) |
| Section | CHAR(1) | Section (A/B) |

> **Source:** `Teacher_Table.csv`

### 3.3 Dim_Subject

| Column | Type | Description |
|---|---|---|
| **Subject_Key** (PK) | INT IDENTITY | Surrogate key |
| Subject_Name | NVARCHAR(30) | Subject name |
| Max_Monthly_Test | INT | 50 |
| Max_Midterm | INT | 100 |
| Max_Final | INT | 100 |
| Max_Total | INT | 250 |

> **Subjects:** Urdu, English, Science, Math, Geography, Social Studies, Islamiat, Computer

### 3.4 Dim_Class

| Column | Type | Description |
|---|---|---|
| **Class_Key** (PK) | INT IDENTITY | Surrogate key |
| Class_Number | INT | Class (1–10) |
| Class_Label | NVARCHAR(20) | e.g., "Class 1" |
| Class_Level | NVARCHAR(20) | Primary (1-5) / Middle (6-8) / Secondary (9-10) |

### 3.5 Dim_Section

| Column | Type | Description |
|---|---|---|
| **Section_Key** (PK) | INT IDENTITY | Surrogate key |
| Section_Name | CHAR(1) | A or B |

### 3.6 Dim_Date

| Column | Type | Description |
|---|---|---|
| **Date_Key** (PK) | INT | YYYYMM format (e.g., 202504) |
| Month_Name | NVARCHAR(15) | April, May, etc. |
| Month_Number | INT | 1–12 |
| Academic_Year | NVARCHAR(10) | "2025-2026" |
| Academic_Quarter | NVARCHAR(5) | Q1/Q2/Q3/Q4 |
| Is_Exam_Month | BIT | Flag for exam months |
| Sort_Order | INT | Academic year sort (April=1, March=10) |

> **Academic Calendar:** April → March, excluding June & July (10 active months)

---

## 4. Fact Tables

### 4.1 Fact_ExamResults

| Column | Type | Description |
|---|---|---|
| **ExamResult_Key** (PK) | BIGINT IDENTITY | Surrogate key |
| Student_Key (FK) | INT | → Dim_Students |
| Subject_Key (FK) | INT | → Dim_Subject |
| Date_Key (FK) | INT | → Dim_Date |
| Class_Key (FK) | INT | → Dim_Class |
| Section_Key (FK) | INT | → Dim_Section |
| Monthly_Test_Score | INT | Score out of 50 |
| Midterm_Score | INT | Score out of 100 |
| Final_Score | INT | Score out of 100 |
| Total_Score | INT | Calculated: Sum of all three |
| Percentage | DECIMAL(5,2) | (Total/250)*100 |

> **Source:** `Exam_Results_Table.csv` · ~48,800 rows
> **Grain:** One row per Student × Subject × Month

### 4.2 Fact_Attendance

| Column | Type | Description |
|---|---|---|
| **Attendance_Key** (PK) | BIGINT IDENTITY | Surrogate key |
| Student_Key (FK) | INT | → Dim_Students |
| Date_Key (FK) | INT | → Dim_Date |
| Class_Key (FK) | INT | → Dim_Class |
| Section_Key (FK) | INT | → Dim_Section |
| Attendance_Percentage | DECIMAL(5,2) | Monthly attendance % |

> **Source:** `Attendance_Table.csv` · ~6,100 rows
> **Grain:** One row per Student × Month

### 4.3 Fact_Fees

| Column | Type | Description |
|---|---|---|
| **Fee_Key** (PK) | BIGINT IDENTITY | Surrogate key |
| Student_Key (FK) | INT | → Dim_Students |
| Date_Key (FK) | INT | → Dim_Date |
| Class_Key (FK) | INT | → Dim_Class |
| Section_Key (FK) | INT | → Dim_Section |
| Monthly_Fee | DECIMAL(10,2) | Expected fee |
| Amount_Paid | DECIMAL(10,2) | Actual paid |
| Outstanding_Amount | DECIMAL(10,2) | Monthly_Fee − Amount_Paid |
| Payment_Status | NVARCHAR(10) | Paid / Unpaid |

> **Source:** `Fee_Collection_Table.csv` · ~6,100 rows
> **Grain:** One row per Student × Month

---

## 5. Relationships

| From (Fact) | To (Dimension) | Key | Cardinality | Direction | Cross-Filter |
|---|---|---|---|---|---|
| Fact_ExamResults.Student_Key | Dim_Students.Student_Key | FK → PK | Many-to-One | Single | Dim → Fact |
| Fact_ExamResults.Subject_Key | Dim_Subject.Subject_Key | FK → PK | Many-to-One | Single | Dim → Fact |
| Fact_ExamResults.Date_Key | Dim_Date.Date_Key | FK → PK | Many-to-One | Single | Dim → Fact |
| Fact_ExamResults.Class_Key | Dim_Class.Class_Key | FK → PK | Many-to-One | Single | Dim → Fact |
| Fact_ExamResults.Section_Key | Dim_Section.Section_Key | FK → PK | Many-to-One | Single | Dim → Fact |
| Fact_Attendance.Student_Key | Dim_Students.Student_Key | FK → PK | Many-to-One | Single | Dim → Fact |
| Fact_Attendance.Date_Key | Dim_Date.Date_Key | FK → PK | Many-to-One | Single | Dim → Fact |
| Fact_Attendance.Class_Key | Dim_Class.Class_Key | FK → PK | Many-to-One | Single | Dim → Fact |
| Fact_Attendance.Section_Key | Dim_Section.Section_Key | FK → PK | Many-to-One | Single | Dim → Fact |
| Fact_Fees.Student_Key | Dim_Students.Student_Key | FK → PK | Many-to-One | Single | Dim → Fact |
| Fact_Fees.Date_Key | Dim_Date.Date_Key | FK → PK | Many-to-One | Single | Dim → Fact |
| Fact_Fees.Class_Key | Dim_Class.Class_Key | FK → PK | Many-to-One | Single | Dim → Fact |
| Fact_Fees.Section_Key | Dim_Section.Section_Key | FK → PK | Many-to-One | Single | Dim → Fact |
| Dim_Teachers.Subject | Dim_Subject.Subject_Name | Logical | Many-to-One | Single | — |
| Dim_Teachers.Class_Assigned | Dim_Class.Class_Number | Logical | Many-to-One | Single | — |

> **Snowflake Adjustment:** Dim_Teachers is NOT directly connected to any fact table. It connects via Dim_Subject + Dim_Class for teacher-performance analysis. Use `TREATAS()` or bridge table in Power BI if drill-through to teacher-level is needed.

---

## 6. Design Decisions

### 6.1 Surrogate Keys
All dimension tables use INT IDENTITY surrogate keys instead of natural keys. This enables:
- Slowly Changing Dimensions (SCD Type 2) if student data changes
- Efficient join performance in Power BI VertiPaq engine
- Decoupling from source system IDs

### 6.2 Degenerate Dimensions
Month is not stored as a degenerate dimension in fact tables — instead, a proper `Dim_Date` table is used with academic calendar awareness (April=Q1 start).

### 6.3 Conformed Dimensions
`Dim_Students`, `Dim_Class`, `Dim_Section`, and `Dim_Date` are **conformed dimensions** shared across all three fact tables, enabling cross-domain analysis (e.g., Attendance vs. Performance correlation).

### 6.4 Snowflake Consideration
The model is a **pure star schema** with no snowflaking. `Dim_Teachers` stands independently and is linked logically through Subject + Class for reporting purposes. This keeps the model simple and performant in Power BI's in-memory engine.

---

## 7. Row Count Estimates

| Table | Estimated Rows |
|---|---|
| Dim_Students | 611 |
| Dim_Teachers | 80 |
| Dim_Subject | 8 |
| Dim_Class | 10 |
| Dim_Section | 2 |
| Dim_Date | 10 (active months) |
| Fact_ExamResults | ~48,800 |
| Fact_Attendance | ~6,100 |
| Fact_Fees | ~6,100 |
