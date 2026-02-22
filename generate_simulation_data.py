"""
School BI Solution – Part 6: Dropout & Transfer Simulation
Generates: Dropout_Log.csv, Transfer_Log.csv
"""

import pandas as pd
import random
import os

random.seed(42)

BASE_DIR = r"C:\Users\hp\Downloads\Schhol_Dashboard"

# Load source data
students = pd.read_csv(os.path.join(BASE_DIR, "Students_Master_Table.csv"))
attendance = pd.read_csv(os.path.join(BASE_DIR, "Attendance_Table.csv"))
fees = pd.read_csv(os.path.join(BASE_DIR, "Fee_Collection_Table.csv"))
exams = pd.read_csv(os.path.join(BASE_DIR, "Exam_Results_Table.csv"))

# Calculate student-level metrics
student_att = attendance.groupby("Student_ID")["Attendance_Percentage"].mean().reset_index()
student_att.columns = ["Student_ID", "Avg_Attendance"]

student_perf = exams.copy()
student_perf["Total"] = student_perf["Monthly_Test_50"] + student_perf["Midterm_100"] + student_perf["Final_100"]
student_perf["Percentage"] = student_perf["Total"] / 250 * 100
student_perf_avg = student_perf.groupby("Student_ID")["Percentage"].mean().reset_index()
student_perf_avg.columns = ["Student_ID", "Avg_Performance"]

fee_default = fees[fees["Payment_Status"] == "Unpaid"].groupby("Student_ID").size().reset_index()
fee_default.columns = ["Student_ID", "Unpaid_Months"]

# Merge for risk analysis
risk_df = students[["Student_ID", "Student_Name", "Class", "Section"]].copy()
risk_df = risk_df.merge(student_att, on="Student_ID", how="left")
risk_df = risk_df.merge(student_perf_avg, on="Student_ID", how="left")
risk_df = risk_df.merge(fee_default, on="Student_ID", how="left")
risk_df["Unpaid_Months"] = risk_df["Unpaid_Months"].fillna(0).astype(int)

# Compute risk score (higher = more at risk)
risk_df["Risk_Score"] = 0
risk_df.loc[risk_df["Avg_Attendance"] < 70, "Risk_Score"] += 3
risk_df.loc[(risk_df["Avg_Attendance"] >= 70) & (risk_df["Avg_Attendance"] < 80), "Risk_Score"] += 1
risk_df.loc[risk_df["Avg_Performance"] < 40, "Risk_Score"] += 3
risk_df.loc[(risk_df["Avg_Performance"] >= 40) & (risk_df["Avg_Performance"] < 55), "Risk_Score"] += 1
risk_df.loc[risk_df["Unpaid_Months"] >= 5, "Risk_Score"] += 3
risk_df.loc[(risk_df["Unpaid_Months"] >= 3) & (risk_df["Unpaid_Months"] < 5), "Risk_Score"] += 1

# ── DROPOUT SIMULATION (5-8% rate) ────────────────────────
dropout_rate = random.uniform(0.05, 0.08)
num_dropouts = int(len(students) * dropout_rate)

# Prioritize highest-risk students for dropout
risk_sorted = risk_df.sort_values("Risk_Score", ascending=False)
dropout_candidates = risk_sorted.head(num_dropouts).copy()

months = ["August", "September", "October", "November", "December", "January", "February"]
reasons = [
    "Financial Constraints",
    "Family Relocation",
    "Health Issues",
    "Low Academic Performance",
    "Lack of Interest",
    "Family Decision",
    "Transportation Issues"
]

dropout_log = []
for _, row in dropout_candidates.iterrows():
    dropout_log.append({
        "Student_ID": row["Student_ID"],
        "Student_Name": row["Student_Name"],
        "Class": row["Class"],
        "Section": row["Section"],
        "Dropout_Month": random.choice(months),
        "Dropout_Reason": random.choice(reasons),
        "Last_Attendance_Pct": round(row["Avg_Attendance"], 2),
        "Last_Exam_Pct": round(row["Avg_Performance"], 2),
        "Fee_Default_Count": row["Unpaid_Months"],
        "Risk_Score": row["Risk_Score"]
    })

dropout_df = pd.DataFrame(dropout_log)
dropout_df.to_csv(os.path.join(BASE_DIR, "Dropout_Log.csv"), index=False)
print(f"[OK] Dropout_Log.csv created: {len(dropout_df)} students ({dropout_rate:.1%} dropout rate)")


# ── TRANSFER SIMULATION ──────────────────────────────────
# Transfer 3-5% of students between sections
transfer_rate = random.uniform(0.03, 0.05)
num_transfers = int(len(students) * transfer_rate)

# Select random non-dropout students
remaining = students[~students["Student_ID"].isin(dropout_df["Student_ID"])]
transfer_students = remaining.sample(n=min(num_transfers, len(remaining)), random_state=42)

transfer_reasons = [
    "Balancing Section Strength",
    "Parent Request",
    "Disciplinary Action",
    "Performance Optimization",
    "Teacher Recommendation",
    "Peer Group Adjustment"
]

transfer_log = []
for _, row in transfer_students.iterrows():
    from_section = row["Section"]
    to_section = "B" if from_section == "A" else "A"
    transfer_log.append({
        "Student_ID": row["Student_ID"],
        "Student_Name": row["Student_Name"],
        "Class": row["Class"],
        "From_Section": from_section,
        "To_Section": to_section,
        "Transfer_Month": random.choice(months),
        "Transfer_Reason": random.choice(transfer_reasons)
    })

transfer_df = pd.DataFrame(transfer_log)
transfer_df.to_csv(os.path.join(BASE_DIR, "Transfer_Log.csv"), index=False)
print(f"[OK] Transfer_Log.csv created: {len(transfer_df)} transfers ({transfer_rate:.1%} rate)")


# ── MID-YEAR ADMISSIONS ─────────────────────────────────
# Simulate 10-15 new mid-year admissions
num_new = random.randint(10, 15)
new_students = []
max_id = students["Student_ID"].max()

for i in range(num_new):
    sid = max_id + 1 + i
    cls = random.randint(1, 8)  # Mid-year usually lower classes
    sec = random.choice(["A", "B"])
    gender = random.choice(["Male", "Female"])
    admission_month = random.choice(["August", "September", "October", "November"])
    new_students.append({
        "Student_ID": sid,
        "Student_Name": f"Student_{sid}",
        "Gender": gender,
        "Class": cls,
        "Section": sec,
        "Admission_Month": admission_month,
        "Admission_Type": "Mid-Year Transfer",
        "Previous_School": f"School_{random.randint(1, 20)}"
    })

midyear_df = pd.DataFrame(new_students)
midyear_df.to_csv(os.path.join(BASE_DIR, "MidYear_Admissions.csv"), index=False)
print(f"[OK] MidYear_Admissions.csv created: {len(midyear_df)} new admissions")

print("\n[DONE] Part 6: Dropout & Transfer Simulation complete!")
