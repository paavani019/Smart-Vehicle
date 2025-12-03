import streamlit as st
import requests

# --- PAGE CONFIG ---
st.set_page_config(page_title="Vehicle Health Dashboard", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
        /* Background gradient */
        body, .stApp {
            background: radial-gradient(1000px 600px at 50% -200px, #1f2a37 0%, #0f172a 40%, #0b1220 100%);
            color: #f8fafc;
        }

        /* Main title */
        h1 {
            color: #ffffff !important;
            text-align: center;
            font-family: 'Segoe UI', system-ui, sans-serif;
            font-size: 2.8rem;
            font-weight: 800;
            margin-bottom: 0.3rem;
        }

        /* Subtitle under title */
        .subtitle {
            text-align: center;
            color: #cbd5e1;
            margin-bottom: 1.5rem;
        }

        /* Card container */
        .card {
            background: #ffffff12;
            padding: 1.8rem 2rem;
            border-radius: 22px;
            box-shadow: 0 6px 28px rgba(0,0,0,0.35);
            backdrop-filter: blur(10px);
            border: 1px solid #a78bfa33;
        }

        /* Lavender labels & subheaders */
        label, h2, h3, .stSubheader {
            color: #a78bfa !important;
            font-weight: 700 !important;
        }

        /* Button styling - lavender accent */
        div.stButton > button {
            background-color: #a78bfa;
            color: #ffffff;
            font-weight: 700;
            border-radius: 10px;
            border: none;
            height: 3rem;
            width: 100%;
            transition: transform .06s ease, background-color .15s ease;
            box-shadow: 0 8px 20px rgba(167,139,250,0.3);
        }
        div.stButton > button:hover {
            background-color: #c4b5fd;
            transform: translateY(-1px);
            color: #000000;
        }
    .block-container { padding-top: 2rem; }
/* Remove unwanted input shadows */
input, textarea, [data-baseweb="input"] {
    background: none !important;
    border: none !important;
    box-shadow: none !important;
}
</style>

""", unsafe_allow_html=True)

# --- TITLE ---
st.markdown("<h1>🚗 Vehicle Health & Maintenance Prediction</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Simulate vehicle telemetry and predict maintenance status in real-time.</p>", unsafe_allow_html=True)
st.markdown("<div style='margin-top:0px;'></div>", unsafe_allow_html=True)

# --- LAYOUT ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 Input Vehicle Telemetry")

    # sliders for telemetry input
    battery = st.slider("Battery Health (%)", 0, 100, 80)
    engine_temp = st.slider("Engine Temperature (°C)", 60, 130, 95)
    oil_pressure = st.slider("Oil Pressure", 0, 50, 30)
    mileage = st.slider("Mileage Since Last Service (km)", 0, 20000, 8000)

    # predict button
    if st.button("🔍 Predict Vehicle Health"):
        payload = {
            "battery_health": battery,
            "engine_temp": engine_temp,
            "oil_pressure": oil_pressure,
            "mileage_since_service": mileage
        }
        try:
            res = requests.post("http://127.0.0.1:8000/maintenance/predict", json=payload, timeout=10)
            result = res.json()
            score = result.get("health_score", "—")
            status = result.get("status", "—")

            # color-coded status chip
            if status == "OK":
                bg = "#16a34a"   # green
            elif isinstance(score, (int, float)) and score > 60:
                bg = "#d97706"   # amber
            else:
                bg = "#dc2626"   # red

            st.markdown(f"""
                <div style='text-align:center; margin-top:18px;'>
                    <h3 style='color:#a78bfa; margin-bottom:6px;'>Predicted Health Score</h3>
                    <div style='font-size:44px; font-weight:900; color:#ffffff; line-height:1;'>{score}</div>
                    <div style='margin-top:10px; background:{bg}; color:#ffffff; padding:10px 14px; border-radius:12px; display:inline-block; font-weight:800; letter-spacing:.3px;'>
                        Status: {status}
                    </div>
                </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"⚠️ Error contacting backend: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

# --- FOOTER CREDIT ---
st.markdown("""
    <hr style='margin-top:3rem; border: 1px solid #a78bfa33;'/>
    <p style='text-align:center; color:#a78bfa; font-size:0.9rem; margin-top:0.8rem;'>
        Developed by <b>Paavani Karuturi</b> – CMPE 281, San José State University
    </p>
""", unsafe_allow_html=True)

