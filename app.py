import streamlit as st
from survey_logic import generate_full_survey_analysis

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Behavioural Bias Identification",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------- ADVANCED STYLING ----------------
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top left, #0f2027, #000000 65%);
    color: #ffffff;
}
.gradient-text {
    background: linear-gradient(90deg, #2df8c5, #1cb5e0, #9b5cff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero {
    text-align: center;
    padding: 90px 20px 50px;
}
.hero h1 {
    font-size: 3.2rem;
    font-weight: 800;
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
    padding: 15px 38px;
    font-size: 1rem;
    border-radius: 999px;
    font-weight: 700;
}
.section { margin-top: 55px; }
.trust {
    margin-top: 30px;
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

# ================= PAGE 0 : HERO =================
if st.session_state.page == 0:
    st.markdown("""
    <div class="hero">
        <h1 class="gradient-text">Decode Your Investment Behaviour</h1>
        <p>
        Identify behavioural biases influencing investment decisions using
        scenario-based psychology and personal finance preferences.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Start Behavioural Assessment"):
        st.session_state.page = 1
        st.rerun()

    st.markdown("""
    <div class="trust">
        Session-based analysis • No data stored • Academic research prototype
    </div>
    """, unsafe_allow_html=True)

# ================= PAGE 1 : AGE & GENDER =================
elif st.session_state.page == 1:
    st.header("Basic Information")

    age = st.selectbox("Select your age group", ["18–25","26–35","36–50","50+"], index=None)
    gender = st.selectbox("Select your gender", ["Female","Male","Prefer not to say"], index=None)

    if st.button("Next"):
        if age and gender:
            st.session_state.responses["demographics"] = {"Q1": age, "Q2": gender}
            st.session_state.page = 2
            st.rerun()
        else:
            st.warning("Please answer both questions.")

# ================= PAGE 2 : Q3–Q14 (BIAS) =================
elif st.session_state.page == 2:
    st.header("Investment Decision Scenarios")

    def ask(q, text, opts):
        st.session_state.responses["bias"][q] = st.radio(text, opts, index=None, key=q)

    bias_questions = [
        ("Q3","When new information contradicts your investment thesis, you usually:",
         ["A. Assume it is temporary noise","B. Wait for further confirmation","C. Adjust expectations slightly",
          "D. Re-examine the entire thesis","E. Exit or reduce exposure"]),
        ("Q4","You bought a stock at ₹1,500; it now trades at ₹1,000. You think:",
         ["A. It should eventually return to ₹1,500","B. ₹1,500 remains a key reference",
          "C. Past prices matter less","D. The fall could indicate opportunity","E. Price history alone should not guide decisions"]),
        ("Q5","When deciding whether to sell an investment, you rely most on:",
         ["A. Original price","B. Previous high","C. Current fundamentals","D. Market sentiment","E. Long-term returns"]),
        ("Q6","After a stock performs very well recently:",
         ["A. Trend will continue","B. Momentum matters","C. Both trend and history","D. Long-term data","E. Short-term moves irrelevant"]),
        ("Q7","Which presentation makes you more comfortable?",
         ["A. 90% success rate","B. 10% failure rate","C. Both equally","D. Absolute numbers","E. Long-term averages"]),
        ("Q8","After repeated market crash news:",
         ["A. Investing feels riskier","B. Reduce exposure","C. Re-check data","D. Proceed cautiously","E. Stick to long-term plans"]),
        ("Q9","Most uncomfortable situation:",
         ["A. Booking a loss","B. Missing a gain","C. Unclear decision","D. Being wrong publicly","E. Small loss for long-term benefit"]),
        ("Q10","After profitable trades:",
         ["A. Increase size","B. Same strategy","C. Keep size","D. Diversify","E. Review assumptions"]),
        ("Q11","Stock trending on social media:",
         ["A. Buy immediately","B. Invest small","C. Track first","D. Research fundamentals","E. Avoid hype"]),
        ("Q12","One stock up, one down:",
         ["A. Sell winner","B. Hold loser","C. Sell part both","D. Rebalance","E. Reassess fundamentals"]),
        ("Q13","You keep old investments because:",
         ["A. Familiar","B. Effort to change","C. Haven’t reviewed","D. No urgency","E. Periodic review"]),
        ("Q14","When markets move sharply:",
         ["A. Trade actively","B. Adjust quickly","C. Pause","D. Stick to rules","E. Avoid reacting"])
    ]

    for q in bias_questions:
        ask(*q)

    if st.button("Next"):
        if all(st.session_state.responses["bias"].values()):
            st.session_state.page = 3
            st.rerun()
        else:
            st.warning("Please answer all questions.")

# ================= PAGE 3 : Q15–Q22 (RISK) =================
elif st.session_state.page == 3:
    st.header("Personal Finance Preferences")

    def ask_risk(q, text, opts):
        st.session_state.responses["risk"][q] = st.radio(text, opts, index=None, key=q)

    risk_questions = [
    ("Q15", "Long-term goal preference (10–15 years). You prefer to:",
     [
         "A. Protect capital even if growth is limited",
         "B. Earn steady low-volatility returns",
         "C. Balance growth and safety",
         "D. Accept volatility for higher growth",
         "E. Maximise growth despite fluctuations"
     ]),

    ("Q16", "Retirement horizon (20+ years away). Your approach would be:",
     [
         "A. Preserve savings",
         "B. Focus on income assets",
         "C. Mix income and growth",
         "D. Tilt toward growth early",
         "E. Aggressively grow capital"
     ]),

    ("Q17", "Medium-term goal (5–7 years). You would:",
     [
         "A. Keep funds fully safe",
         "B. Use mostly low-risk instruments",
         "C. Combine safety with equity",
         "D. Use growth assets initially",
         "E. Invest aggressively"
     ]),

    ("Q18", "Reaction to a 10–15% portfolio decline:",
     [
         "A. Exit investments",
         "B. Reduce exposure",
         "C. Hold and wait",
         "D. Increase exposure",
         "E. Rebalance strategically"
     ]),

    ("Q19", "Risk–return preference. Which best describes you?",
     [
         "A. Lower risk, lower return",
         "B. Moderate risk, moderate return",
         "C. Market-level risk and return",
         "D. Higher risk for higher return",
         "E. Maximum return regardless of risk"
     ]),

    ("Q20", "How do you view market volatility?",
     [
         "A. Something to avoid",
         "B. A reason to be cautious",
         "C. A normal part of investing",
         "D. A potential opportunity",
         "E. A source of advantage"
     ]),

    ("Q21", "For your long-term future, you value:",
     [
         "A. Stable income",
         "B. Mostly income with some growth",
         "C. Equal income and growth",
         "D. Mostly growth",
         "E. Growth first, income later"
     ]),

    ("Q22", "Time vs certainty trade-off. You can reach your goal in:\n"
             "• 10 years with low risk, or\n"
             "• 6 years with high uncertainty.\nYou would choose to:",
     [
         "A. Definitely choose safety",
         "B. Lean toward safety",
         "C. Balance both",
         "D. Prefer the faster route",
         "E. Strongly prefer speed despite risk"
     ])
]


    for q in risk_questions:
        ask_risk(*q)

    if st.button("Submit Survey"):
        if all(st.session_state.responses["risk"].values()):
            st.session_state.page = 4
            st.rerun()
        else:
            st.warning("Please answer all questions.")

# ================= PAGE 4 : ANALYSIS =================
elif st.session_state.page == 4:
    st.header("Assessment Results")

    # Convert responses to numeric scale
    responses = {}
    for section in ["bias","risk"]:
        for q, ans in st.session_state.responses[section].items():
            responses[q] = ["A","B","C","D","E"].index(ans.split(".")[0]) + 1

    analysis = generate_full_survey_analysis(responses)

    bfs = analysis["behavioral_bias_analysis"]["bfs_summary"]
    bias_profile = analysis["behavioral_bias_analysis"]["bias_profile"]
    risk = analysis["risk_appetite_analysis"]

    st.subheader("Behavioral Finance Score")
    st.metric("BFS", f"{bfs['bfs_score']} / {bfs['max_score']}", bfs["category"])

    st.subheader("Behavioral Bias Breakdown")
    for b, d in bias_profile.items():
        st.write(f"**{b}** — {d['level']} (Score: {d['score']})")

    st.subheader("Risk Appetite Assessment")
    st.metric("Average Risk Score", risk["average_score"], risk["category"])
    st.write(risk["interpretation"])
