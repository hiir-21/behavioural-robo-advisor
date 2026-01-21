import streamlit as st
from survey_logic import generate_full_survey_analysis

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Behavioral Robo-Advisor",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #0f2027, #000000 60%);
    color: #ffffff;
}

.app-title {
    text-align: center;
    font-size: 1.9rem;
    font-weight: 800;
    margin-top: 18px;
}

.navbar {
    display: flex;
    justify-content: center;
    gap: 14px;
    margin: 20px 0;
}

.stButton > button {
    background: linear-gradient(135deg, #2df8c5, #1cb5e0);
    color: black;
    border: none;
    padding: 10px 26px;
    font-size: 0.95rem;
    border-radius: 999px;
    font-weight: 600;
}

.hero {
    text-align: center;
    padding: 70px 20px 30px;
}
.hero h1 {
    font-size: 3rem;
    font-weight: 700;
}
.hero p {
    font-size: 1.1rem;
    color: #b0b8c1;
    max-width: 720px;
    margin: auto;
}

.section { margin-top: 40px; }

.card {
    background: #0d1117;
    padding: 26px;
    border-radius: 14px;
    margin-top: 20px;
    border: 1px solid #1f2933;
}

.trust {
    margin-top: 25px;
    font-size: 0.85rem;
    color: #8b949e;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "responses" not in st.session_state:
    st.session_state.responses = {
        "demographics": {},
        "bias": {},
        "risk": {}
    }

# ---------------- APP TITLE ----------------
st.markdown("<div class='app-title'>Behavioral Robo-Advisor</div>", unsafe_allow_html=True)

# ---------------- NAVBAR ----------------
st.markdown("<div class='navbar'>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("Home"):
        st.session_state.page = "Home"
        st.rerun()

with c2:
    if st.button("Methodology"):
        st.session_state.page = "Methodology"
        st.rerun()

with c3:
    if st.button("Biases"):
        st.session_state.page = "Biases"
        st.rerun()

with c4:
    if st.button("Results"):
        st.session_state.page = "Results"
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
st.divider()

# ======================================================
# HOME
# ======================================================
if st.session_state.page == "Home":

    st.markdown("""
    <div class="hero">
        <h1>Understand Your Investment Behaviour</h1>
        <p>
        Identify behavioural biases influencing investment decisions using
        scenario-based psychology and personal finance preferences.
        This tool provides behavioural diagnostics only and does not offer financial advice.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("Start Behavioural Assessment"):
            st.session_state.page = 1
            st.rerun()

    st.markdown("""
    <div class="trust">
        Session-based analysis • No data stored • Academic research prototype
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# METHODOLOGY
# ======================================================
elif st.session_state.page == "Methodology":
    st.header("Methodology")

    st.markdown("""
    **Behavioral Finance Scoring (BFS)**  
    Measures cognitive and emotional biases based on Prospect Theory
    (Kahneman & Tversky).

    **Risk Appetite Scoring (RAS)**  
    Uses ordinal responses (1–5) to classify investors into Low, Moderate,
    or High risk appetite categories.

    **Integrated View**  
    Behavioral biases are interpreted alongside risk tolerance to
    identify potential decision-making mismatches.
    """)

# ======================================================
# BIASES
# ======================================================
elif st.session_state.page == "Biases":
    st.header("Behavioral Biases Covered")

    st.markdown("""
    - Loss Aversion  
    - Anchoring Bias  
    - Herd Behaviour  
    - Overconfidence  
    - Recency Bias  
    - Framing Effect  
    - Disposition Effect  
    - Status Quo Bias  
    """)

# ======================================================
# RESULTS
# ======================================================
elif st.session_state.page == "Results":

    if not st.session_state.responses["risk"]:
        st.warning("Please complete the assessment first to view your results.")
    else:
        st.header("Assessment Results")

        responses_numeric = {}
        for section in ["bias", "risk"]:
            for q, ans in st.session_state.responses[section].items():
                responses_numeric[q] = ["A","B","C","D","E"].index(ans[0]) + 1

        analysis = generate_full_survey_analysis(responses_numeric)

        bfs = analysis["behavioral_bias_analysis"]["bfs_summary"]
        bias_profile = analysis["behavioral_bias_analysis"]["bias_profile"]
        risk = analysis["risk_appetite_analysis"]

        st.subheader("Behavioral Finance Score (BFS)")
        st.metric("BFS", f"{bfs['bfs_score']} / {bfs['max_score']}", bfs["category"])

        st.subheader("Detected Behavioral Biases")
        for bias, data in bias_profile.items():
            st.write(f"**{bias}** — {data['level']} (Score: {data['score']})")

        st.subheader("Risk Appetite Assessment")
        st.metric("Average Risk Score", risk["average_score"], risk["category"])
        st.write(risk["interpretation"])
