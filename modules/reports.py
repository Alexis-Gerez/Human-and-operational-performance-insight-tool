import streamlit as st
import pandas as pd
from utils.i18n import get_text

def show(data_engine, lang):
    st.markdown(f"## {get_text('nav_reports', lang)}")
    
    st.info("Select datasets to generate comprehensive reports. Use the Print button in your browser/system to save as PDF.")
    
    # Export options
    d1 = st.session_state.get("df_wf")
    d2 = st.session_state.get("df_ops")
    d3 = st.session_state.get("kanban_db")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Export Data")
        if d1 is not None:
            csv_wf = d1.to_csv(index=False).encode('utf-8')
            st.download_button("Download Workforce Data (CSV)", csv_wf, "workforce_data.csv", "text/csv")
            
        if d2 is not None:
            csv_ops = d2.to_csv(index=False).encode('utf-8')
            st.download_button("Download Operations Data (CSV)", csv_ops, "operations_data.csv", "text/csv")

    with col2:
        st.markdown("### Print View Mode")
        if st.button("Generate Printable Summary"):
            st.markdown("## EXECUTIVE SUMMARY REPORT")
            st.markdown(f"**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d')}")
            
            st.markdown("### Key Operational Metrics")
            st.table(d2.groupby("Sector")[["Efficiency_Pct", "Incidents", "Rework_Count"]].mean().head())
            
            st.markdown("### Critical Action Plan")
            st.table(d3[d3["Status"] != "Done"])
            
            st.success("Press Ctrl+P (Cmd+P) to print this page.")
