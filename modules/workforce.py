import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from utils.i18n import get_text

def show(data_engine, lang):
    st.markdown(f"## {get_text('nav_workforce', lang)}")
    
    df_wf = st.session_state.get("df_wf", data_engine.generate_workforce_data())
    
    # Tabs for different levels of analysis
    tab1, tab2, tab3 = st.tabs([
        get_text("wf_dist", lang), 
        get_text("wf_absent", lang),
        "👤 Individual Detail" if lang == "EN" else "👤 Detalle Individual"
    ])
    
    with tab1:
        st.dataframe(df_wf, use_container_width=True, height=300)
        
        c1, c2 = st.columns(2)
        with c1:
            # Distribution by Role
            fig_role = px.bar(df_wf["Role"].value_counts().reset_index(), x="Role", y="count", color="Role")
            st.plotly_chart(fig_role, use_container_width=True)
            
        with c2:
            # Seniority Distribution histogram
            fig_sen = px.histogram(df_wf, x="Seniority_Years", nbins=15, title="Seniority Dist.")
            st.plotly_chart(fig_sen, use_container_width=True)
            
    with tab2:
        # Absenteeism analysis
        avg_abs = df_wf.groupby("Sector")["Absenteeism_Days"].mean().reset_index().sort_values("Absenteeism_Days", ascending=False)
        fig_abs = px.bar(avg_abs, x="Sector", y="Absenteeism_Days", color="Absenteeism_Days", color_continuous_scale="Reds")
        st.plotly_chart(fig_abs, use_container_width=True)
        
        st.info("High absenteeism in a sector correlates strongly with lower efficiency and higher incident risk." if lang == "EN" else "El ausentismo alto en un sector se correlaciona fuertemente con menor eficiencia y mayor riesgo de incidentes.")

    with tab3:
        st.markdown("### " + ("Employee Performance profile" if lang == "EN" else "Perfil de Desempeño del Empleado"))
        
        # Selector
        employee_ids = df_wf["ID"].tolist()
        selected_id = st.selectbox("Select Employee / Seleccionar Empleado", employee_ids)
        
        # Get Employee Data
        employee = df_wf[df_wf["ID"] == selected_id].iloc[0]
        
        # Profile Card
        with st.container():
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Role / Rol", employee["Role"])
            col2.metric("Sector", employee["Sector"])
            col3.metric("Category / Categoría", employee["Category"])
            col4.metric("Seniority / Antigüedad", f"{employee['Seniority_Years']} Yrs")
            
        st.divider()
        
        # Simulate History Data for this specific employee (on the fly)
        # We simulate 12 months of data based on their current stats
        months = pd.date_range(end=pd.Timestamp.now(), periods=12, freq='M')
        
        # Efficiency Trend (Monthly)
        # Base efficiency around 85-95%, slightly random
        base_eff = np.random.normal(90, 5)
        eff_trend = np.clip(np.random.normal(base_eff, 3, 12), 70, 100)
        
        # Quality/Defects (Daily-ish aggregated to Monthly for view)
        defects = np.random.poisson(2, 12)
        
        df_history = pd.DataFrame({
            "Date": months,
            "Efficiency": eff_trend,
            "Defects": defects
        })
        
        # Charts
        c_chart1, c_chart2 = st.columns(2)
        
        with c_chart1:
            st.subheader("Monthly Efficiency Trend" if lang == "EN" else "Tendencia Mensual de Eficiencia")
            fig_eff = px.line(df_history, x="Date", y="Efficiency", markers=True)
            fig_eff.add_hline(y=95, line_dash="dash", line_color="green", annotation_text="Target")
            fig_eff.update_yaxes(range=[60, 105])
            st.plotly_chart(fig_eff, use_container_width=True)
            
        with c_chart2:
            st.subheader("Quality Incidents (Last 12 Months)" if lang == "EN" else "Incidentes de Calidad (Últimos 12 Meses)")
            fig_qual = px.bar(df_history, x="Date", y="Defects", color="Defects", color_continuous_scale="Reds")
            st.plotly_chart(fig_qual, use_container_width=True)
            
        # Daily Activity (Last 30 Days Simulation)
        st.subheader("Daily Activity (Last 30 Days)" if lang == "EN" else "Actividad Diaria (Últimos 30 Días)")
        days = pd.date_range(end=pd.Timestamp.now(), periods=30, freq='D')
        daily_output = np.random.normal(100, 10, 30) # Units produced
        
        df_daily = pd.DataFrame({"Date": days, "Units Produced": daily_output})
        fig_daily = px.area(df_daily, x="Date", y="Units Produced")
        st.plotly_chart(fig_daily, use_container_width=True)
