"""
Dashboard Utilities - Theme, KPI cards, helpers
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import io, base64

MONTH_ORDER = ["April", "May", "August", "September", "October",
               "November", "December", "January", "February", "March"]

GRADE_COLORS = {"A+": "#1abc9c", "A": "#2ecc71", "B": "#3498db",
                "C": "#f39c12", "D": "#e67e22", "F": "#e74c3c"}

LIGHT = {
    "primary": "#1B2A4A", "secondary": "#00B2A9", "success": "#2ECC71",
    "warning": "#F39C12", "danger": "#E74C3C", "purple": "#9B59B6",
    "blue_light": "#3498DB", "orange": "#E67E22",
    "bg": "#F5F6FA", "bg2": "#E8EAF0", "card": "#FFFFFF",
    "text": "#2C3E50", "text2": "#7F8C8D", "border": "rgba(27,42,74,0.06)",
    "shadow": "rgba(27,42,74,0.08)", "sidebar_bg": "linear-gradient(180deg,#1B2A4A,#0f1b33)",
    "sidebar_text": "white", "header_bg": "linear-gradient(135deg,#1B2A4A,#2c3e6d)",
    "grid": "rgba(0,0,0,0.05)", "plot_bg": "rgba(0,0,0,0)"
}

DARK = {
    "primary": "#60A5FA", "secondary": "#34D399", "success": "#4ADE80",
    "warning": "#FBBF24", "danger": "#F87171", "purple": "#C084FC",
    "blue_light": "#60A5FA", "orange": "#FB923C",
    "bg": "#0F172A", "bg2": "#1E293B", "card": "#1E293B",
    "text": "#F1F5F9", "text2": "#94A3B8", "border": "rgba(148,163,184,0.15)",
    "shadow": "rgba(0,0,0,0.3)", "sidebar_bg": "linear-gradient(180deg,#0F172A,#020617)",
    "sidebar_text": "#F1F5F9", "header_bg": "linear-gradient(135deg,#1E293B,#334155)",
    "grid": "rgba(255,255,255,0.06)", "plot_bg": "rgba(0,0,0,0)"
}

def get_theme():
    return DARK if st.session_state.get("dark_mode", False) else LIGHT

def inject_css(c):
    st.markdown(f"""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    *,html,body,[class*="css"]{{font-family:'Inter',sans-serif;}}
    .main .block-container{{padding-top:1rem;padding-bottom:1rem;max-width:100%;}}
    .stApp{{background:linear-gradient(135deg,{c['bg']},{c['bg2']});}}
    section[data-testid="stSidebar"]{{background:{c['sidebar_bg']};color:{c['sidebar_text']};}}
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] label{{color:{c['sidebar_text']} !important;}}
    .kpi-card{{background:{c['card']};border-radius:16px;padding:20px 24px;
        box-shadow:0 4px 20px {c['shadow']};border:1px solid {c['border']};
        transition:all .3s ease;height:100%;}}
    .kpi-card:hover{{transform:translateY(-4px);box-shadow:0 8px 30px {c['shadow']};}}
    .kpi-value{{font-size:2rem;font-weight:800;color:{c['primary']};line-height:1.1;margin:6px 0;}}
    .kpi-label{{font-size:.8rem;font-weight:600;color:{c['text2']};text-transform:uppercase;letter-spacing:1px;}}
    .kpi-delta-pos{{font-size:.85rem;font-weight:600;color:{c['success']};}}
    .kpi-delta-neg{{font-size:.85rem;font-weight:600;color:{c['danger']};}}
    .kpi-icon{{font-size:1.5rem;margin-bottom:4px;}}
    .chart-box{{background:{c['card']};border-radius:16px;padding:20px;
        box-shadow:0 4px 20px {c['shadow']};border:1px solid {c['border']};margin-bottom:16px;}}
    .chart-title{{font-size:1rem;font-weight:700;color:{c['primary']};margin-bottom:12px;
        padding-bottom:8px;border-bottom:2px solid {c['secondary']};display:inline-block;}}
    .page-hdr{{background:{c['header_bg']};color:white;padding:24px 32px;border-radius:20px;
        margin-bottom:24px;box-shadow:0 8px 32px {c['shadow']};}}
    .page-hdr h1{{color:white;margin:0;font-weight:800;font-size:1.8rem;}}
    .page-hdr p{{color:rgba(255,255,255,.7);margin:4px 0 0 0;font-size:.95rem;}}
    .stTabs [data-baseweb="tab-list"]{{gap:8px;background:{c['card']};border-radius:12px;padding:6px;
        box-shadow:0 2px 10px {c['shadow']};}}
    .stTabs [data-baseweb="tab"]{{border-radius:8px;font-weight:600;color:{c['text']};}}
    .stTabs [aria-selected="true"]{{background:{c['header_bg']};color:white !important;}}
    div[data-testid="stMetric"]{{background:{c['card']};border-radius:12px;padding:16px;
        box-shadow:0 2px 12px {c['shadow']};}}
    .student-card{{background:{c['card']};border-radius:20px;padding:28px;
        box-shadow:0 6px 24px {c['shadow']};border:1px solid {c['border']};margin-bottom:20px;}}
    .student-name{{font-size:1.6rem;font-weight:800;color:{c['primary']};}}
    .student-info{{font-size:.9rem;color:{c['text2']};margin-top:4px;}}
    .progress-bar-bg{{background:{c['bg']};border-radius:10px;height:12px;overflow:hidden;}}
    .progress-bar-fill{{height:100%;border-radius:10px;transition:width .8s ease;}}
    #MainMenu{{visibility:hidden;}}footer{{visibility:hidden;}}header{{visibility:hidden;}}
    </style>""", unsafe_allow_html=True)

def kpi(icon, label, value, delta=None, good=True):
    c = get_theme()
    dh = ""
    if delta:
        cls = "kpi-delta-pos" if good else "kpi-delta-neg"
        arr = "▲" if good else "▼"
        dh = f'<div class="{cls}">{arr} {delta}</div>'
    return f'<div class="kpi-card"><div class="kpi-icon">{icon}</div><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div>{dh}</div>'

def hdr(title):
    return f'<div class="chart-title">{title}</div>'

def plot_layout(fig, height=400):
    c = get_theme()
    fig.update_layout(
        plot_bgcolor=c["plot_bg"], paper_bgcolor=c["plot_bg"],
        font=dict(family="Inter", color=c["text"]),
        margin=dict(l=40, r=20, t=40, b=40), height=height,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
        xaxis=dict(gridcolor=c["grid"]), yaxis=dict(gridcolor=c["grid"])
    )
    return fig

def progress_bar(label, pct, color):
    return f'''<div style="margin:8px 0;"><div style="display:flex;justify-content:space-between;margin-bottom:4px;">
    <span style="font-size:.85rem;font-weight:600;">{label}</span>
    <span style="font-size:.85rem;font-weight:700;color:{color};">{pct:.1f}%</span></div>
    <div class="progress-bar-bg"><div class="progress-bar-fill" style="width:{min(pct,100):.1f}%;background:{color};"></div></div></div>'''

def fig_to_bytes(fig, fmt="png"):
    return fig.to_image(format=fmt, width=1200, height=800, scale=2)

def student_report_fig(student_id, students, exams, attendance, fees):
    """Generate a comprehensive student report as a Plotly figure."""
    c = get_theme()
    stu = students[students["Student_ID"] == student_id]
    if len(stu) == 0:
        return None, None
    stu = stu.iloc[0]
    s_exams = exams[exams["Student_ID"] == student_id].copy()
    s_att = attendance[attendance["Student_ID"] == student_id].copy()
    s_fees = fees[fees["Student_ID"] == student_id].copy()

    from plotly.subplots import make_subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Monthly Exam Scores", "Attendance Trend",
                        "Subject-wise Performance", "Fee Payment Status"),
        vertical_spacing=0.15, horizontal_spacing=0.12,
        specs=[[{"type": "xy"}, {"type": "xy"}],
               [{"type": "xy"}, {"type": "domain"}]]
    )

    # 1) Monthly exam trend
    if len(s_exams) > 0:
        month_map = {m: i for i, m in enumerate(MONTH_ORDER)}
        s_exams["MS"] = s_exams["Month"].map(month_map)
        monthly = s_exams.groupby(["Month", "MS"])["Percentage"].mean().reset_index().sort_values("MS")
        fig.add_trace(go.Scatter(
            x=monthly["Month"], y=monthly["Percentage"],
            mode="lines+markers", name="Exam %",
            line=dict(color=c["secondary"], width=3),
            marker=dict(size=8)
        ), row=1, col=1)

    # 2) Attendance trend
    if len(s_att) > 0:
        month_map = {m: i for i, m in enumerate(MONTH_ORDER)}
        s_att["MS"] = s_att["Month"].map(month_map)
        att_m = s_att.sort_values("MS")
        fig.add_trace(go.Bar(
            x=att_m["Month"], y=att_m["Attendance_Percentage"],
            name="Attendance %", marker_color=c["blue_light"]
        ), row=1, col=2)

    # 3) Subject-wise
    if len(s_exams) > 0:
        subj = s_exams.groupby("Subject")["Percentage"].mean().reset_index().sort_values("Percentage")
        fig.add_trace(go.Bar(
            x=subj["Percentage"], y=subj["Subject"], orientation="h",
            name="Subject Avg", marker_color=c["purple"]
        ), row=2, col=1)

    # 4) Fee status
    if len(s_fees) > 0:
        paid = (s_fees["Payment_Status"] == "Paid").sum()
        unpaid = (s_fees["Payment_Status"] == "Unpaid").sum()
        fig.add_trace(go.Pie(
            labels=["Paid", "Unpaid"], values=[paid, unpaid],
            marker_colors=[c["success"], c["danger"]],
            hole=0.5, textinfo="label+percent"
        ), row=2, col=2)

    fig.update_layout(
        title=dict(text=f"Progress Report: {stu['Student_Name']} (ID: {student_id}) | Class {stu['Class']}-{stu['Section']}",
                   font=dict(size=16, family="Inter")),
        plot_bgcolor=c["plot_bg"], paper_bgcolor=c["plot_bg"],
        font=dict(family="Inter", color=c["text"]),
        height=700, width=1100, showlegend=False,
        margin=dict(l=50, r=30, t=80, b=40)
    )
    
    info = {
        "name": stu["Student_Name"], "class": stu["Class"], "section": stu["Section"],
        "gender": stu["Gender"], "guardian": stu["Guardian_Name"],
        "guardian_contact": stu.get("Guardian_Contact", "N/A"),
        "fee_status": stu["Fee_Status"], "scholarship": stu["Scholarship"],
        "performance": stu["Performance_Category"],
        "avg_score": s_exams["Percentage"].mean() if len(s_exams) > 0 else 0,
        "avg_att": s_att["Attendance_Percentage"].mean() if len(s_att) > 0 else 0,
        "subjects_count": s_exams["Subject"].nunique() if len(s_exams) > 0 else 0,
        "paid_months": (s_fees["Payment_Status"] == "Paid").sum() if len(s_fees) > 0 else 0,
        "total_months": len(s_fees)
    }
    return fig, info
