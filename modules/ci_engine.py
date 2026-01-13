import streamlit as st
from utils.i18n import get_text
from utils.recommendations import RecommendationEngine

def show(data_engine, lang):
    st.markdown(f"## {get_text('nav_ci', lang)}")
    
    st.markdown(f"""
    <div style='background-color: rgba(0, 100, 255, 0.1); padding: 20px; border-radius: 5px; border-left: 5px solid #0056b3;'>
        <h4>{get_text('rec_title', lang)}</h4>
        <p>{get_text('rec_sub', lang)}</p>
    </div>
    <br>
    """, unsafe_allow_html=True)
    
    if st.button("Run Analysis Engine"):
        with st.spinner("Analyzing operational signals..."):
            df_wf = st.session_state.get("df_wf")
            df_ops = st.session_state.get("df_ops")
            
            engine = RecommendationEngine(df_wf, df_ops)
            recommendations = engine.analyze_priorities()
            
            if not recommendations.empty:
                for index, row in recommendations.iterrows():
                    priority_color = "red" if row["Priority"] == "Critical" else "orange" if row["Priority"] == "High" else "blue"
                    
                    with st.container():
                        st.markdown(f"""
                        <div class='kpi-card' style='text-align: left; border-left: 5px solid {priority_color}; margin-bottom: 20px;'>
                            <h4>[{row['Priority']}] {row['Sector']} - {row['Methodology']}</h4>
                            <p><strong>Diagnosis:</strong> {row['Message']}</p>
                            <p><strong>Suggested Action:</strong> {row['Action']}</p>
                            <small>Type: {row['Type']}</small>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("System optimized. No critical deviations found.")
