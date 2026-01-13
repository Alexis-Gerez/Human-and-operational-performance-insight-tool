import streamlit as st
import plotly.express as px
from utils.i18n import get_text

def show(data_engine, lang):
    st.markdown(f"## {get_text('nav_operations', lang)}")
    
    df_ops = st.session_state.get("df_ops", data_engine.generate_operational_data())
    
    # Filters
    selected_sector = st.selectbox("Filter by Sector", ["All"] + list(df_ops["Sector"].unique()))
    
    if selected_sector != "All":
        df_view = df_ops[df_ops["Sector"] == selected_sector]
    else:
        df_view = df_ops
        
    # Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Avg Production", int(df_view["Production_Volume"].mean()))
    c2.metric("Avg Efficiency", f"{df_view['Efficiency_Pct'].mean():.1f}%")
    c3.metric("Total Scrap", int(df_view["Scrap_Count"].sum()))
    
    st.markdown("### Process Stability")
    
    # Control Chart-ish view
    fig_proc = px.scatter(df_view, x="Date", y="Efficiency_Pct", color="Sector", size="Production_Volume", hover_data=["Incidents"])
    # Add standard line
    fig_proc.add_hline(y=100, line_dash="dash", line_color="green", annotation_text="Target")
    fig_proc.add_hline(y=85, line_dash="dot", line_color="orange", annotation_text="Warning")
    
    st.plotly_chart(fig_proc, use_container_width=True)
    
    # Pareto of Defects
    # Converting row-wise defects to aggregate for visual
    # (Simulating defect types would be better, but we use Rework/Scrap split)
    
    st.markdown("### Quality Cost Analysis (Pareto)")
    agg_qual = df_view.groupby("Sector")[["Rework_Count", "Scrap_Count"]].sum().reset_index()
    agg_qual = agg_qual.melt(id_vars="Sector", value_vars=["Rework_Count", "Scrap_Count"], var_name="Type", value_name="Count")
    
    fig_qual = px.bar(agg_qual, x="Sector", y="Count", color="Type", title="Defects Distribution (Rework vs Scrap)")
    st.plotly_chart(fig_qual, use_container_width=True)
