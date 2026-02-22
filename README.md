# 🎓 School BI Dashboard

> Interactive Business Intelligence platform for Pakistani school systems — Academics, Attendance, Finance & Parent Engagement analytics in one place.

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.54-FF4B4B?logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-6.x-3F4F75?logo=plotly)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

| Feature | Description |
|---|---|
| 📊 **7-Tab Dashboard** | Executive, Academic, Attendance, Financial, Student Lookup, Upload, Rankings |
| 🌙 **Dark/Light Mode** | Toggle between themes with 30+ CSS variables |
| 🔎 **Student Lookup** | Search by ID → profile card, 4-panel progress chart, progress bars |
| 💾 **Export Reports** | Download as PNG, JPEG, SVG, PDF, or HTML |
| 📱 **Parent Notification** | SMS-ready message templates for progress reports |
| 📤 **CSV Upload** | Upload your own data to dynamically refresh the dashboard |
| 🎯 **Smart Filters** | Filter by Class, Section, Month, Gender across all tabs |

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/school-bi-dashboard.git
cd school-bi-dashboard

# Install dependencies
pip install streamlit plotly pandas numpy

# Optional: for image export
pip install kaleido
```

### Run the Dashboard

```bash
streamlit run app.py --server.headless true --server.port 8510
```

Open **http://localhost:8510** in your browser.

### Generate Additional Data (Optional)

```bash
python generate_simulation_data.py    # Dropout/Transfer logs
python generate_survey_data.py        # Parent satisfaction survey
python generate_school_comparison.py  # School ranking comparison
```

## 📁 Project Structure

```
school-bi-dashboard/
│
├── app.py                          # Main dashboard application
├── dashboard_utils.py              # Theme engine & helper functions
├── PRD.md                          # Product Requirements Document
├── README.md                       # This file
│
├── 📄 Source Data
│   ├── Students_Master_Table.csv   # 611 students (Classes 1-10, Sections A/B)
│   ├── Exam_Results_Table.csv      # ~48,801 exam records (long format)
│   ├── Attendance_Table.csv        # ~6,101 monthly attendance records
│   ├── Fee_Collection_Table.csv    # ~6,101 fee payment records
│   └── Teacher_Table.csv           # 80 teacher assignments
│
├── 🔧 Data Generators
│   ├── generate_simulation_data.py # Dropout & transfer simulation
│   ├── generate_survey_data.py     # Parent satisfaction survey
│   └── generate_school_comparison.py # School ranking comparison
│
├── 📊 Generated Datasets
│   ├── Dropout_Log.csv             # 42 risk-scored dropouts
│   ├── Transfer_Log.csv            # 19 section transfers
│   ├── MidYear_Admissions.csv      # 10 new admissions
│   ├── Parent_Survey_Table.csv     # 610 survey responses
│   └── School_Comparison_Table.csv # 5-school ranking
│
└── 📘 Documentation
    ├── School_BI_Data_Model.md     # Star Schema (6 dims, 3 facts)
    ├── DAX_Measures_Library.dax    # 50+ Power BI DAX measures
    ├── SQL_Schema_and_Queries.sql  # T-SQL schema & analytical queries
    ├── Dashboard_Wireframe.md      # 4-page UX wireframe
    └── PowerBI_Implementation_Guide.md
```

## 📊 Dashboard Pages

### 🏠 Executive Overview
6 KPI cards (Students, Revenue, Academic %, Attendance, Pass Rate, Fee Collection) with monthly trend line, fee donut chart, gender distribution, and class-level quick stats.

### 📊 Academic Analytics
Subject × Month performance heatmap, Section A vs B comparison, top/bottom 5 student rankings, monthly score trend with area fill, and grade distribution (A+ through F).

### 📋 Attendance Insights
At-risk student identification (<75%), monthly attendance trend by section with 75% threshold line, attendance category donut, scatter plot with Pearson correlation coefficient, and at-risk student table.

### 💰 Financial Dashboard
Revenue expected vs collected combo chart with collection rate overlay, payment status by class, class-wise revenue horizontal bars, and fee defaulter list (≥3 unpaid months).

### 🔎 Student Lookup
- Search by Student ID
- Profile card with academic average, guardian info, fee/scholarship status
- Visual progress bars for academics, attendance, and fee payment
- 4-panel chart: Monthly exam trend, Attendance bars, Subject-wise bars, Fee pie
- **Export:** Download report as PNG / JPEG / SVG / PDF / HTML
- **Parent SMS:** Enter contact number, choose message template, preview message

### 📤 Upload Data
Upload your own CSV files to replace dashboard data on-the-fly. Supports Students, Exams, Attendance, Fees, and Teachers datasets with preview and validation.

### 📈 Rankings & Survey
School comparison ranking (weighted: 40% Academic + 20% Attendance + 20% Revenue + 20% Satisfaction), parent satisfaction by category, NPS score distribution, and dropout analysis.

## 🎨 Theming

Toggle between **Light** and **Dark** mode via the sidebar switch:

| Element | Light | Dark |
|---|---|---|
| Background | `#F5F6FA` gradient | `#0F172A` gradient |
| Cards | White `#FFFFFF` | Slate `#1E293B` |
| Primary | Navy `#1B2A4A` | Blue `#60A5FA` |
| Accent | Teal `#00B2A9` | Emerald `#34D399` |

## 🗄️ Data Model

Star Schema architecture with **6 dimension tables** and **3 fact tables**:

- **Dimensions:** Student, Subject, Month, Teacher, School, Survey Response
- **Facts:** Exam Results, Attendance, Fee Collection

See [School_BI_Data_Model.md](School_BI_Data_Model.md) for the complete schema.

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Framework | Streamlit 1.54+ |
| Charts | Plotly 6.x |
| Data Processing | Pandas, NumPy |
| Image Export | Kaleido (optional) |
| Styling | Custom CSS with CSS variables |
| Font | Inter (Google Fonts) |

## 📋 Power BI Alternative

This project also includes full **Power BI** implementation artifacts:
- `DAX_Measures_Library.dax` — 50+ DAX measures + 13 calculated columns
- `SQL_Schema_and_Queries.sql` — Complete T-SQL schema
- `PowerBI_Implementation_Guide.md` — Step-by-step .pbix setup guide

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-analytics`)
3. Commit changes (`git commit -m 'Add teacher analytics tab'`)
4. Push to branch (`git push origin feature/new-analytics`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

---

<p align="center">Built with ❤️ for Pakistani Schools</p>
