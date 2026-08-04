import base64
import joblib
import pandas as pd
import streamlit as st

SITE_NAME = "HeartSense"
SITE_TAGLINE = "Heart Disease Predictor"
HOME_BACKGROUND_IMAGE = "Heart.jpg"

st.set_page_config(page_title=f"{SITE_NAME} — {SITE_TAGLINE}", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "home"


@st.cache_data
def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


FONT_IMPORT = "@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&display=swap');"

COMMON_CSS = """
header[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 1.5rem; }
[data-testid="stSidebar"] { background: #0f2440 !important; }

/* dropdown list (renders outside the page) */
div[data-baseweb="popover"] li { background: #ffffff !important; color: #111827 !important; }
"""

# Dark text for the white Guidance page (main area only, sidebar stays dark)
LIGHT_PAGE_CSS = """
[data-testid="stMain"] p, [data-testid="stMain"] li, [data-testid="stMain"] span {
    color: #1f2937 !important;
}
[data-testid="stMain"] [data-testid="stExpander"] summary {
    background: #dbeafe !important;
    border-radius: 8px !important;
}
[data-testid="stMain"] [data-testid="stExpander"] summary:hover { background: #bfdbfe !important; }
[data-testid="stMain"] [data-testid="stExpander"] svg { fill: #1e3a8a !important; }
[data-testid="stMain"] [data-testid="stAlert"] * { color: #1e3a8a !important; }
"""


def set_image_background(image_filename, overlay=0.35):
    b64 = get_base64(f"Images/{image_filename}")
    st.markdown(
        f"""
        <style>
        {FONT_IMPORT}
        .stApp {{
            background-image: linear-gradient(rgba(15,36,64,{overlay}), rgba(15,36,64,{overlay})),
                               url("data:image/jpeg;base64,{b64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        {COMMON_CSS}
        </style>
        """,
        unsafe_allow_html=True,
    )


def set_solid_background(color="#0f2440", extra_css=""):
    st.markdown(
        f"<style>{FONT_IMPORT}.stApp {{ background: {color}; }}{COMMON_CSS}{extra_css}</style>",
        unsafe_allow_html=True,
    )


if st.session_state.page == "home":
    set_image_background(HOME_BACKGROUND_IMAGE)
elif st.session_state.page == "prediction":
    set_solid_background("#ffffff")
else:
    set_solid_background("#ffffff", extra_css=LIGHT_PAGE_CSS)


@st.cache_resource
def load_model():
    model = joblib.load("randomforest_model.pkl")
    feature_columns = joblib.load("heart_disease_feature_columns.pkl")
    return model, feature_columns


# Landing / welcome page
if st.session_state.page == "home":
    st.markdown(
        f"""
        <div style='display:flex; flex-direction:column; align-items:center;
                    text-align:center; padding-top:14vh; gap:1.1rem; margin-bottom:1.4rem;'>
            <p style='color:#d4af37; letter-spacing:7px; font-size:1.5rem; font-weight:700; margin:0; line-height:1;'>WELCOME TO</p>
            <h1 style="font-family:'Playfair Display',serif; font-weight:900; font-size:4.5rem; color:#fff; margin:0; line-height:1;">{SITE_NAME}</h1>
            <h2 style="font-family:'Playfair Display',serif; font-weight:900; font-size:2.6rem; color:#fff; margin:0; line-height:1;">{SITE_TAGLINE}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <style>
        [data-testid="stMain"] div.stButton > button {
            background: #ffffff;
            color: #0f2440 !important;
            border: none;
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: 700;
            padding: 0.6rem 1.5rem;
        }
        [data-testid="stMain"] div.stButton > button:hover { background: #d4af37; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    _, mid, _ = st.columns([2, 1, 2])
    with mid:
        if st.button("Start Prediction  →", use_container_width=True):
            st.session_state.page = "prediction"
            st.rerun()

    st.stop()

# Sidebar navigation
NAV_ITEMS = [("home", "🏠 Home"), ("prediction", "❤️ Prediction"), ("guidance", "📋 Guidance")]

with st.sidebar:
    st.markdown(
        f"<h3 style='text-align:center; color:#d4af37;'>❤️ {SITE_NAME}</h3>",
        unsafe_allow_html=True,
    )
    st.divider()
    for key, label in NAV_ITEMS:
        is_active = st.session_state.page == key
        if st.button(label, use_container_width=True, disabled=is_active, key=f"nav_{key}"):
            st.session_state.page = key
            st.rerun()

# Prediction page
if st.session_state.page == "prediction":
    model, feature_columns = load_model()

    st.markdown(
        "<h2 style='text-align:center; color:#123a63; margin-bottom:0.6rem;'>❤️ Heart Disease Predictor</h2>",
        unsafe_allow_html=True,
    )

    CHEST_PAIN_OPTIONS = {
        "Typical angina": 1,
        "Atypical angina": 2,
        "Non-anginal pain": 3,
        "Asymptomatic": 4,
    }
    EKG_OPTIONS = {
        "Normal": 0,
        "ST-T wave abnormality": 1,
        "Probable/definite LV hypertrophy": 2,
    }
    SLOPE_OPTIONS = {"Upsloping": 1, "Flat": 2, "Downsloping": 3}
    THALLIUM_OPTIONS = {"Normal": 3, "Fixed defect": 6, "Reversible defect": 7}

    st.markdown(
        """
        <style>
        .st-key-prediction_form {
            background: linear-gradient(180deg, #14406e 0%, #0f2440 100%);
            border-radius: 14px;
            border: 1px solid #1e4b7a;
            padding: 0.8rem 1.2rem 1rem 1.2rem;
        }
        .st-key-prediction_form * { color: #e2e8f0 !important; }
        .st-key-prediction_form [data-testid="stWidgetLabel"] p {
            text-transform: uppercase;
            font-size: 0.72rem;
            font-weight: 800 !important;
            letter-spacing: 0.6px;
            color: #ffffff !important;
            margin-bottom: 0.15rem !important;
        }
        /* white fields, including the dropdown arrow */
        .st-key-prediction_form [data-testid="stSelectbox"] div,
        .st-key-prediction_form [data-testid="stSelectbox"] span,
        .st-key-prediction_form input,
        .st-key-prediction_form [data-testid="stNumberInputContainer"],
        .st-key-prediction_form [data-testid="stNumberInputStepUp"],
        .st-key-prediction_form [data-testid="stNumberInputStepDown"] {
            background: #ffffff !important;
            color: #111827 !important;
            border-color: #d1d5db !important;
        }
        .st-key-prediction_form svg { fill: #111827 !important; }
        /* labels sit directly on the blue card (beats the white-field rule above) */
        .st-key-prediction_form [data-testid="stWidgetLabel"],
        .st-key-prediction_form [data-testid="stSelectbox"] [data-testid="stWidgetLabel"],
        .st-key-prediction_form [data-testid="stSelectbox"] [data-testid="stWidgetLabel"] div,
        .st-key-prediction_form [data-testid="stSelectbox"] [data-testid="stWidgetLabel"] span,
        .st-key-prediction_form [data-testid="stSelectbox"] [data-testid="stWidgetLabel"] p {
            background: transparent !important;
            color: #ffffff !important;
        }
        .form-title {
            font-weight: 800;
            letter-spacing: 1px;
            font-size: 0.9rem;
            color: #ffffff !important;
            border-bottom: 2px solid rgba(255,255,255,0.25);
            padding-bottom: 0.5rem;
            margin-bottom: 0.4rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True, key="prediction_form"):
        st.markdown("<div class='form-title'>🩺 PATIENT DETAILS</div>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3, gap="medium")

        with col1:
            age = st.number_input("Age", 18, 100, 50)
            sex_label = st.selectbox("Gender", ["Female", "Male"])
            height_cm = st.number_input("Height (cm)", 100, 220, 170)
            weight_kg = st.number_input("Weight (kg)", 30, 200, 70)
            cp_label = st.selectbox("Chest pain type", list(CHEST_PAIN_OPTIONS.keys()))

        with col2:
            bp = st.number_input("Resting blood pressure (BP)", 80, 220, 130)
            chol = st.number_input("Cholesterol (mg/dl)", 100, 600, 240)
            fbs_label = st.selectbox("Fasting blood sugar > 120 mg/dl?", ["No", "Yes"])
            ekg_label = st.selectbox("Resting EKG results", list(EKG_OPTIONS.keys()))
            max_hr = st.number_input("Max heart rate achieved", 60, 220, 150)

        with col3:
            angina_label = st.selectbox("Exercise-induced angina?", ["No", "Yes"])
            st_depression = st.number_input("Old peak (ST depression)", 0.0, 7.0, 1.0, step=0.1)
            slope_label = st.selectbox("Slope of peak exercise ST segment", list(SLOPE_OPTIONS.keys()))
            vessels = st.selectbox("Number of major vessels (0-3)", [0, 1, 2, 3])
            thallium_label = st.selectbox("Thallium stress test result", list(THALLIUM_OPTIONS.keys()))

    # Turn the friendly labels back into the numeric codes the model expects
    input_row = {
        "Age": age,
        "Sex": 1 if sex_label == "Male" else 0,
        "Chest pain type": CHEST_PAIN_OPTIONS[cp_label],
        "BP": bp,
        "Cholesterol": chol,
        "FBS over 120": 1 if fbs_label == "Yes" else 0,
        "EKG results": EKG_OPTIONS[ekg_label],
        "Max HR": max_hr,
        "Exercise angina": 1 if angina_label == "Yes" else 0,
        "ST depression": st_depression,
        "Slope of ST": SLOPE_OPTIONS[slope_label],
        "Number of vessels fluro": vessels,
        "Thallium": THALLIUM_OPTIONS[thallium_label],
    }

    input_df = pd.DataFrame([input_row])[feature_columns]

    st.write("")
    if st.button("❤️ Predict Heart Disease", type="primary", use_container_width=True):
        prediction = model.predict(input_df)[0]
        confidence = model.predict_proba(input_df)[0][prediction]

        if prediction == 1:
            st.error(f"⚠️ Prediction: **Presence** of heart disease  \nConfidence: {confidence:.0%}")
        else:
            st.success(f"✅ Prediction: **Absence** of heart disease  \nConfidence: {confidence:.0%}")

# Guidance page
elif st.session_state.page == "guidance":
    st.markdown(
        "<h1 style='text-align:center; color:#b8860b;'>📋 Guidance for Heart Patients</h1>"
        "<p style='text-align:center;'>General educational information, not medical advice. "
        "Always follow your own doctor's instructions.</p>",
        unsafe_allow_html=True,
    )

    with st.expander("🥗 Diet & Nutrition"):
        st.markdown(
            """
            - Favor vegetables, fruits, whole grains, and lean protein (fish, poultry, legumes).
            - Limit salt, saturated fat, fried food, and added sugar.
            - Watch portion sizes and avoid excess alcohol.
            - Stay hydrated, and keep an eye on fluid intake if your doctor has advised limits.
            """
        )

    with st.expander("🏃 Physical Activity"):
        st.markdown(
            """
            - Aim for at least 30 minutes of moderate activity (walking, cycling, swimming)
              most days of the week, if approved by your doctor.
            - Start slow and build up gradually — don't push through chest pain or dizziness.
            - Include light stretching or rehab exercises if part of a cardiac recovery plan.
            """
        )

    with st.expander("💊 Medication & Checkups"):
        st.markdown(
            """
            - Take prescribed medication exactly as directed — never stop suddenly without medical advice.
            - Keep regular follow-up appointments and monitor BP, cholesterol, and blood sugar.
            - Track your weight; sudden gain can signal fluid retention.
            """
        )

    with st.expander("🚭 Lifestyle Changes"):
        st.markdown(
            """
            - Quit smoking and avoid secondhand smoke — one of the biggest risk reducers available.
            - Manage stress with relaxation techniques, adequate sleep, and social support.
            - Maintain a healthy weight and get regular sleep (7-9 hours).
            """
        )

    with st.expander("🚨 Warning Signs — Seek Emergency Help"):
        st.markdown(
            """
            Call emergency services immediately if you or someone else experiences:
            - Chest pain, pressure, or tightness lasting more than a few minutes
            - Pain spreading to the arm, jaw, neck, or back
            - Shortness of breath, cold sweat, nausea, or lightheadedness
            - Sudden weakness, irregular or racing heartbeat
            """
        )

    st.divider()
    st.info(
        "This page is general education content, not a substitute for "
        "professional medical advice, diagnosis, or treatment."
    )