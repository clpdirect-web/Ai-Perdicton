import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="AI Prediction Bot", layout="wide")

st.title("AI Prediction Bot")
st.write("Paper-trading prediction dashboard. No real-money automation.")

if "history" not in st.session_state:
    st.session_state.history = []

st.sidebar.header("Bot Settings")

starting_bankroll = st.sidebar.number_input(
    "Starting Paper Bankroll",
    min_value=100,
    value=1000,
    step=100
)

risk_per_trade = st.sidebar.slider(
    "Risk Per Prediction %",
    min_value=1,
    max_value=10,
    value=2
)

st.header("New Prediction")

event_name = st.text_input("Event / Market Name")

market_probability = st.slider(
    "Market Probability %",
    min_value=1,
    max_value=99,
    value=50
)

signal_strength = st.slider(
    "AI Signal Strength",
    min_value=1,
    max_value=100,
    value=55
)

confidence = st.slider(
    "Confidence Level",
    min_value=1,
    max_value=100,
    value=60
)

ai_probability = round((signal_strength * 0.6) + (confidence * 0.4), 2)
edge = round(ai_probability - market_probability, 2)

stake = round(starting_bankroll * (risk_per_trade / 100), 2)

st.subheader("AI Result")

col1, col2, col3, col4 = st.columns(4)

col1.metric("AI Probability", f"{ai_probability}%")
col2.metric("Market Probability", f"{market_probability}%")
col3.metric("Edge", f"{edge}%")
col4.metric("Paper Stake", f"${stake}")

if edge > 5:
    recommendation = "YES - strong paper trade"
elif edge > 2:
    recommendation = "WATCH - small edge"
else:
    recommendation = "NO TRADE"

st.success(f"Bot Recommendation: {recommendation}")

if st.button("Save Prediction"):
    st.session_state.history.append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "event": event_name,
        "market_probability": market_probability,
        "ai_probability": ai_probability,
        "edge": edge,
        "stake": stake,
        "recommendation": recommendation,
        "result": "pending"
    })
    st.success("Prediction saved.")

st.header("Prediction History")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No predictions saved yet.")
