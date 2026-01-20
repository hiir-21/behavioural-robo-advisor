import streamlit as st

def show_methodology():
    st.header("Methodology")

    st.subheader("Behavioral Finance Score (BFS)")
    st.write("""
    The Behavioral Finance Score (BFS) is calculated using responses to
    scenario-based questions (Q3–Q14). Each response is scored on a 1–5
    Likert scale, where higher values indicate stronger bias expression.
    """)

    st.subheader("Risk Appetite Score (RAS)")
    st.write("""
    Risk appetite is assessed using questions Q15–Q22. Responses are mapped
    to an ordinal scale and averaged to obtain a composite risk tolerance score.
    """)

