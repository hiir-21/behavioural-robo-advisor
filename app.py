import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Behavioural Bias Identification",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------- CSS STYLING ----------------
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #0f2027, #000000 60%);
    color: #ffffff;
}

/* NAVBAR */
.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 30px;
    border-bottom: 1px solid #1f2933;
    margin-bottom: 20px;
}

.nav-left {
    font-size: 1.3rem;
    font-weight: 700;
}

.nav-center button {
    background: none;
    border: none;
    color: #b0b8c1;
    font-size: 0.95rem;
    margin: 0 10px;
    cursor: pointer;
}

.nav-center button:hover {
    color: white;
}

.hero {
    text-align: center;
    padding: 90px 20px 40px;
}

.hero h1 {
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 18px;
}

.hero p {
    font-size: 1.1rem;
    color: #b0b8c1;
    max-width: 720px;
    margin: auto;
}

.stButton > button {
    background: linear-gradient(135deg, #2df8c5, #1cb5e0);
    color: black;
    border: none;
    padding: 14px 34px;
    font-size: 1rem;
    border-radius: 999px;
    font-weight: 600;
    margin-top: 30px;
}

.section {
    margin-top: 40px;
}

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
    st.session_state.page = 0

if "responses" not in st.session_state:
    st.session_state.responses = {
        "demographics": {},
        "bias": {},
        "risk": {}
    }

# ---------------- NAVBAR ----------------
nav = st.container()
with nav:
    c1, c2 = st.columns([2, 3])

    with c1:
        st.markdown("<div class='nav-left'>🧠 Behavioural Robo-Advisor</div>", unsafe_allow_html=True)

    with c2:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("Home"):
                st.session_state.page = 0
                st.rerun()
        with col2:
            if st.button("Methodology"):
                st.session_state.page = 99
                st.rerun()
        with col3:
            if st.button("Biases"):
                st.session_state.page = 98
                st.rerun()
        with col4:
            if st.button("About"):
                st.session_state.page = 97
                st.rerun()

# ---------------- PAGE 0 : HERO ----------------
if st.session_state.page == 0:
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

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Start Behavioural Assessment"):
            st.session_state.page = 1
            st.rerun()

    st.markdown("""
    <div class="trust">
        Session-based analysis • No data stored • Academic research prototype
    </div>
    """, unsafe_allow_html=True)

# ---------------- PAGE 1 : Q1–Q2 ----------------
elif st.session_state.page == 1:
    st.header("Basic Information")

    age = st.selectbox("Q1. Select your age group",
        ["18–25", "26–35", "36–50", "50+"], index=None)

    gender = st.selectbox("Q2. Select your gender",
        ["Female", "Male", "Prefer not to say"], index=None)

    if st.button("Next"):
        if age and gender:
            st.session_state.responses["demographics"] = {"Q1": age, "Q2": gender}
            st.session_state.page = 2
            st.rerun()
        else:
            st.warning("Please answer both questions.")

# ---------------- PAGE 2 : BIAS QUESTIONS ----------------
elif st.session_state.page == 2:
    st.header("Investment Decision Scenarios")

    def ask_bias(qno, question, options):
        st.session_state.responses["bias"][qno] = st.radio(
            question, options, index=None, key=qno
        )

    ask_bias("Q3","When new information contradicts your investment thesis:",
        ["A. Assume it is temporary noise","B. Wait for confirmation",
         "C. Adjust expectations","D. Re-examine thesis","E. Exit or reduce exposure"])

    ask_bias("Q4","Stock bought at ₹1,500 now ₹1,000:",
        ["A. It will return","B. ₹1,500 is reference","C. Past prices matter less",
         "D. Fall may be opportunity","E. Ignore price history"])

    ask_bias("Q5","When selling, you rely on:",
        ["A. Original price","B. Previous high","C. Fundamentals",
         "D. Market sentiment","E. Long-term returns"])

    ask_bias("Q6","After strong performance:",
        ["A. Trend continues","B. Momentum matters","C. Both matter",
         "D. Long-term data","E. Short-term irrelevant"])

    if st.button("Next"):
        if all(st.session_state.responses["bias"].values()):
            st.session_state.page = 3
            st.rerun()
        else:
            st.warning("Please answer all questions.")

# ---------------- PAGE 3 : RISK QUESTIONS ----------------
elif st.session_state.page == 3:
    st.header("Personal Finance Preferences")

    def ask_risk(qno, question, options):
        st.session_state.responses["risk"][qno] = st.radio(
            question, options, index=None, key=qno
        )

    ask_risk("Q15","Long-term goal preference:",
        ["A. Protect capital","B. Low volatility","C. Balanced",
         "D. High growth","E. Max growth"])

    ask_risk("Q16","Retirement approach:",
        ["A. Preserve","B. Income focus","C. Balanced",
         "D. Growth early","E. Aggressive"])

    if st.button("Submit Survey"):
        if all(st.session_state.responses["risk"].values()):
            st.session_state.page = 4
            st.rerun()
        else:
            st.warning("Please answer all questions.")

# ---------------- PAGE 4 : COMPLETION ----------------
elif st.session_state.page == 4:
    st.markdown("""
    <div class="card">
        <h3>Assessment Completed</h3>
        <p>
        Your responses have been recorded successfully.
        Behavioural bias scoring and risk appetite analysis will be performed next.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- STATIC PAGES ----------------
elif st.session_state.page == 99:
    st.header("Methodology")
    st.write("Explanation of BFS and Risk Appetite methodology.")

elif st.session_state.page == 98:
    st.header("Behavioural Biases")
    st.write("Confirmation bias, loss aversion, anchoring, herding, etc.")

elif st.session_state.page == 97:
    st.header("About Us")
    st.write("Purpose, project motivation, and mentor details.")
