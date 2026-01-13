import streamlit as st

def apply_styling(theme):
    """
    Applies custom CSS based on the selected theme.
    Themes: 'Dark Industrial', 'Navy Blue', 'Light Corporate'
    """
    
    # Base CSS common to all themes
    base_css = """
<style>
    /* General Layout */
    .main {
        padding-top: 2rem;
    }
    h1, h2, h3 {
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        font-weight: 600;
    }
    .stButton>button {
        width: 100%;
        border-radius: 4px;
        font-weight: 500;
    }
    /* KPI Card Style */
    .kpi-card {
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: bold;
    }
    .kpi-label {
        font-size: 1rem;
        opacity: 0.8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Print Styles */
    @media print {
        .stSidebar, header, footer, .stButton {
            display: none !important;
        }
        .main {
            padding: 0 !important;
            margin: 0 !important;
            background-color: white !important;
            color: black !important;
        }
        body {
            transform: scale(0.9);
            -webkit-print-color-adjust: exact;
        }
        .kpi-card {
            border: 1px solid #ccc;
            box-shadow: none;
            page-break-inside: avoid;
        }
    }
</style>
"""
    
    # Theme Specific CSS
    theme_css = ""
    
    if theme == "Dark Industrial":
        theme_css = """
<style>
    /* Dark Industrial Theme */
    .stApp {
        background-color: #1e1e1e;
        color: #e0e0e0;
    }
    .kpi-card {
        background-color: #2d2d2d;
        border-left: 5px solid #ffcc00; /* Safety Yellow Accent */
    }
    h1, h2, h3 {
        color: #ffffff;
    }
    .stSidebar {
        background-color: #252526;
    }
    .stDataFrame {
        border: 1px solid #444;
    }
</style>
"""
    elif theme == "Navy Blue":
        theme_css = """
<style>
    /* Navy Blue Theme */
    .stApp {
        background-color: #0d1b2a;
        color: #e0e1dd;
    }
    .kpi-card {
        background-color: #1b263b;
        border-left: 5px solid #415a77;
    }
    h1, h2, h3 {
        color: #ffffff;
    }
    .stSidebar {
        background-color: #1b263b;
    }
</style>
"""
    else: # Light Corporate
        theme_css = """
<style>
    /* Light Corporate Theme */
    .stApp {
        background-color: #f4f6f9;
        color: #333333;
    }
    
    /* Card Backgrounds */
    .kpi-card {
        background-color: #ffffff;
        border-left: 5px solid #0056b3;
        color: #333333;
    }
    
    /* Headers - Force Dark Blue */
    h1, h2, h3, h4, h5, h6 {
        color: #2c3e50 !important;
    }
    
    /* Sidebar Styling */
    .stSidebar {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }
    
    /* Specific Text Elements on Light Backgrounds */
    .stSidebar [data-testid="stMarkdownContainer"] p, 
    .stSidebar [data-testid="stMarkdownContainer"] span, 
    .stSidebar [data-testid="stMarkdownContainer"] div,
    .main [data-testid="stMarkdownContainer"] p,
    .main [data-testid="stMarkdownContainer"] li {
        color: #333333 !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #2c3e50 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #555555 !important;
    }
    
    /* Inputs Labels */
    .stSelectbox label p, .stRadio label p, .stTextInput label p {
        color: #333333 !important;
    }
    
    /* DataFrames */
    .stDataFrame {
        color: #333333;
    }
    
    /* Tab Headers */
    button[data-baseweb="tab"] div {
        color: #333333 !important;
    }
    
    /* Fix: Ensure items inside dark buttons stay white (or default) */
    .stButton button p {
        color: inherit !important;
    }
</style>
"""

    st.markdown(base_css + theme_css, unsafe_allow_html=True)

def render_kpi(label, value, delta=None, color=""):
    """
    Helper to match the custom CSS KPI card
    """
    delta_html = ""
    if delta:
        delta_color = "green" if "+" in str(delta) else "red"
        delta_html = f"<div style='color: {delta_color}; font-size: 0.9rem; margin-top: 5px;'>{delta}</div>"
        
    html = f"""
    <div class="kpi-card">
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
        {delta_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
