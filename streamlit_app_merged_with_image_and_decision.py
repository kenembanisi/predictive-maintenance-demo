
import streamlit as st
import joblib
import numpy as np
from PIL import Image
import random

# Load model and scaler
model = joblib.load("pump_failure_model.pkl")
scaler = joblib.load("pump_scaler.pkl")

# Page setup
st.set_page_config(page_title="Predictive Maintenance Demo", layout="wide")


# Title
st.title("🔧 Predictive Maintenance Demo: Smart Pump Monitoring")


# Show image in a column (1/3 width)
_, centre_col, _ = st.columns([1, 2, 2])
with centre_col:
    st.image("centrifugal-pump-11.jpg", caption="Real Centrifugal Pump", use_container_width=True)


# Tabs
tabs = st.tabs(["Live Sensor Control", "Decision-Making Scenario"])

# ---------------- Tab 1 ----------------
with tabs[0]:
    # st.sidebar.header("Adjust Sensor Readings")
    # vibration = st.sidebar.slider("Vibration (mm/s)", 0.0, 10.0, 3.0, 0.1)
    # temperature = st.sidebar.slider("Temperature (°C)", 30.0, 120.0, 60.0, 1.0)
    # rpm = st.sidebar.slider("RPM", 1500, 2000, 1750, 10)

    col1, _ = st.columns([1, 2])
    with col1:
        st.subheader("🔧 Adjust Sensor Readings")

        # Sensor input sliders
        vibration = st.slider("Vibration (mm/s) (Range: 0–10 mm/s)", 0.0, 10.0, 3.0, 0.1)
        temperature = st.slider("Temperature (°C) (Range: 30–120 °C)", 30.0, 120.0, 60.0, 1.0)
        rpm = st.slider("RPM (Range: 1500–2000)", 1500, 2000, 1750, 10)


    # Prediction
    input_scaled = scaler.transform([[vibration, temperature, rpm]])
    failure_prob = model.predict_proba(input_scaled)[0][1]

    # Status levels
    if failure_prob > 0.8:
        status = "🔴 CRITICAL"
        pump_color = "#cc0000"
        motor_color = "#cc0000"
        heat_glow = "0 0 20px 5px red"
    elif failure_prob > 0.4:
        status = "🟠 Monitor"
        pump_color = "#e69500"
        motor_color = "#e69500"
        heat_glow = "0 0 10px 3px orange"
    else:
        status = "🟢 OK"
        pump_color = "#2eb82e"
        motor_color = "#2eb82e"
        heat_glow = "none"

    vibration_anim = "vibrate 0.3s infinite" if vibration > 6.5 else "none"

    # Digital twin visualization
    digital_twin = f"""
    <style>
    .pump-container {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        padding: 20px;
    }}
    .pump-part {{
        height: 120px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-family: sans-serif;
    }}
    .pump-housing {{
        width: 100px;
        background-color: {pump_color};
        animation: {vibration_anim};
    }}
    .shaft {{
        width: 60px;
        background-color: red;
    }}
    .motor {{
        width: 140px;
        background-color: {motor_color};
        box-shadow: {heat_glow};
    }}
    .sensor-data {{
        text-align: center;
        font-size: 14px;
        margin-top: 10px;
        font-family: monospace;
    }}
    @keyframes vibrate {{
        0% {{ transform: translateX(-2px); }}
        50% {{ transform: translateX(2px); }}
        100% {{ transform: translateX(-2px); }}
    }}
    </style>

    <div class="pump-container">
        <div class="pump-part pump-housing">Pump</div>
        <div class="pump-part shaft">Shaft</div>
        <div class="pump-part motor">Motor</div>
    </div>
    <div class="sensor-data">
        <div>Vibration: <strong>{vibration:.2f} mm/s</strong> | Temperature: <strong>{temperature:.2f} °C</strong> | RPM: <strong>{rpm}</strong></div>
    </div>
    """

    # Estimate RUL based on failure probability
    if failure_prob > 0.8:
        rul_hours = random.randint(1, 12)
        rul = f"{rul_hours} hours"
    elif failure_prob > 0.6:
        rul_hours = random.randint(12, 48)
        rul = f"{rul_hours} hours"
    elif failure_prob > 0.4:
        rul_days = random.randint(2, 5)
        rul = f"{rul_days} days"
    elif failure_prob > 0.2:
        rul_days = random.randint(5, 10)
        rul = f"{rul_days} days"
    else:
        rul_days = random.randint(10, 30)
        rul = f"{rul_days} days"

    # Show RUL estimate
    rul_col, _ = st.columns([1, 1])
    


     # Metrics in row
    mcol1, mcol2, mcol3 = st.columns([1, 1, 1])
    with mcol1:
        st.metric(label="Failure Probability", value=f"{failure_prob*100:.2f}%")
    with mcol2:
        st.metric(label="Maintenance Status", value=status)
    with mcol3:
        st.metric(label="🕒 Estimated Remaining Useful Life (RUL)", value=rul)

    # Visual twin
    st.subheader("🧠 Digital Twin Visualization")
    st.markdown(digital_twin, unsafe_allow_html=True)

    # Sensor readings
    # st.subheader("🔍 Sensor Readings")
    # st.write({
    #     "Vibration (mm/s)": vibration,
    #     "Temperature (°C)": temperature,
    #     "RPM": rpm
    # })

# ---------------- Tab 2 ----------------
with tabs[1]:
    st.subheader("🎯 Scenario: Anomaly Detected")
    st.markdown("A pump is showing unusual sensor readings. What would you do based on the available data?")

    # Refresh scenario
    if "scenario" not in st.session_state or st.button("🔁 Refresh Scenario"):
        st.session_state["scenario"] = {
            "vibration": round(random.uniform(5.5, 9.5), 2),
            "temperature": round(random.uniform(85.0, 110.0), 2),
            "rpm": int(random.uniform(1600, 1900))
        }

    scenario = st.session_state["scenario"]

    # Display simulated scenario
    st.write(f"**Vibration:** {scenario['vibration']} mm/s (Range: 0–10 mm/s)")
    st.write(f"**Temperature:** {scenario['temperature']} °C (Range: 30–120 °C)")
    st.write(f"**RPM:** {scenario['rpm']} (Range: 1500–2000)")

    # Decision input
    user_decision = st.radio("Choose your action:", ["Continue Operation", "Schedule Maintenance", "Shut Down Immediately"])

    # Run prediction
    sim_input_scaled = scaler.transform([[scenario['vibration'], scenario['temperature'], scenario['rpm']]])
    sim_failure_prob = model.predict_proba(sim_input_scaled)[0][1]
    sim_status = model.predict(sim_input_scaled)[0]

    # Reveal result
    if st.button("Reveal AI Recommendation and Outcome"):
        st.write("**AI Failure Probability:** {:.2f}%".format(sim_failure_prob * 100))
        if sim_status == 1:
            st.write("**AI Recommendation:** 🔴 High Risk — Maintenance Required Immediately")
        else:
            st.write("**AI Recommendation:** 🟢 Low Risk — Continue Operation")

        # Outcome feedback
        if user_decision == "Continue Operation":
            if sim_status == 1:
                st.error("Pump failed after 6 hours. 🚨 Cost: $150,000 in downtime.")
            else:
                st.success("Pump continued to operate normally.")
        elif user_decision == "Schedule Maintenance":
            if sim_status == 1:
                st.success("Failure prevented. Cost of scheduled maintenance: $15,000.")
            else:
                st.info("Preventive maintenance performed. No failure was imminent.")
        else:
            st.warning("Production paused. Cost: $50,000. But failure risk averted.")
