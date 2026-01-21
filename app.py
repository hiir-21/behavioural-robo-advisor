import streamlit as st
from survey_logic import generate_full_survey_analysis

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Behavioural Robo-Advisor",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "responses" not in st.session_state:
    st.session_state.responses = {
        "demographics": {},
        "bias": {},
        "risk": {}
    }

if "survey_completed" not in st.session_state:
    st.session_state.survey_completed = False

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# --------------------------------------------------
# STYLES
# --------------------------------------------------
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #0f2027, #000000 70%);
    color: white;
}

/* TITLE */
.app-title {
    text-align: center;
    font-size: 2rem;
    font-weight: 800;
    margin-top: 20px;
}

/* NAV BAR */
.navbar {
    display: flex;
    justify-content: center;
    gap: 18px;
    margin: 30px 0 25px;
}

.nav-btn > button {
    padding: 10px 24px;
    border-radius: 999px;
    border: none;
    font-weight: 600;
    background: #0d1117;
    color: #c9d1d9;
}

.nav-btn-active > button {
    background: linear-gradient(135deg, #2df8c5, #1cb5e0);
    color: black;
}

/* HERO */
.hero {
    text-align: center;
    margin-top: 70px;
}

.hero h1 {
    font-size: 3rem;
    font-weight: 800;
}

.hero p {
    max-width: 700px;
    margin: auto;
    color: #9ba3af;
    font-size: 1.1rem;
}

/* BUTTON */
.stButton > button {
    background: linear-gradient(135deg, #2df8c5, #1cb5e0);
    color: black;
    border-radius: 999px;
    padding: 14px 36px;
    border: none;
    font-weight: 600;
    margin-top: 35px;
}

/* CARD */
.card {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(14px);
    border-radius: 18px;
    padding: 28px;
    margin-top: 30px;
    border: 1px solid rgba(255,255,255,0.08);
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# APP TITLE
# --------------------------------------------------
st.markdown('<div class="app-title">🧠 Behavioural Robo-Advisor</div>', unsafe_allow_html=True)

# --------------------------------------------------
# NAV BAR
# --------------------------------------------------
tabs = ["Home", "Methodology", "Biases", "Results", "About"]
cols = st.columns(len(tabs))

for col, tab in zip(cols, tabs):
    with col:
        cls = "nav-btn-active" if st.session_state.page == tab else "nav-btn"
        st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
        if st.button(tab, key=f"nav-{tab}"):
            st.session_state.page = tab
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ==================================================
# HOME
# ==================================================
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

    if st.button("Start Behavioural Assessment"):
        st.session_state.page = "Survey-Demographics"
        st.rerun()

# ==================================================
# SURVEY – DEMOGRAPHICS
# ==================================================
elif st.session_state.page == "Survey-Demographics":

    st.header("Basic Information")

    age = st.selectbox("Q1. Select your age group",
                       ["18–25", "26–35", "36–50", "50+"], index=None)

    gender = st.selectbox("Q2. Select your gender",
                          ["Female", "Male", "Prefer not to say"], index=None)

    if st.button("Next"):
        if age and gender:
            st.session_state.responses["demographics"] = {"Q1": age, "Q2": gender}
            st.session_state.page = "Survey-Bias"
            st.rerun()
        else:
            st.warning("Please answer both questions.")

# ==================================================
# SURVEY – BIAS (Q3–Q14)
# ==================================================
elif st.session_state.page == "Survey-Bias":

    st.header("Investment Decision Scenarios")

    def ask_bias(q, text, opts):
        st.session_state.responses["bias"][q] = st.radio(text, opts, index=None, key=q)

    ask_bias("Q3","Q3. When new information contradicts your investment thesis, you usually:",
        ["A. Assume it is temporary noise","B. Wait for further confirmation",
         "C. Adjust expectations slightly","D. Re-examine the entire thesis","E. Exit or reduce exposure"])

    ask_bias("Q4","Q4. You bought a stock at ₹1,500; it now trades at ₹1,000. Which thought best reflects your reaction?",
        ["A. It should eventually return to ₹1,500","B. ₹1,500 remains a key reference for my decision",
         "C. Past prices matter less than future performance","D. The fall itself could indicate opportunity",
         "E. Price history alone should not guide decisions"])

    ask_bias("Q5","Q5. When deciding whether to sell an investment, you rely most on:",
        ["A. The price you originally paid","B. The asset’s previous highest price",
         "C. Current valuation and fundamentals","D. Recent market sentiment and news",
         "E. Long-term expected returns"])

    ask_bias("Q6","Q6. After a stock performs very well over the last few months, you believe:",
        ["A. The trend will continue","B. Momentum matters more than history",
         "C. Both trend and history matter","D. Long-term data is more reliable",
         "E. Short-term movements are irrelevant"])

    ask_bias("Q7","Q7. Which presentation makes you more comfortable investing?",
        ["A. “90% success rate”","B. “Only 10% failure rate”","C. Both equally",
         "D. Absolute return numbers","E. Long-term historical averages"])

    ask_bias("Q8","Q8. After repeated news about market crashes, you:",
        ["A. Feel investing is riskier","B. Reduce exposure temporarily",
         "C. Re-check historical data","D. Proceed cautiously","E. Stick strictly to long-term plans"])

    ask_bias("Q9","Q9. Which situation feels most uncomfortable to you as an investor?",
        ["A. Selling an investment at a loss","B. Missing out on a potential gain",
         "C. Making a decision without sufficient information","D. Being wrong in front of others",
         "E. Realising a loss even when it improves future outcomes"])

    ask_bias("Q10","Q10. After a series of profitable trades, you plan your next investment by:",
        ["A. Increasing position size significantly","B. Using the same strategy with minor tweaks",
         "C. Keeping position size unchanged","D. Diversifying to reduce reliance",
         "E. Reviewing assumptions behind past success"])

    ask_bias("Q11","Q11. A stock is trending heavily on social media and business news. You:",
        ["A. Buy immediately","B. Invest a small amount","C. Track it closely first",
         "D. Research fundamentals independently","E. Avoid it due to hype"])

    ask_bias("Q12","Q12. You have one stock with large gains and one with losses. You:",
        ["A. Sell the winner to lock profits","B. Hold the loser hoping for recovery",
         "C. Sell part of both","D. Rebalance based on targets","E. Reassess both on fundamentals"])

    ask_bias("Q13","Q13. You keep an old investment mainly because:",
        ["A. It feels familiar","B. Changing requires effort",
         "C. You haven’t reviewed alternatives","D. There’s no urgent reason",
         "E. You reassess periodically"])

    ask_bias("Q14","Q14. When markets move sharply in a single day, you tend to:",
        ["A. Trade actively","B. Adjust positions quickly",
         "C. Pause and reassess","D. Stick to preset rules","E. Avoid reacting"])

    if st.button("Next"):
        if all(st.session_state.responses["bias"].values()):
            st.session_state.page = "Survey-Risk"
            st.rerun()
        else:
            st.warning("Please answer all questions.")

# ==================================================
# SURVEY – RISK (Q15–Q22)
# ==================================================
elif st.session_state.page == "Survey-Risk":

    st.header("Personal Finance Preferences")

    def ask_risk(q, text, opts):
        st.session_state.responses["risk"][q] = st.radio(text, opts, index=None, key=q)

    ask_risk("Q15","Q15. Long-Term Wealth Goal (10–15 years)\nYou prefer to:",
        ["A. Protect capital even if growth is limited","B. Earn steady low-volatility returns",
         "C. Balance growth and safety","D. Accept volatility for higher growth",
         "E. Maximise growth despite fluctuations"])

    ask_risk("Q16","Q16. Retirement Horizon (20+ years away)\nYour approach would be:",
        ["A. Preserve savings","B. Focus on income assets","C. Mix income and growth",
         "D. Tilt toward growth early","E. Aggressively grow capital"])

    ask_risk("Q17","Q17. Medium-Term Goal (5–7 years)\nYou would:",
        ["A. Keep funds fully safe","B. Use mostly low-risk instruments",
         "C. Combine safety with equity","D. Use growth assets initially",
         "E. Invest aggressively"])

    ask_risk("Q18","Q18. Reaction to a 10–15% Portfolio Decline\nYou would most likely:",
        ["A. Exit investments","B. Reduce exposure","C. Hold and wait",
         "D. Increase exposure","E. Rebalance strategically"])

    ask_risk("Q19","Q19. Risk–Return Preference\nWhich best describes you?",
        ["A. Lower risk, lower return","B. Moderate risk, moderate return",
         "C. Market-level risk and return","D. Higher risk for higher return",
         "E. Maximum return regardless of risk"])

    ask_risk("Q20","Q20. Volatility Attitude\nHow do you view market volatility?",
        ["A. Something to avoid","B. A reason to be cautious",
         "C. A normal part of investing","D. A potential opportunity",
         "E. A source of advantage"])

    ask_risk("Q21","Q21. Income vs Growth Orientation\nFor your long-term future, you value:",
        ["A. Stable income","B. Mostly income with some growth",
         "C. Equal income and growth","D. Mostly growth",
         "E. Growth first, income later"])

    ask_risk("Q22","Q22. Time vs Certainty Trade-off\nYou can reach your goal in:\n• 10 years with low risk, or\n• 6 years with high uncertainty\nYou would choose to:",
        ["A. Definitely choose safety","B. Lean toward safety",
         "C. Balance both","D. Prefer the faster route",
         "E. Strongly prefer speed despite risk"])

    if st.button("Submit Survey"):
        responses_numeric = {
            q: ["A","B","C","D","E"].index(ans[0]) + 1
            for section in ["bias", "risk"]
            for q, ans in st.session_state.responses[section].items()
        }

        st.session_state.analysis_result = generate_full_survey_analysis(responses_numeric)
        st.session_state.survey_completed = True
        st.session_state.page = "Results"
        st.rerun()

# ==================================================
# RESULTS
# ==================================================
elif st.session_state.page == "Results":

    if not st.session_state.survey_completed:
        st.warning("Please complete the behavioural assessment to view results.")
    else:
        analysis = st.session_state.analysis_result

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

# ==================================================
# STATIC PAGES
# ==================================================
elif st.session_state.page == "Methodology":
    st.header("Methodology")
    st.info("Methodology content already defined earlier.")

elif st.session_state.page == "Biases":
    st.header("Behavioural Biases")
    st.info("This section will describe individual behavioural biases.")

elif st.session_state.page == "About":
    st.header("About")
    st.info("This project is an academic behavioural finance prototype.")
