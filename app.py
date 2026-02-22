"""
School BI Dashboard v2 – Redesigned with Advanced Features
Dark/Light Mode | CSV Upload | Student Lookup | Progress Export | Parent Notification
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os, io, base64, json
from datetime import datetime
from dashboard_utils import (
    MONTH_ORDER, GRADE_COLORS, LIGHT, DARK, get_theme,
    inject_css, kpi, hdr, plot_layout, progress_bar, student_report_fig
)

st.set_page_config(page_title="School BI Dashboard v2", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

# ── SESSION STATE INIT ────────────────────────────────────
for key, val in [("dark_mode", False), ("uploaded_data", {}), ("student_search_id", "")]:
    if key not in st.session_state:
        st.session_state[key] = val

C = get_theme()
inject_css(C)

# ── DATA LOADING ──────────────────────────────────────────
@st.cache_data
def load_csv(path):
    return pd.read_csv(path) if os.path.exists(path) else None

def load_all():
    base = os.path.dirname(os.path.abspath(__file__))
    # Use uploaded data if available, otherwise load from disk
    ud = st.session_state.uploaded_data
    students = ud.get("students", load_csv(os.path.join(base, "Students_Master_Table.csv")))
    exams = ud.get("exams", load_csv(os.path.join(base, "Exam_Results_Table.csv")))
    attendance = ud.get("attendance", load_csv(os.path.join(base, "Attendance_Table.csv")))
    fees = ud.get("fees", load_csv(os.path.join(base, "Fee_Collection_Table.csv")))
    teachers = ud.get("teachers", load_csv(os.path.join(base, "Teacher_Table.csv")))
    dropout = load_csv(os.path.join(base, "Dropout_Log.csv"))
    transfer = load_csv(os.path.join(base, "Transfer_Log.csv"))
    survey = load_csv(os.path.join(base, "Parent_Survey_Table.csv"))
    comparison = load_csv(os.path.join(base, "School_Comparison_Table.csv"))

    if exams is not None and "Total_Score" not in exams.columns:
        exams["Total_Score"] = exams["Monthly_Test_50"] + exams["Midterm_100"] + exams["Final_100"]
        exams["Percentage"] = exams["Total_Score"] / 250 * 100
        exams["Grade"] = pd.cut(exams["Percentage"], bins=[-1,50,60,70,80,90,101], labels=["F","D","C","B","A","A+"])
        exams["Performance_Band"] = pd.cut(exams["Percentage"], bins=[-1,50,80,101], labels=["Low Performer","Average Performer","High Performer"])
    if exams is not None:
        mm = {m:i for i,m in enumerate(MONTH_ORDER)}
        exams["Month_Sort"] = exams["Month"].map(mm)
    if attendance is not None:
        mm = {m:i for i,m in enumerate(MONTH_ORDER)}
        attendance["Month_Sort"] = attendance["Month"].map(mm)
        if "Attendance_Category" not in attendance.columns:
            attendance["Attendance_Category"] = pd.cut(attendance["Attendance_Percentage"], bins=[-1,60,75,80,90,101], labels=["Critical","Low","Satisfactory","Good","Excellent"])
    if fees is not None:
        mm = {m:i for i,m in enumerate(MONTH_ORDER)}
        fees["Month_Sort"] = fees["Month"].map(mm)
        if "Outstanding_Amount" not in fees.columns:
            fees["Outstanding_Amount"] = fees["Monthly_Fee"] - fees["Amount_Paid"]
    return students, exams, attendance, fees, teachers, dropout, transfer, survey, comparison

students, exams, attendance, fees, teachers, dropout, transfer, survey, comparison = load_all()

# ── SIDEBAR ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 School BI v2")
    st.markdown("##### Advanced Dashboard")
    st.markdown("---")

    # Dark/Light Mode Toggle
    dark = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode, key="dark_toggle")
    if dark != st.session_state.dark_mode:
        st.session_state.dark_mode = dark
        st.rerun()

    st.markdown("---")
    st.markdown("### 🔍 Filters")

    all_classes = sorted(students["Class"].unique()) if students is not None else []
    all_sections = sorted(students["Section"].unique()) if students is not None else []

    selected_classes = st.multiselect("Class", all_classes, default=all_classes, key="cf")
    selected_sections = st.multiselect("Section", all_sections, default=all_sections, key="sf")
    selected_months = st.multiselect("Month", MONTH_ORDER, default=MONTH_ORDER, key="mf")
    selected_gender = st.multiselect("Gender", ["Male","Female"], default=["Male","Female"], key="gf")

    st.markdown("---")
    st.markdown(f"<div style='text-align:center;color:{C['text2']};font-size:.75rem;'>School BI v2.0 | {datetime.now().strftime('%Y-%m-%d')}</div>", unsafe_allow_html=True)

# ── FILTER DATA ───────────────────────────────────────────
if students is not None:
    f_stu = students[(students["Class"].isin(selected_classes))&(students["Section"].isin(selected_sections))&(students["Gender"].isin(selected_gender))]
    sids = f_stu["Student_ID"].tolist()
    f_ex = exams[(exams["Student_ID"].isin(sids))&(exams["Month"].isin(selected_months))] if exams is not None else pd.DataFrame()
    f_at = attendance[(attendance["Student_ID"].isin(sids))&(attendance["Month"].isin(selected_months))] if attendance is not None else pd.DataFrame()
    f_fe = fees[(fees["Student_ID"].isin(sids))&(fees["Month"].isin(selected_months))] if fees is not None else pd.DataFrame()
else:
    f_stu = f_ex = f_at = f_fe = pd.DataFrame()

# ── TABS ──────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🏠 Executive", "📊 Academic", "📋 Attendance", "💰 Financial",
    "🔎 Student Lookup", "📤 Upload Data", "📈 Rankings"
])

# ══════════════════════════════════════════════════════════
# TAB 1: EXECUTIVE
# ══════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="page-hdr"><h1>Executive Overview</h1><p>Key performance indicators — Academic Year 2025-2026</p></div>', unsafe_allow_html=True)
    ts = len(f_stu)
    tr = f_fe["Amount_Paid"].sum() if len(f_fe)>0 else 0
    op = f_ex["Percentage"].mean() if len(f_ex)>0 else 0
    aa = f_at["Attendance_Percentage"].mean() if len(f_at)>0 else 0
    pp = (len(f_ex[f_ex["Percentage"]>=33])/len(f_ex)*100) if len(f_ex)>0 else 0
    fc = (f_fe["Amount_Paid"].sum()/f_fe["Monthly_Fee"].sum()*100) if len(f_fe)>0 and f_fe["Monthly_Fee"].sum()>0 else 0

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    with c1: st.markdown(kpi("👨‍🎓","Students",f"{ts:,}"),unsafe_allow_html=True)
    with c2: st.markdown(kpi("💰","Revenue",f"Rs {tr/1e6:.1f}M","Active",True),unsafe_allow_html=True)
    with c3: st.markdown(kpi("📊","Academic %",f"{op:.1f}%",f"{op:.0f} pts",op>=50),unsafe_allow_html=True)
    with c4: st.markdown(kpi("📋","Attendance",f"{aa:.1f}%","avg",aa>=75),unsafe_allow_html=True)
    with c5: st.markdown(kpi("✅","Pass Rate",f"{pp:.1f}%",">=33%",pp>=80),unsafe_allow_html=True)
    with c6: st.markdown(kpi("🏦","Fee %",f"{fc:.1f}%","collected",fc>=70),unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    cl,cr = st.columns([2,1])
    with cl:
        st.markdown('<div class="chart-box">',unsafe_allow_html=True)
        st.markdown(hdr("Monthly Academic Trend by Section"),unsafe_allow_html=True)
        if len(f_ex)>0:
            td = f_ex.groupby(["Month","Month_Sort","Section"])["Percentage"].mean().reset_index().sort_values("Month_Sort")
            fig = px.line(td,x="Month",y="Percentage",color="Section",markers=True,
                         color_discrete_map={"A":C["secondary"],"B":C["purple"]},category_orders={"Month":MONTH_ORDER})
            fig.update_traces(line=dict(width=3),marker=dict(size=8))
            st.plotly_chart(plot_layout(fig,350),width="stretch")
        st.markdown('</div>',unsafe_allow_html=True)
    with cr:
        st.markdown('<div class="chart-box">',unsafe_allow_html=True)
        st.markdown(hdr("Fee Payment Status"),unsafe_allow_html=True)
        if len(f_fe)>0:
            sc = f_fe["Payment_Status"].value_counts()
            fig = go.Figure(data=[go.Pie(labels=sc.index,values=sc.values,hole=.6,
                marker_colors=[C["success"],C["danger"]],textinfo="label+percent")])
            st.plotly_chart(plot_layout(fig,350),width="stretch")
        st.markdown('</div>',unsafe_allow_html=True)

    cl2,cr2 = st.columns(2)
    with cl2:
        st.markdown('<div class="chart-box">',unsafe_allow_html=True)
        st.markdown(hdr("Students by Class & Gender"),unsafe_allow_html=True)
        gc = f_stu.groupby(["Class","Gender"]).size().reset_index(name="Count")
        fig = px.bar(gc,x="Class",y="Count",color="Gender",barmode="stack",
                     color_discrete_map={"Male":C["blue_light"],"Female":C["secondary"]},text="Count")
        fig.update_traces(textposition="inside",textfont_size=11)
        st.plotly_chart(plot_layout(fig,350),width="stretch")
        st.markdown('</div>',unsafe_allow_html=True)
    with cr2:
        st.markdown('<div class="chart-box">',unsafe_allow_html=True)
        st.markdown(hdr("Quick Stats by Class"),unsafe_allow_html=True)
        rows=[]
        for cls in sorted(f_stu["Class"].unique()):
            ci=f_stu[f_stu["Class"]==cls]["Student_ID"].tolist()
            ce=f_ex[f_ex["Student_ID"].isin(ci)] if len(f_ex)>0 else pd.DataFrame()
            ca=f_at[f_at["Student_ID"].isin(ci)] if len(f_at)>0 else pd.DataFrame()
            cf=f_fe[f_fe["Student_ID"].isin(ci)] if len(f_fe)>0 else pd.DataFrame()
            rows.append({"Class":f"Class {cls}","Students":len(f_stu[f_stu['Class']==cls]),
                "Avg %":f"{ce['Percentage'].mean():.1f}" if len(ce)>0 else "-",
                "Att %":f"{ca['Attendance_Percentage'].mean():.1f}" if len(ca)>0 else "-",
                "Fee %":f"{cf['Amount_Paid'].sum()/cf['Monthly_Fee'].sum()*100:.0f}" if len(cf)>0 and cf['Monthly_Fee'].sum()>0 else "-"})
        st.dataframe(pd.DataFrame(rows),width="stretch",hide_index=True,height=350)
        st.markdown('</div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# TAB 2: ACADEMIC
# ══════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="page-hdr"><h1>Academic Analytics</h1><p>Subject performance, rankings, and grade distributions</p></div>',unsafe_allow_html=True)
    if len(f_ex)>0:
        st.markdown('<div class="chart-box">',unsafe_allow_html=True)
        st.markdown(hdr("Subject x Month Heatmap"),unsafe_allow_html=True)
        hm = f_ex.pivot_table(values="Percentage",index="Subject",columns="Month",aggfunc="mean")
        am = [m for m in MONTH_ORDER if m in hm.columns]; hm = hm[am]
        fig = go.Figure(data=go.Heatmap(z=hm.values,x=hm.columns,y=hm.index,
            colorscale=[[0,"#e74c3c"],[.33,"#f39c12"],[.5,"#f1c40f"],[.67,"#2ecc71"],[1,"#1abc9c"]],
            text=np.round(hm.values,1),texttemplate="%{text}%",textfont=dict(size=11)))
        st.plotly_chart(plot_layout(fig,380),width="stretch")
        st.markdown('</div>',unsafe_allow_html=True)

        cl,cr = st.columns(2)
        with cl:
            st.markdown('<div class="chart-box">',unsafe_allow_html=True)
            st.markdown(hdr("Section A vs B Performance"),unsafe_allow_html=True)
            cp = f_ex.groupby(["Class","Section"])["Percentage"].mean().reset_index()
            fig = px.bar(cp,x="Class",y="Percentage",color="Section",barmode="group",
                        color_discrete_map={"A":C["secondary"],"B":C["purple"]},text=cp["Percentage"].round(1))
            fig.update_traces(textposition="outside",textfont_size=10)
            st.plotly_chart(plot_layout(fig,380),width="stretch")
            st.markdown('</div>',unsafe_allow_html=True)
        with cr:
            st.markdown('<div class="chart-box">',unsafe_allow_html=True)
            st.markdown(hdr("Top 5 & Bottom 5 Students"),unsafe_allow_html=True)
            sa = f_ex.groupby("Student_ID")["Percentage"].mean().reset_index()
            sa = sa.merge(f_stu[["Student_ID","Student_Name","Class","Section"]],on="Student_ID").sort_values("Percentage",ascending=False)
            t5 = sa.head(5)[["Student_Name","Class","Percentage"]].copy(); t5["Percentage"]=t5["Percentage"].round(1)
            t5.insert(0,"Rank",["🥇","🥈","🥉","4th","5th"])
            b5 = sa.tail(5)[["Student_Name","Class","Percentage"]].copy(); b5["Percentage"]=b5["Percentage"].round(1)
            st.markdown("**🏆 Top 5**"); st.dataframe(t5,width="stretch",hide_index=True,height=170)
            st.markdown("**⚠️ Bottom 5**"); st.dataframe(b5,width="stretch",hide_index=True,height=170)
            st.markdown('</div>',unsafe_allow_html=True)

        cl2,cr2 = st.columns(2)
        with cl2:
            st.markdown('<div class="chart-box">',unsafe_allow_html=True)
            st.markdown(hdr("Monthly Score Trend"),unsafe_allow_html=True)
            mt = f_ex.groupby(["Month","Month_Sort"])["Percentage"].mean().reset_index().sort_values("Month_Sort")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=mt["Month"],y=mt["Percentage"],mode="lines+markers",fill="tozeroy",
                fillcolor=f"rgba({int(C['secondary'][1:3],16)},{int(C['secondary'][3:5],16)},{int(C['secondary'][5:7],16)},0.15)",
                line=dict(color=C["secondary"],width=3),marker=dict(size=10)))
            st.plotly_chart(plot_layout(fig,350),width="stretch")
            st.markdown('</div>',unsafe_allow_html=True)
        with cr2:
            st.markdown('<div class="chart-box">',unsafe_allow_html=True)
            st.markdown(hdr("Grade Distribution"),unsafe_allow_html=True)
            grc = f_ex["Grade"].value_counts().reindex(["A+","A","B","C","D","F"]).fillna(0)
            fig = go.Figure(data=[go.Bar(x=grc.index,y=grc.values,
                marker_color=[GRADE_COLORS.get(g,"#999") for g in grc.index],
                text=grc.values.astype(int),textposition="outside")])
            st.plotly_chart(plot_layout(fig,350),width="stretch")
            st.markdown('</div>',unsafe_allow_html=True)
    else:
        st.warning("No exam data for selected filters.")

# ══════════════════════════════════════════════════════════
# TAB 3: ATTENDANCE
# ══════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="page-hdr"><h1>Attendance Insights</h1><p>Trends, risk identification, and correlation</p></div>',unsafe_allow_html=True)
    if len(f_at)>0:
        av = f_at["Attendance_Percentage"].mean()
        rc = len(f_at.groupby("Student_ID")["Attendance_Percentage"].mean().reset_index().query("Attendance_Percentage<75"))
        ep = (f_at["Attendance_Category"]=="Excellent").mean()*100
        crp = (f_at["Attendance_Category"]=="Critical").mean()*100
        c1,c2,c3,c4 = st.columns(4)
        with c1: st.markdown(kpi("📋","Avg Attendance",f"{av:.1f}%","all",av>=75),unsafe_allow_html=True)
        with c2: st.markdown(kpi("⚠️","At-Risk",f"{rc}","<75%",False),unsafe_allow_html=True)
        with c3: st.markdown(kpi("⭐","Excellent",f"{ep:.1f}%",">=90%",True),unsafe_allow_html=True)
        with c4: st.markdown(kpi("🔴","Critical",f"{crp:.1f}%","<60%",False),unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)

        cl,cr = st.columns([2,1])
        with cl:
            st.markdown('<div class="chart-box">',unsafe_allow_html=True)
            st.markdown(hdr("Monthly Attendance by Section"),unsafe_allow_html=True)
            am = f_at.groupby(["Month","Month_Sort","Section"])["Attendance_Percentage"].mean().reset_index().sort_values("Month_Sort")
            fig = px.line(am,x="Month",y="Attendance_Percentage",color="Section",markers=True,
                         color_discrete_map={"A":C["secondary"],"B":C["purple"]},category_orders={"Month":MONTH_ORDER})
            fig.add_hline(y=75,line_dash="dash",line_color=C["danger"],annotation_text="75% Threshold")
            fig.update_traces(line=dict(width=3),marker=dict(size=8))
            st.plotly_chart(plot_layout(fig,350),width="stretch")
            st.markdown('</div>',unsafe_allow_html=True)
        with cr:
            st.markdown('<div class="chart-box">',unsafe_allow_html=True)
            st.markdown(hdr("Category Breakdown"),unsafe_allow_html=True)
            cc = f_at["Attendance_Category"].value_counts()
            cmap = {"Excellent":C["success"],"Good":"#2980b9","Satisfactory":C["warning"],"Low":C["orange"],"Critical":C["danger"]}
            fig = go.Figure(data=[go.Pie(labels=cc.index,values=cc.values,hole=.5,
                marker_colors=[cmap.get(c,"#999") for c in cc.index],textinfo="label+percent")])
            st.plotly_chart(plot_layout(fig,350),width="stretch")
            st.markdown('</div>',unsafe_allow_html=True)

        cl2,cr2 = st.columns(2)
        with cl2:
            st.markdown('<div class="chart-box">',unsafe_allow_html=True)
            st.markdown(hdr("Attendance vs Academic (Scatter)"),unsafe_allow_html=True)
            sa2 = f_at.groupby("Student_ID")["Attendance_Percentage"].mean().reset_index()
            sp2 = f_ex.groupby("Student_ID")["Percentage"].mean().reset_index() if len(f_ex)>0 else pd.DataFrame()
            if len(sp2)>0:
                sd = sa2.merge(sp2,on="Student_ID").merge(f_stu[["Student_ID","Performance_Category","Class"]],on="Student_ID")
                fig = px.scatter(sd,x="Attendance_Percentage",y="Percentage",color="Performance_Category",
                    color_discrete_map={"High":C["success"],"Average":C["warning"],"Low":C["danger"]},opacity=.7,hover_data=["Class"])
                z = np.polyfit(sd["Attendance_Percentage"],sd["Percentage"],1); p = np.poly1d(z)
                xr = np.linspace(sd["Attendance_Percentage"].min(),sd["Attendance_Percentage"].max(),50)
                fig.add_trace(go.Scatter(x=xr,y=p(xr),mode="lines",name="Trend",line=dict(color=C["primary"],width=2,dash="dash")))
                st.plotly_chart(plot_layout(fig,380),width="stretch")
                corr = sd["Attendance_Percentage"].corr(sd["Percentage"])
                st.markdown(f"<div style='text-align:center;color:{C['text2']};'>Pearson r = <b>{corr:.3f}</b></div>",unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)
        with cr2:
            st.markdown('<div class="chart-box">',unsafe_allow_html=True)
            st.markdown(hdr("At-Risk Students (<75%)"),unsafe_allow_html=True)
            rs = sa2[sa2["Attendance_Percentage"]<75].merge(f_stu[["Student_ID","Student_Name","Class","Section"]],on="Student_ID")
            rs["Attendance_Percentage"]=rs["Attendance_Percentage"].round(1)
            st.dataframe(rs[["Student_Name","Class","Section","Attendance_Percentage"]].head(20).rename(columns={"Attendance_Percentage":"Att %"}),width="stretch",hide_index=True,height=420)
            st.markdown('</div>',unsafe_allow_html=True)
    else:
        st.warning("No attendance data for selected filters.")

# ══════════════════════════════════════════════════════════
# TAB 4: FINANCIAL
# ══════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="page-hdr"><h1>Financial Dashboard</h1><p>Fee collection, revenue trends, and defaulter analysis</p></div>',unsafe_allow_html=True)
    if len(f_fe)>0:
        te=f_fe["Monthly_Fee"].sum(); tc=f_fe["Amount_Paid"].sum(); to2=te-tc
        fcp=tc/te*100 if te>0 else 0
        fd_c = f_fe[f_fe["Payment_Status"]=="Unpaid"].groupby("Student_ID").size()
        dfc = (fd_c>=3).sum()
        c1,c2,c3,c4,c5 = st.columns(5)
        with c1: st.markdown(kpi("💵","Expected",f"Rs {te/1e6:.1f}M"),unsafe_allow_html=True)
        with c2: st.markdown(kpi("💰","Collected",f"Rs {tc/1e6:.1f}M",f"{fcp:.0f}%",True),unsafe_allow_html=True)
        with c3: st.markdown(kpi("📉","Outstanding",f"Rs {to2/1e6:.1f}M","pending",False),unsafe_allow_html=True)
        with c4: st.markdown(kpi("📊","Collection",f"{fcp:.1f}%","rate",fcp>=70),unsafe_allow_html=True)
        with c5: st.markdown(kpi("⚠️","Defaulters",f"{dfc}",">=3mo",False),unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)

        cl,cr = st.columns([2,1])
        with cl:
            st.markdown('<div class="chart-box">',unsafe_allow_html=True)
            st.markdown(hdr("Monthly Revenue: Expected vs Collected"),unsafe_allow_html=True)
            mr = f_fe.groupby(["Month","Month_Sort"]).agg(Exp=("Monthly_Fee","sum"),Col=("Amount_Paid","sum")).reset_index().sort_values("Month_Sort")
            mr["Rate"]=mr["Col"]/mr["Exp"]*100
            fig = make_subplots(specs=[[{"secondary_y":True}]])
            fig.add_trace(go.Bar(x=mr["Month"],y=mr["Exp"],name="Expected",marker_color=f"rgba({int(C['primary'][1:3],16)},{int(C['primary'][3:5],16)},{int(C['primary'][5:7],16)},0.3)"),secondary_y=False)
            fig.add_trace(go.Bar(x=mr["Month"],y=mr["Col"],name="Collected",marker_color=C["secondary"]),secondary_y=False)
            fig.add_trace(go.Scatter(x=mr["Month"],y=mr["Rate"],name="Rate %",mode="lines+markers",line=dict(color=C["warning"],width=3)),secondary_y=True)
            fig.update_layout(barmode="group"); st.plotly_chart(plot_layout(fig,380),width="stretch")
            st.markdown('</div>',unsafe_allow_html=True)
        with cr:
            st.markdown('<div class="chart-box">',unsafe_allow_html=True)
            st.markdown(hdr("Payment by Class"),unsafe_allow_html=True)
            cs = f_fe.groupby(["Class","Payment_Status"]).size().reset_index(name="Count")
            fig = px.bar(cs,x="Count",y="Class",color="Payment_Status",orientation="h",barmode="stack",
                        color_discrete_map={"Paid":C["success"],"Unpaid":C["danger"]},text="Count")
            fig.update_traces(textposition="inside"); st.plotly_chart(plot_layout(fig,380),width="stretch")
            st.markdown('</div>',unsafe_allow_html=True)

        cl2,cr2 = st.columns(2)
        with cl2:
            st.markdown('<div class="chart-box">',unsafe_allow_html=True)
            st.markdown(hdr("Revenue by Class"),unsafe_allow_html=True)
            crv = f_fe.groupby("Class")["Amount_Paid"].sum().reset_index().sort_values("Amount_Paid",ascending=True)
            fig = go.Figure(go.Bar(x=crv["Amount_Paid"],y=crv["Class"].astype(str).apply(lambda x:f"Class {x}"),
                orientation="h",marker_color=C["secondary"],text=(crv["Amount_Paid"]/1e6).round(2).astype(str)+"M",textposition="outside"))
            st.plotly_chart(plot_layout(fig,380),width="stretch")
            st.markdown('</div>',unsafe_allow_html=True)
        with cr2:
            st.markdown('<div class="chart-box">',unsafe_allow_html=True)
            st.markdown(hdr("Fee Defaulters (>=3 Unpaid)"),unsafe_allow_html=True)
            dd = f_fe[f_fe["Payment_Status"]=="Unpaid"].groupby("Student_ID").agg(Unpaid=("Payment_Status","count"),Owed=("Outstanding_Amount","sum")).reset_index()
            dd = dd[dd["Unpaid"]>=3].merge(f_stu[["Student_ID","Student_Name","Class","Guardian_Name"]],on="Student_ID").sort_values("Owed",ascending=False)
            dd["Owed"]=dd["Owed"].round(0).astype(int)
            st.dataframe(dd[["Student_Name","Class","Unpaid","Owed","Guardian_Name"]].head(15),width="stretch",hide_index=True,height=380)
            st.markdown('</div>',unsafe_allow_html=True)
    else:
        st.warning("No fee data for selected filters.")

# ══════════════════════════════════════════════════════════
# TAB 5: STUDENT LOOKUP  ★ NEW FEATURE ★
# ══════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="page-hdr"><h1>🔎 Student Progress Lookup</h1><p>Search by Student ID for individual exam, attendance, and financial reports</p></div>',unsafe_allow_html=True)

    if students is not None:
        all_ids = sorted(students["Student_ID"].unique())
        col_search, col_btn = st.columns([3,1])
        with col_search:
            sid = st.selectbox("Enter or Select Student ID", options=[""] + [str(i) for i in all_ids], key="stu_sel", index=0)
        with col_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            search_btn = st.button("🔍 Search", type="primary", width="stretch")

        if sid and (search_btn or sid != ""):
            sid_int = int(sid)
            fig, info = student_report_fig(sid_int, students, exams, attendance, fees)

            if info is None:
                st.error(f"Student ID {sid} not found.")
            else:
                # Student Profile Card
                st.markdown(f'''<div class="student-card">
                    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">
                        <div><div class="student-name">👤 {info["name"]}</div>
                        <div class="student-info">ID: {sid_int} | Class {info["class"]}-{info["section"]} | {info["gender"]}</div>
                        <div class="student-info">Guardian: {info["guardian"]} | Contact: {info["guardian_contact"]}</div>
                        <div class="student-info">Fee Status: {info["fee_status"]} | Scholarship: {info["scholarship"]} | Category: {info["performance"]}</div></div>
                        <div style="text-align:center;">
                            <div style="font-size:2.5rem;font-weight:900;color:{C["secondary"]};">{info["avg_score"]:.1f}%</div>
                            <div style="font-size:.8rem;color:{C["text2"]};">Academic Avg</div>
                        </div>
                    </div></div>''', unsafe_allow_html=True)

                # Progress Bars
                pc1, pc2, pc3 = st.columns(3)
                with pc1:
                    st.markdown(progress_bar("Academic Score", info["avg_score"], C["secondary"]), unsafe_allow_html=True)
                with pc2:
                    att_color = C["success"] if info["avg_att"]>=80 else (C["warning"] if info["avg_att"]>=60 else C["danger"])
                    st.markdown(progress_bar("Attendance", info["avg_att"], att_color), unsafe_allow_html=True)
                with pc3:
                    fee_pct = info["paid_months"]/info["total_months"]*100 if info["total_months"]>0 else 0
                    st.markdown(progress_bar("Fee Payment", fee_pct, C["success"] if fee_pct>=80 else C["danger"]), unsafe_allow_html=True)

                # Charts
                st.plotly_chart(fig, width="stretch")

                # ── EXPORT OPTIONS ──
                st.markdown("---")
                st.markdown(f"### 💾 Export Progress Report")
                exp1, exp2, exp3 = st.columns(3)

                with exp1:
                    fmt = st.selectbox("Image Format", ["PNG", "JPEG", "SVG", "PDF"], key="img_fmt")
                with exp2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("📥 Download Report Image", type="primary", width="stretch"):
                        try:
                            img_bytes = fig.to_image(format=fmt.lower(), width=1200, height=800, scale=2)
                            st.download_button(
                                label=f"Save as {fmt}",
                                data=img_bytes,
                                file_name=f"Student_{sid_int}_Report.{fmt.lower()}",
                                mime=f"image/{fmt.lower()}" if fmt != "PDF" else "application/pdf"
                            )
                        except Exception as e:
                            st.warning(f"Image export requires kaleido: `pip install kaleido`. Error: {e}")
                with exp3:
                    st.markdown("<br>", unsafe_allow_html=True)
                    # Generate HTML report as downloadable file
                    html_report = f"""<html><head><title>Progress Report - {info['name']}</title>
                    <style>body{{font-family:Inter,sans-serif;padding:40px;}}
                    .hdr{{background:#1B2A4A;color:white;padding:20px;border-radius:10px;}}
                    table{{width:100%;border-collapse:collapse;margin-top:20px;}}
                    td,th{{padding:10px;border:1px solid #ddd;text-align:left;}}</style></head>
                    <body><div class="hdr"><h1>Student Progress Report</h1>
                    <p>{info['name']} | ID: {sid_int} | Class {info['class']}-{info['section']}</p></div>
                    <table><tr><th>Metric</th><th>Value</th></tr>
                    <tr><td>Academic Average</td><td>{info['avg_score']:.1f}%</td></tr>
                    <tr><td>Attendance Average</td><td>{info['avg_att']:.1f}%</td></tr>
                    <tr><td>Subjects</td><td>{info['subjects_count']}</td></tr>
                    <tr><td>Fee Paid Months</td><td>{info['paid_months']}/{info['total_months']}</td></tr>
                    <tr><td>Performance Category</td><td>{info['performance']}</td></tr>
                    <tr><td>Guardian</td><td>{info['guardian']}</td></tr>
                    <tr><td>Contact</td><td>{info['guardian_contact']}</td></tr>
                    </table><p style="color:#999;margin-top:30px;">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p></body></html>"""
                    st.download_button("📄 Download HTML Report", html_report.encode(), f"Student_{sid_int}_Report.html", "text/html", width="stretch")

                # ── PARENT NOTIFICATION ──
                st.markdown("---")
                st.markdown("### 📱 Send Progress Report to Parent")
                pn1, pn2, pn3 = st.columns([2,2,1])
                with pn1:
                    parent_num = st.text_input("Parent/Guardian Contact Number",
                        value=str(info.get("guardian_contact", "")), key="parent_phone",
                        placeholder="+92-300-1234567")
                with pn2:
                    msg_template = st.selectbox("Message Template", [
                        "Full Progress Report",
                        "Academic Summary Only",
                        "Attendance Alert",
                        "Fee Reminder"
                    ], key="msg_tmpl")
                with pn3:
                    st.markdown("<br>", unsafe_allow_html=True)
                    send_btn = st.button("📤 Send Report", type="primary", width="stretch")

                if send_btn:
                    if not parent_num.strip():
                        st.error("Please enter a valid contact number.")
                    else:
                        msg_map = {
                            "Full Progress Report": f"Dear {info['guardian']}, your child {info['name']} (Class {info['class']}-{info['section']}) scored {info['avg_score']:.1f}% in academics with {info['avg_att']:.1f}% attendance. Fee: {info['paid_months']}/{info['total_months']} months paid.",
                            "Academic Summary Only": f"Dear {info['guardian']}, {info['name']}'s academic average is {info['avg_score']:.1f}% across {info['subjects_count']} subjects. Category: {info['performance']}.",
                            "Attendance Alert": f"Dear {info['guardian']}, {info['name']}'s attendance is {info['avg_att']:.1f}%.{' ATTENTION: Below 75% threshold!' if info['avg_att']<75 else ' Good attendance.'}",
                            "Fee Reminder": f"Dear {info['guardian']}, fee status for {info['name']}: {info['paid_months']}/{info['total_months']} months paid. {'Please clear outstanding dues.' if info['paid_months']<info['total_months'] else 'All fees cleared.'}"
                        }
                        st.success(f"✅ Report prepared for **{parent_num}**")
                        st.info(f"**Message Preview:**\n\n{msg_map[msg_template]}")
                        st.caption("Note: SMS integration requires a Twilio/SMS gateway API key to be configured. The message has been generated and is ready to send via your preferred gateway.")
    else:
        st.warning("No student data loaded. Upload data in the Upload tab.")

# ══════════════════════════════════════════════════════════
# TAB 6: UPLOAD DATA  ★ NEW FEATURE ★
# ══════════════════════════════════════════════════════════
with tab6:
    st.markdown('<div class="page-hdr"><h1>📤 Upload Data</h1><p>Upload your own CSV files to replace or update dashboard data</p></div>',unsafe_allow_html=True)

    st.markdown('<div class="chart-box">',unsafe_allow_html=True)
    st.markdown(hdr("Upload CSV Files"),unsafe_allow_html=True)

    st.markdown("""
    Upload CSV files to update the dashboard data. The following file types are supported:
    | File Type | Required Columns |
    |---|---|
    | **Students** | Student_ID, Student_Name, Gender, Class, Section |
    | **Exams** | Student_ID, Month, Subject, Monthly_Test_50, Midterm_100, Final_100 |
    | **Attendance** | Student_ID, Month, Attendance_Percentage |
    | **Fees** | Student_ID, Month, Monthly_Fee, Amount_Paid, Payment_Status |
    | **Teachers** | Teacher_ID, Teacher_Name, Subject, Class_Assigned |
    """)

    u1, u2 = st.columns(2)
    with u1:
        upload_type = st.selectbox("Select Data Type", ["Students", "Exams", "Attendance", "Fees", "Teachers"], key="utype")
    with u2:
        uploaded_file = st.file_uploader(f"Upload {upload_type} CSV", type=["csv"], key="ufile")

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ Loaded {len(df)} rows x {len(df.columns)} columns")
            st.dataframe(df.head(10), width="stretch", hide_index=True)

            if st.button("✅ Apply to Dashboard", type="primary"):
                key_map = {"Students":"students","Exams":"exams","Attendance":"attendance","Fees":"fees","Teachers":"teachers"}
                st.session_state.uploaded_data[key_map[upload_type]] = df
                st.success(f"✅ {upload_type} data applied! Switch to other tabs to see updated visuals.")
                st.rerun()
        except Exception as e:
            st.error(f"Error reading CSV: {e}")

    # Show currently loaded data status
    st.markdown("---")
    st.markdown(hdr("Current Data Status"), unsafe_allow_html=True)
    status_rows = []
    for name, data in [("Students", students), ("Exams", exams), ("Attendance", attendance), ("Fees", fees), ("Teachers", teachers)]:
        src = "📤 Uploaded" if name.lower() in st.session_state.uploaded_data else "💾 Disk"
        rows = len(data) if data is not None else 0
        cols = len(data.columns) if data is not None else 0
        status_rows.append({"Dataset": name, "Source": src, "Rows": rows, "Columns": cols})
    st.dataframe(pd.DataFrame(status_rows), width="stretch", hide_index=True)

    if st.session_state.uploaded_data:
        if st.button("🔄 Reset All to Original Files"):
            st.session_state.uploaded_data = {}
            st.rerun()
    st.markdown('</div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# TAB 7: RANKINGS & SURVEY
# ══════════════════════════════════════════════════════════
with tab7:
    st.markdown('<div class="page-hdr"><h1>Rankings & Parent Survey</h1><p>School ranking comparison and parent satisfaction</p></div>',unsafe_allow_html=True)
    st1, st2, st3 = st.tabs(["🏫 School Rankings", "📝 Parent Survey", "📊 Dropout Analysis"])

    with st1:
        if comparison is not None:
            st.markdown('<div class="chart-box">',unsafe_allow_html=True)
            cd = comparison.copy()
            if "Ranking_Score" in cd.columns: cd = cd.sort_values("Ranking_Score",ascending=False)
            if "School_Name" in cd.columns and "Ranking_Score" in cd.columns:
                fig = go.Figure(go.Bar(x=cd["School_Name"],y=cd["Ranking_Score"],
                    marker=dict(color=cd["Ranking_Score"],colorscale=[[0,C["warning"]],[.5,C["secondary"]],[1,C["success"]]]),
                    text=cd["Ranking_Score"].round(1),textposition="outside",textfont=dict(size=14)))
                st.plotly_chart(plot_layout(fig,400),width="stretch")
            st.dataframe(cd,width="stretch",hide_index=True)
            st.markdown('</div>',unsafe_allow_html=True)
        else:
            st.warning("Run `generate_school_comparison.py` first.")

    with st2:
        if survey is not None:
            pr = len(survey[survey["Recommendation_Score"]>=9]); dt = len(survey[survey["Recommendation_Score"]<=6])
            nps = (pr-dt)/len(survey)*100
            c1,c2,c3 = st.columns(3)
            with c1: st.markdown(kpi("📝","Responses",f"{len(survey)}"),unsafe_allow_html=True)
            with c2: st.markdown(kpi("⭐","Satisfaction",f"{survey['Overall_Satisfaction'].mean():.2f}/5"),unsafe_allow_html=True)
            with c3: st.markdown(kpi("📊","NPS",f"{nps:.1f}","score",nps>0),unsafe_allow_html=True)
            st.markdown("<br>",unsafe_allow_html=True)
            cl,cr = st.columns(2)
            with cl:
                st.markdown('<div class="chart-box">',unsafe_allow_html=True)
                cats = ["Teaching_Quality_Rating","Discipline_Rating","Communication_Rating","Fee_Satisfaction"]
                labs = ["Teaching","Discipline","Communication","Fee"]
                vals = [survey[c].mean() for c in cats]
                fig = go.Figure(go.Bar(x=labs,y=vals,marker_color=[C["secondary"],C["blue_light"],C["purple"],C["warning"]],
                    text=[f"{v:.2f}" for v in vals],textposition="outside"))
                fig.update_layout(yaxis_range=[0,5.5]); st.plotly_chart(plot_layout(fig,380),width="stretch")
                st.markdown('</div>',unsafe_allow_html=True)
            with cr:
                st.markdown('<div class="chart-box">',unsafe_allow_html=True)
                nd = survey["Recommendation_Score"].value_counts().sort_index()
                clrs = [C["danger"] if s<=6 else (C["warning"] if s<=8 else C["success"]) for s in nd.index]
                fig = go.Figure(go.Bar(x=nd.index,y=nd.values,marker_color=clrs,text=nd.values,textposition="outside"))
                fig.update_layout(xaxis=dict(dtick=1)); st.plotly_chart(plot_layout(fig,380),width="stretch")
                st.markdown('</div>',unsafe_allow_html=True)
        else:
            st.warning("Run `generate_survey_data.py` first.")

    with st3:
        if dropout is not None:
            c1,c2,c3 = st.columns(3)
            with c1: st.markdown(kpi("🚪","Dropouts",f"{len(dropout)}"),unsafe_allow_html=True)
            with c2: st.markdown(kpi("📉","Rate",f"{len(dropout)/len(students)*100:.1f}%","",False),unsafe_allow_html=True)
            with c3:
                if transfer is not None: st.markdown(kpi("🔄","Transfers",f"{len(transfer)}"),unsafe_allow_html=True)
            st.markdown("<br>",unsafe_allow_html=True)
            cl,cr = st.columns(2)
            with cl:
                rc2 = dropout["Dropout_Reason"].value_counts()
                fig = go.Figure(go.Pie(labels=rc2.index,values=rc2.values,hole=.45,marker_colors=px.colors.qualitative.Set2,textinfo="label+percent"))
                st.plotly_chart(plot_layout(fig,380),width="stretch")
            with cr:
                dc = dropout["Class"].value_counts().sort_index()
                fig = go.Figure(go.Bar(x=[f"Class {c}" for c in dc.index],y=dc.values,marker_color=C["danger"],text=dc.values,textposition="outside"))
                st.plotly_chart(plot_layout(fig,380),width="stretch")
            st.dataframe(dropout,width="stretch",hide_index=True)
        else:
            st.warning("Run `generate_simulation_data.py` first.")
