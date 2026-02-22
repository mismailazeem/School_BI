"""
School BI Solution – Part 7: Parent Satisfaction Survey Data
Generates: Parent_Survey_Table.csv
"""

import pandas as pd
import numpy as np
import os

np.random.seed(42)

BASE_DIR = r"C:\Users\hp\Downloads\Schhol_Dashboard"

# Load student data for linking
students = pd.read_csv(os.path.join(BASE_DIR, "Students_Master_Table.csv"))

# Generate survey responses correlated with performance category
survey_data = []

for _, student in students.iterrows():
    perf = student["Performance_Category"]
    
    # Base ratings influenced by performance category
    if perf == "High":
        base_teaching = np.random.choice([4, 5], p=[0.3, 0.7])
        base_discipline = np.random.choice([3, 4, 5], p=[0.1, 0.3, 0.6])
        base_comm = np.random.choice([3, 4, 5], p=[0.15, 0.35, 0.5])
        base_fee = np.random.choice([3, 4, 5], p=[0.2, 0.4, 0.4])
        nps_base = np.random.choice(range(7, 11), p=[0.1, 0.2, 0.3, 0.4])
    elif perf == "Average":
        base_teaching = np.random.choice([2, 3, 4, 5], p=[0.05, 0.30, 0.45, 0.20])
        base_discipline = np.random.choice([2, 3, 4, 5], p=[0.10, 0.30, 0.40, 0.20])
        base_comm = np.random.choice([2, 3, 4], p=[0.15, 0.45, 0.40])
        base_fee = np.random.choice([2, 3, 4], p=[0.20, 0.50, 0.30])
        nps_base = np.random.choice(range(5, 10), p=[0.10, 0.20, 0.30, 0.25, 0.15])
    else:  # Low
        base_teaching = np.random.choice([1, 2, 3, 4], p=[0.10, 0.35, 0.40, 0.15])
        base_discipline = np.random.choice([1, 2, 3, 4], p=[0.15, 0.30, 0.35, 0.20])
        base_comm = np.random.choice([1, 2, 3], p=[0.25, 0.45, 0.30])
        base_fee = np.random.choice([1, 2, 3], p=[0.30, 0.45, 0.25])
        nps_base = np.random.choice(range(1, 8), p=[0.10, 0.15, 0.20, 0.20, 0.15, 0.10, 0.10])
    
    # Fee satisfaction also influenced by fee status
    if student["Fee_Status"] == "Unpaid":
        base_fee = max(1, base_fee - np.random.choice([0, 1], p=[0.4, 0.6]))
    
    # Scholarship holders tend to rate fee satisfaction higher
    if student["Scholarship"] == "Yes":
        base_fee = min(5, base_fee + np.random.choice([0, 1], p=[0.5, 0.5]))
    
    # Overall satisfaction = average of 4 ratings
    overall = round((base_teaching + base_discipline + base_comm + base_fee) / 4, 2)
    
    survey_data.append({
        "Student_ID": student["Student_ID"],
        "Teaching_Quality_Rating": int(base_teaching),
        "Discipline_Rating": int(base_discipline),
        "Communication_Rating": int(base_comm),
        "Fee_Satisfaction": int(base_fee),
        "Overall_Satisfaction": overall,
        "Recommendation_Score": int(nps_base)
    })

survey_df = pd.DataFrame(survey_data)

# Ensure all ratings are within 1-5 and NPS within 0-10
survey_df["Teaching_Quality_Rating"] = survey_df["Teaching_Quality_Rating"].clip(1, 5)
survey_df["Discipline_Rating"] = survey_df["Discipline_Rating"].clip(1, 5)
survey_df["Communication_Rating"] = survey_df["Communication_Rating"].clip(1, 5)
survey_df["Fee_Satisfaction"] = survey_df["Fee_Satisfaction"].clip(1, 5)
survey_df["Recommendation_Score"] = survey_df["Recommendation_Score"].clip(0, 10)

# Save
survey_df.to_csv(os.path.join(BASE_DIR, "Parent_Survey_Table.csv"), index=False)

# Print summary
print(f"[OK] Parent_Survey_Table.csv created: {len(survey_df)} rows")
print(f"\n--- Survey Summary ---")
print(f"Teaching Quality Avg: {survey_df['Teaching_Quality_Rating'].mean():.2f}")
print(f"Discipline Avg:       {survey_df['Discipline_Rating'].mean():.2f}")
print(f"Communication Avg:    {survey_df['Communication_Rating'].mean():.2f}")
print(f"Fee Satisfaction Avg: {survey_df['Fee_Satisfaction'].mean():.2f}")
print(f"Overall Satisfaction: {survey_df['Overall_Satisfaction'].mean():.2f}")
print(f"Recommendation Avg:   {survey_df['Recommendation_Score'].mean():.2f}")

# NPS Calculation
promoters = len(survey_df[survey_df["Recommendation_Score"] >= 9])
detractors = len(survey_df[survey_df["Recommendation_Score"] <= 6])
nps = (promoters - detractors) / len(survey_df) * 100
print(f"\n--- NPS Score ---")
print(f"Promoters (9-10): {promoters} ({promoters/len(survey_df)*100:.1f}%)")
print(f"Passives (7-8):   {len(survey_df) - promoters - detractors}")
print(f"Detractors (0-6): {detractors} ({detractors/len(survey_df)*100:.1f}%)")
print(f"NPS Score:        {nps:.1f}")

print("\n[DONE] Part 7: Parent Satisfaction Survey complete!")
