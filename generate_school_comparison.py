"""
School BI Solution – Part 8: School Ranking Comparison Dataset
Generates: School_Comparison_Table.csv
"""

import pandas as pd
import numpy as np
import os

np.random.seed(42)

BASE_DIR = r"C:\Users\hp\Downloads\Schhol_Dashboard"

# Simulate 5 schools with realistic Pakistani school metrics
schools = [
    {
        "School_Name": "Al-Noor Academy",
        "Total_Students": 611,  # Our school
        "Average_Result_Pct": None,  # Will compute from actual data
        "Board_Result_Pct": None,
        "Fee_Revenue": None,
        "Teacher_Student_Ratio": None,
        "Satisfaction_Index": None,
        "Attendance_Average": None,
    },
    {
        "School_Name": "City Grammar School",
        "Total_Students": np.random.randint(450, 700),
        "Average_Result_Pct": round(np.random.uniform(55, 75), 2),
        "Board_Result_Pct": round(np.random.uniform(60, 85), 2),
        "Fee_Revenue": round(np.random.uniform(8000000, 20000000), 2),
        "Teacher_Student_Ratio": round(np.random.uniform(6, 12), 1),
        "Satisfaction_Index": round(np.random.uniform(2.5, 4.5), 2),
        "Attendance_Average": round(np.random.uniform(70, 90), 2),
    },
    {
        "School_Name": "Pakistan International School",
        "Total_Students": np.random.randint(500, 800),
        "Average_Result_Pct": round(np.random.uniform(60, 80), 2),
        "Board_Result_Pct": round(np.random.uniform(65, 90), 2),
        "Fee_Revenue": round(np.random.uniform(10000000, 25000000), 2),
        "Teacher_Student_Ratio": round(np.random.uniform(5, 10), 1),
        "Satisfaction_Index": round(np.random.uniform(3.0, 4.8), 2),
        "Attendance_Average": round(np.random.uniform(75, 92), 2),
    },
    {
        "School_Name": "Crescent Model School",
        "Total_Students": np.random.randint(350, 550),
        "Average_Result_Pct": round(np.random.uniform(50, 68), 2),
        "Board_Result_Pct": round(np.random.uniform(55, 78), 2),
        "Fee_Revenue": round(np.random.uniform(5000000, 15000000), 2),
        "Teacher_Student_Ratio": round(np.random.uniform(8, 15), 1),
        "Satisfaction_Index": round(np.random.uniform(2.0, 3.8), 2),
        "Attendance_Average": round(np.random.uniform(65, 82), 2),
    },
    {
        "School_Name": "Iqbal Public School",
        "Total_Students": np.random.randint(400, 650),
        "Average_Result_Pct": round(np.random.uniform(52, 72), 2),
        "Board_Result_Pct": round(np.random.uniform(58, 82), 2),
        "Fee_Revenue": round(np.random.uniform(6000000, 18000000), 2),
        "Teacher_Student_Ratio": round(np.random.uniform(7, 14), 1),
        "Satisfaction_Index": round(np.random.uniform(2.3, 4.2), 2),
        "Attendance_Average": round(np.random.uniform(68, 88), 2),
    }
]

# Compute actual metrics for "our" school (Al-Noor Academy)
exams = pd.read_csv(os.path.join(BASE_DIR, "Exam_Results_Table.csv"))
attendance = pd.read_csv(os.path.join(BASE_DIR, "Attendance_Table.csv"))
fees = pd.read_csv(os.path.join(BASE_DIR, "Fee_Collection_Table.csv"))

exams["Total"] = exams["Monthly_Test_50"] + exams["Midterm_100"] + exams["Final_100"]
exams["Percentage"] = exams["Total"] / 250 * 100

our_avg_result = round(exams["Percentage"].mean(), 2)
our_board_result = round(exams[exams["Class"].isin([9, 10])]["Percentage"].mean(), 2)
our_attendance = round(attendance["Attendance_Percentage"].mean(), 2)
our_revenue = round(fees["Amount_Paid"].sum(), 2)
our_tsr = round(611 / 80, 1)  # 611 students, 80 teachers

# Try to load survey if exists, otherwise estimate
survey_path = os.path.join(BASE_DIR, "Parent_Survey_Table.csv")
if os.path.exists(survey_path):
    survey = pd.read_csv(survey_path)
    our_satisfaction = round(survey["Overall_Satisfaction"].mean(), 2)
else:
    our_satisfaction = 3.45  # Estimated

schools[0]["Average_Result_Pct"] = our_avg_result
schools[0]["Board_Result_Pct"] = our_board_result
schools[0]["Fee_Revenue"] = our_revenue
schools[0]["Teacher_Student_Ratio"] = our_tsr
schools[0]["Satisfaction_Index"] = our_satisfaction
schools[0]["Attendance_Average"] = our_attendance

# Create DataFrame
comparison_df = pd.DataFrame(schools)

# Calculate Weighted Ranking Score
# Weights: 40% Academic, 20% Attendance, 20% Revenue Stability, 20% Parent Satisfaction
max_revenue = comparison_df["Fee_Revenue"].max()

comparison_df["Academic_Score"] = comparison_df["Average_Result_Pct"] * 0.40
comparison_df["Attendance_Score"] = comparison_df["Attendance_Average"] * 0.20
comparison_df["Revenue_Score"] = (comparison_df["Fee_Revenue"] / max_revenue * 100) * 0.20
comparison_df["Satisfaction_Score"] = (comparison_df["Satisfaction_Index"] * 20) * 0.20  # Scale 1-5 to 0-100
comparison_df["Ranking_Score"] = round(
    comparison_df["Academic_Score"] + 
    comparison_df["Attendance_Score"] + 
    comparison_df["Revenue_Score"] + 
    comparison_df["Satisfaction_Score"], 
    2
)

# Remove intermediate columns for clean output
output_df = comparison_df[[
    "School_Name", "Total_Students", "Average_Result_Pct", "Board_Result_Pct",
    "Fee_Revenue", "Teacher_Student_Ratio", "Satisfaction_Index",
    "Attendance_Average", "Ranking_Score"
]].copy()

output_df = output_df.sort_values("Ranking_Score", ascending=False).reset_index(drop=True)
output_df.index = output_df.index + 1
output_df.index.name = "Rank"

# Save
output_df.to_csv(os.path.join(BASE_DIR, "School_Comparison_Table.csv"))

print("[OK] School_Comparison_Table.csv created: 5 schools")
print(f"\n--- School Rankings ---")
print(output_df.to_string())
print(f"\n--- Ranking Formula ---")
print("Weighted Score = 40% × Academic + 20% × Attendance + 20% × Revenue_Normalized + 20% × Satisfaction_Scaled")

print("\n[DONE] Part 8: School Ranking Comparison complete!")
