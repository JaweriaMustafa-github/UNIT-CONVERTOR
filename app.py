# Project2: Unit Converter with Streamlit
import streamlit as st

# Set page config
st.set_page_config(
    page_title="Smart Unit Converter",
    layout="wide"
)

# Custom CSS for themes
custom_css = {
    "light": """
        <style>
        .stApp {
            background-color: #ffffff;
            color: #000000;
        }
        .stButton button {
            background-color: white !important;
            color: black !important;
            border: 2px solid black !important;
            transition: all 0.3s ease !important;
        }
        .stButton button:hover {
            background-color: black !important;
            color: white !important;
            border: 2px solid white !important;
        }
        .stSelectbox, .stNumberInput {
            background-color: #f0f2f6;
        }
        </style>
    """,
    "dark": """
        <style>
        .stApp {
            background-color: #1e1e1e;
        }
        .stMarkdown p, .stSelectbox label, .stNumberInput label {
            background-image: linear-gradient(45deg, #FFD700, #B7410E);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        h1, h2, h3 {
            background-image: linear-gradient(45deg, #FFD700, #B7410E);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold;
        }
        .stSelectbox, .stNumberInput {
            background-color: #2d2d2d;
            color: white;
        }
        .stButton button {
            background-color: white !important;
            color: black !important;
            border: 2px solid black !important;
            transition: all 0.3s ease !important;
        }
        .stButton button:hover {
            background-color: black !important;
            color: white !important;
            border: 2px solid white !important;
        }
        .history-entry {
            background-image: linear-gradient(45deg, #FFD700, #B7410E);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold;
        }
        </style>
    """,
    "gradient": """
        <style>
        .stApp {
            background: linear-gradient(135deg, #833ab4, #fd1d1d, #405de6);
            color: #ffffff;
        }
        .stButton button {
            background-color: white !important;
            color: black !important;
            border: 2px solid black !important;
            transition: all 0.3s ease !important;
        }
        .stButton button:hover {
            background-color: black !important;
            color: white !important;
            border: 2px solid white !important;
        }
        .stSelectbox, .stNumberInput {
            background-color: rgba(255, 255, 255, 0.1);
        }
        </style>
    """
}

# Initialize theme in session state if not present
if 'theme' not in st.session_state:
    st.session_state.theme = "light"

# Initialize history if not present
if 'conversion_history' not in st.session_state:
    st.session_state.conversion_history = []

# Sidebar settings
with st.sidebar:
    st.title("Settings")
    selected_theme = st.selectbox(
        "Choose Theme",
        ["Light", "Dark", "Gradient"],
        index=["Light", "Dark", "Gradient"].index(st.session_state.theme.capitalize())
    )
    
    if selected_theme.lower() != st.session_state.theme:
        st.session_state.theme = selected_theme.lower()
        st.rerun()

# Apply the selected theme
st.markdown(custom_css[st.session_state.theme], unsafe_allow_html=True)

# Converter styles
converter_styles = {
    "light": {
        "success": "background-color: #e8f5e9; color: #2e7d32; padding: 10px; border-radius: 5px;",
        "error": "background-color: #ffebee; color: #c62828; padding: 10px; border-radius: 5px;"
    },
    "dark": {
        "success": "background-color: #1b5e20; color: #ffffff; padding: 10px; border-radius: 5px;",
        "error": "background-color: #b71c1c; color: #ffffff; padding: 10px; border-radius: 5px;"
    },
    "gradient": {
        "success": "background-color: rgba(255, 255, 255, 0.2); color: #ffffff; padding: 10px; border-radius: 5px;",
        "error": "background-color: rgba(255, 0, 0, 0.3); color: #ffffff; padding: 10px; border-radius: 5px;"
    }
}

def convert_temperature(value, from_unit, to_unit):
    if from_unit == "Fahrenheit":
        celsius = (value - 32) * 5/9
    elif from_unit == "Kelvin":
        celsius = value - 273.15
    else:
        celsius = value

    if to_unit == "Fahrenheit":
        return celsius * 9/5 + 32
    elif to_unit == "Kelvin":
        return celsius + 273.15
    else:
        return celsius

def get_conversion_factors(category):
    if category == "Length":
        return {
            "Meters": 1,
            "Kilometers": 1000,
            "Miles": 1609.34,
            "Feet": 0.3048,
            "Inches": 0.0254
        }
    elif category == "Weight":
        return {
            "Kilograms": 1,
            "Grams": 0.001,
            "Pounds": 0.453592,
            "Ounces": 0.0283495
        }
    elif category == "Speed":
        return {
            "m/s": 1,
            "km/h": 0.277778,
            "mph": 0.44704
        }
    elif category == "Area":
        return {
            "Square Meters": 1,
            "Square Kilometers": 1e6,
            "Acres": 4046.86,
            "Hectares": 10000,
            "Square Feet": 0.092903
        }

def perform_conversion(category, value, from_unit, to_unit):
    try:
        if category == "Temperature":
            return convert_temperature(value, from_unit, to_unit)
        else:
            conversion_factors = get_conversion_factors(category)
            base_value = value * conversion_factors[from_unit]
            return base_value / conversion_factors[to_unit]
    except Exception as e:
        raise ValueError(f"Conversion error: {str(e)}")

# Main Title
st.title("Smart Unit Converter")

# Conversion categories
categories = ["Length", "Weight", "Temperature", "Speed", "Area"]
units = {
    "Length": ["Meters", "Kilometers", "Miles", "Feet", "Inches"],
    "Weight": ["Kilograms", "Grams", "Pounds", "Ounces"],
    "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
    "Speed": ["m/s", "km/h", "mph"],
    "Area": ["Square Meters", "Square Kilometers", "Acres", "Hectares", "Square Feet"]
}

# Input Layout
col1, col2, col3 = st.columns(3)
with col1:
    category = st.selectbox("Select Category", categories)
    value = st.number_input("Enter Value", value=0.0)
with col2:
    from_unit = st.selectbox("From Unit", units[category])
with col3:
    to_unit = st.selectbox("To Unit", units[category])

# Convert Button
if from_unit == to_unit:
    st.warning("Please select different units to convert.")
elif st.button("Convert"):

    try:
        result = perform_conversion(category, value, from_unit, to_unit)
        result_str = f"{value} {from_unit} = {result:.2f} {to_unit}"
        st.markdown(
            f"""<div style="{converter_styles[st.session_state.theme]['success']}">
                Result: {result_str}
            </div>""",
            unsafe_allow_html=True
        )

        # Add to history
        st.session_state.conversion_history.append(result_str)

    except Exception as e:
        st.markdown(
            f"""<div style="{converter_styles[st.session_state.theme]['error']}">
                An error occurred: {str(e)}
            </div>""",
            unsafe_allow_html=True
        )

# Show History
if st.session_state.conversion_history:
    st.markdown("### Conversion History")
    for entry in st.session_state.conversion_history[::-1]:
        st.markdown(f'<div class="history-entry">{entry}</div>', unsafe_allow_html=True)
