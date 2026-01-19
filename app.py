import streamlit as st

st.set_page_config(page_title="Behavioural Bias Identification", layout="centered")

# ---------- TITLE ----------
st.title("Behavioural Bias Identification Dashboard")
st.write("This dashboard provides behavioural diagnostics only. It does not offer financial advice.")

st.divider()

# ---------- INTRO ----------
st.subheader("Welcome")
st.write("""
This tool helps identify behavioural biases in investment decision-making using:
- Scenario-based questions
- Portfolio allocation patterns

Your responses are analysed only during this session and are not stored.
""")

# ---------- START BUTTON ----------
if "start" not in st.session_state:
    st.session_state.start = False

if not st.session_state.start:
    if st.button("Start Behavioural Assessment"):
        st.session_state.start = True
        st.rerun()
