import streamlit as st
from utils.i18n import get_text
from utils.styling import apply_styling
from utils.data_engine import DataEngine

# Page Config
st.set_page_config(
    page_title="Industrial Insight Tool",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Utils
data_engine = DataEngine()

# Sidebar Configuration
with st.sidebar:
    st.title("Human and operational performance insight tool")
    
    # Language Selector
    lang = st.radio("Language / Idioma", ["EN", "ES"], horizontal=True)
    
    # Theme Selector
    theme = st.selectbox(
        get_text("theme", lang), 
        ["Dark Industrial", "Navy Blue", "Light Corporate"]
    )
    st.session_state.theme = theme # Store for modules to use if needed
    
    st.markdown("---")
    
    # Navigation
    menu_options = {
        "dashboard": get_text("nav_dashboard", lang),
        "workforce": get_text("nav_workforce", lang),
        "operations": get_text("nav_operations", lang),
        "skills": get_text("nav_skills", lang),
        "ci": get_text("nav_ci", lang),
        "kanban": get_text("nav_kanban", lang),
        "reports": get_text("nav_reports", lang),
    }
    
    selection = st.radio("Navigation", list(menu_options.values()), label_visibility="collapsed")
    
    st.markdown("---")
    st.caption(get_text("disclaimer", lang))

# Apply Custom Styling
apply_styling(theme)

# Routing
import modules.dashboard as dashboard
import modules.workforce as workforce
import modules.operations as operations
import modules.skills as skills
import modules.ci_engine as ci_engine
import modules.kanban as kanban
import modules.reports as reports

# Map selection back to key
selected_key = [k for k, v in menu_options.items() if v == selection][0]

if selected_key == "dashboard":
    dashboard.show(data_engine, lang)
elif selected_key == "workforce":
    workforce.show(data_engine, lang)
elif selected_key == "operations":
    operations.show(data_engine, lang)
elif selected_key == "skills":
    skills.show(data_engine, lang)
elif selected_key == "ci":
    ci_engine.show(data_engine, lang)
elif selected_key == "kanban":
    kanban.show(data_engine, lang)
elif selected_key == "reports":
    reports.show(data_engine, lang)

