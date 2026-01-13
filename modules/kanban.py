import streamlit as st
import pandas as pd
from utils.i18n import get_text

def show(data_engine, lang):
    st.markdown(f"## {get_text('nav_kanban', lang)}")
    
    if "kanban_db" not in st.session_state:
        st.session_state.kanban_db = data_engine.generate_initial_kanban()
        
    df_kanban = st.session_state.kanban_db
    
    # Kanban Columns
    c1, c2, c3 = st.columns(3)
    
    cols = {
        "To Do": c1,
        "In Progress": c2,
        "Done": c3
    }
    
    labels = {
        "To Do": get_text("todo", lang),
        "In Progress": get_text("doing", lang),
        "Done": get_text("done", lang)
    }
    
    for status, col in cols.items():
        with col:
            st.markdown(f"### {labels[status]}")
            tasks = df_kanban[df_kanban["Status"] == status]
            
            for idx, task in tasks.iterrows():
                with st.container():
                    st.markdown(f"""
                    <div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 10px; color: black; border: 1px solid #ccc;'>
                        <strong>{task['ID']}</strong><br>
                        {task['Desc']}<br>
                        <small>Owner: {task['Owner']} | Area: {task['Area']}</small>
                        <div style='margin-top: 5px; font-size: 0.8em; background: #ddd; padding: 2px 5px; display: inline-block; border-radius: 3px;'>{task['Type']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
    # Add new task form (Simplified)
    with st.expander("Add New Action"):
        with st.form("new_action"):
            desc = st.text_input("Task Description")
            owner = st.text_input("Owner")
            area = st.selectbox("Area", ["Assembly A", "Assembly B", "Machining", "Quality Control"])
            type_ci = st.selectbox("Type", ["Kaizen", "5S", "Safety", "Lean"])
            submitted = st.form_submit_button("Add Task")
            if submitted:
                 new_task = {"ID": f"ACT-{len(df_kanban)+1:03d}", "Desc": desc, "Owner": owner, "Status": "To Do", "Area": area, "Type": type_ci}
                 st.session_state.kanban_db = pd.concat([df_kanban, pd.DataFrame([new_task])], ignore_index=True)
                 st.rerun()
