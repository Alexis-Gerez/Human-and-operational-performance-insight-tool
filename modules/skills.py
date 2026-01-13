import streamlit as st
import plotly.express as px
from utils.i18n import get_text

def show(data_engine, lang):
    st.markdown(f"## {get_text('nav_skills', lang)}")
    
    df_wf = st.session_state.get("df_wf", data_engine.generate_workforce_data())
    
    # Matrix View
    st.markdown("### Skill Matrix View")
    
    # Heatmap setup: Sector vs Role vs Polyvalence
    # We aggregate to prevent too many rows
    matrix_data = df_wf.pivot_table(index="Sector", columns="Role", values="Polyvalence_Score", aggfunc="mean").fillna(0)
    
    fig_hm = px.imshow(matrix_data, text_auto=True, color_continuous_scale="Blues", title="Avg Polyvalence by Role & Sector")
    st.plotly_chart(fig_hm, use_container_width=True)
    
    # Training Needs
    st.markdown(f"### {get_text('tr_needs', lang)}")
    
    # Filter employees with low polyvalence (<40)
    training_candidates = df_wf[df_wf["Polyvalence_Score"] < 50][["ID", "Role", "Sector", "Polyvalence_Score", "Seniority_Years"]]
    
    if not training_candidates.empty:
        st.warning(f"Detected {len(training_candidates)} employees with critical skill gaps.")
        st.dataframe(training_candidates.style.background_gradient(subset=["Polyvalence_Score"], cmap="Reds"), use_container_width=True)
    else:
        st.success("No critical skill gaps detected.")
