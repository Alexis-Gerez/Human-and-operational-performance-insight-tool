import streamlit as st
import plotly.express as px
from utils.i18n import get_text
from utils.styling import render_kpi

def show(data_engine, lang):
    st.markdown(f"## {get_text('nav_dashboard', lang)}")
    
    # Load Data
    if "df_ops" not in st.session_state:
        st.session_state.df_ops = data_engine.generate_operational_data()
    if "df_wf" not in st.session_state:
        st.session_state.df_wf = data_engine.generate_workforce_data()
        
    df_ops = st.session_state.df_ops
    df_wf = st.session_state.df_wf
    
    # High Level KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    total_employees = len(df_wf)
    avg_efficiency = df_ops["Efficiency_Pct"].mean()
    total_incidents = df_ops["Incidents"].sum()
    
    with col1:
        render_kpi(get_text("kpi_workforce", lang), total_employees, "+2")
    with col2:
        render_kpi(get_text("kpi_efficiency", lang), f"{avg_efficiency:.1f}%", "-1.2%")
    with col3:
        render_kpi(get_text("kpi_incidents", lang), total_incidents, "-3")
    with col4:
        # Dummy value for open actions
        render_kpi(get_text("kpi_actions", lang), "12", "+4")
        
    st.markdown("---")
    
    # Charts Row 1
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader(get_text("op_perf", lang))
        # Daily efficiency trend
        daily_eff = df_ops.groupby("Date")[["Efficiency_Pct"]].mean().reset_index()
        fig_eff = px.line(daily_eff, x="Date", y="Efficiency_Pct", markers=True, height=350)
        fig_eff.update_layout(template="plotly_dark" if "Dark" in st.session_state.get("theme", "") else "plotly_white")
        st.plotly_chart(fig_eff, use_container_width=True)
        
    with c2:
        st.subheader(get_text("wf_dist", lang))
        # Headcount by Sector
        sector_counts = df_wf["Sector"].value_counts().reset_index()
        sector_counts.columns = ["Sector", "Count"]
        fig_dist = px.pie(sector_counts, names="Sector", values="Count", hole=0.4, height=350)
        st.plotly_chart(fig_dist, use_container_width=True)
