# Power BI Implementation Guide

Step-by-step setup guide for importing this School BI Solution into Power BI Desktop.

---

## Step 1: Get Data

1. Open **Power BI Desktop** → **Home** → **Get Data** → **Text/CSV**
2. Import these files in order:

| File | Table Name |
|---|---|
| `Students_Master_Table.csv` | Dim_Students |
| `Teacher_Table.csv` | Dim_Teachers |
| `Exam_Results_Table.csv` | Fact_ExamResults |
| `Attendance_Table.csv` | Fact_Attendance |
| `Fee_Collection_Table.csv` | Fact_Fees |
| `Dropout_Log.csv` | Dropout_Log |
| `Transfer_Log.csv` | Transfer_Log |
| `MidYear_Admissions.csv` | MidYear_Admissions |
| `Parent_Survey_Table.csv` | Parent_Survey |
| `School_Comparison_Table.csv` | School_Comparison |

---

## Step 2: Create Dimension Tables (Power Query)

### Dim_Subject
```
Home → Enter Data → Create manually:
Subject_Key | Subject_Name
1           | Urdu
2           | English
3           | Science
4           | Math
5           | Geography
6           | Social Studies
7           | Islamiat
8           | Computer
```

### Dim_Class
```
Home → Enter Data:
Class_Key | Class_Number | Class_Label | Class_Level
1         | 1            | Class 1     | Primary
2         | 2            | Class 2     | Primary
...
9         | 9            | Class 9     | Secondary
10        | 10           | Class 10    | Secondary
```

### Dim_Section
```
Home → Enter Data:
Section_Key | Section_Name
1           | A
2           | B
```

### Dim_Date
```
Home → Enter Data:
Date_Key | Month_Name | Month_Number | Academic_Year | Academic_Quarter | Sort_Order
202504   | April      | 4            | 2025-2026     | Q1               | 1
202505   | May        | 5            | 2025-2026     | Q1               | 2
202508   | August     | 8            | 2025-2026     | Q1               | 3
...
202603   | March      | 3            | 2025-2026     | Q4               | 10
```

---

## Step 3: Create Relationships (Model View)

Go to **Model View** → drag and drop to create these relationships:

| From | To | Key | Cardinality |
|---|---|---|---|
| Fact_ExamResults.Student_ID | Dim_Students.Student_ID | FK → PK | Many:1 |
| Fact_ExamResults.Subject | Dim_Subject.Subject_Name | FK → PK | Many:1 |
| Fact_ExamResults.Month | Dim_Date.Month_Name | FK → PK | Many:1 |
| Fact_ExamResults.Class | Dim_Class.Class_Number | FK → PK | Many:1 |
| Fact_ExamResults.Section | Dim_Section.Section_Name | FK → PK | Many:1 |
| Fact_Attendance.Student_ID | Dim_Students.Student_ID | FK → PK | Many:1 |
| Fact_Attendance.Month | Dim_Date.Month_Name | FK → PK | Many:1 |
| Fact_Fees.Student_ID | Dim_Students.Student_ID | FK → PK | Many:1 |
| Fact_Fees.Month | Dim_Date.Month_Name | FK → PK | Many:1 |
| Parent_Survey.Student_ID | Dim_Students.Student_ID | FK → PK | Many:1 |

> **Important:** Set all relationship directions to **Single (Dimension → Fact)**. Set cross-filter to **Single direction**.

---

## Step 4: Add Calculated Columns

Go to **Data View** → select the table → **New Column** for each:

1. Select **Fact_ExamResults** table, add columns from `DAX_Measures_Library.dax` Section 7 (items 7.1 through 7.6)
2. Select **Fact_Fees** table, add columns 7.7 and 7.8
3. Select **Fact_Attendance** table, add column 7.10
4. Select **Dim_Date** table, add columns 7.12 and 7.13

---

## Step 5: Add DAX Measures

1. **Home** → **New Measure** (or create a Measures table: `Modeling → New Table → _Measures = ROW("x", 0)`)
2. Add all measures from `DAX_Measures_Library.dax` Sections 1–6
3. Organize into Display Folders:
   - Academic KPIs
   - Attendance KPIs
   - Financial KPIs
   - Survey KPIs
   - Ranking KPIs
   - Dropout KPIs

---

## Step 6: Build Dashboard Pages

Follow `Dashboard_Wireframe.md` to build 4 pages:

1. **Executive Overview** – KPI cards, trend line, donut, bar chart, matrix
2. **Academic Analytics** – Subject heatmap, class comparison, top/bottom students
3. **Attendance Insights** – Trend, category donut, scatter plot, risk table
4. **Financial Dashboard** – Revenue trend, paid/unpaid bars, scholarship waterfall

### Page Setup
- Canvas size: **16:9 (1280×720)**
- Theme: Import custom JSON with Navy Blue (`#1B2A4A`) primary
- Background: Light Gray (`#F5F6FA`)

---

## Step 7: Add Interactivity

1. **Slicers**: Add Academic Year, Class, Section, Month to top bar of each page
2. **Drill-through**: Right-click any student/class → drill-through to detail page
3. **Bookmarks**: Create "Overview", "At-Risk", "Fee Focus" bookmarks
4. **Tooltips**: Create tooltip page with student detail card
5. **Navigation**: Add page navigation buttons with icons

---

## Step 8: Publish & Share

1. **File → Publish** → select your Power BI workspace
2. Set up **Scheduled Refresh** if connecting to a live database
3. Create a **Power BI App** for stakeholder distribution
4. Enable **Row-Level Security (RLS)** if needed per section/class

---

## Files Index

| File | Part | Description |
|---|---|---|
| `School_BI_Data_Model.md` | 1 | Star Schema documentation |
| `DAX_Measures_Library.dax` | 2, 3 | 50+ DAX measures + calculated columns |
| `SQL_Schema_and_Queries.sql` | 4 | SQL Server schema + analytical queries |
| `Dashboard_Wireframe.md` | 5 | 4-page wireframe with UX design |
| `generate_simulation_data.py` | 6 | Dropout & transfer data generator |
| `Dropout_Log.csv` | 6 | 42 dropout records |
| `Transfer_Log.csv` | 6 | 19 transfer records |
| `MidYear_Admissions.csv` | 6 | 10 mid-year admission records |
| `generate_survey_data.py` | 7 | Parent survey data generator |
| `Parent_Survey_Table.csv` | 7 | 610 parent survey responses |
| `generate_school_comparison.py` | 8 | School comparison data generator |
| `School_Comparison_Table.csv` | 8 | 5-school ranking comparison |
| `PowerBI_Implementation_Guide.md` | Final | This guide |
