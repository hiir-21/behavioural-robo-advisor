import streamlit as st

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
    padding: 15px 38px;
    font-size: 1rem;
    border-radius: 999px;
    font-weight: 700;
    box-shadow: 0 0 25px rgba(45, 248, 197, 0.25);
}

.stButton > button:hover {
    transform: translateY(-2px) scale(1.04);
    box-shadow: 0 0 35px rgba(45, 248, 197, 0.45);
}

.section {
    margin-top: 55px;
}

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

# ================= PAGE 1 : AGE & GENDER =================
elif st.session_state.page == 1:
    st.header("Basic Information")

    age = st.selectbox(
        "Select your age group",
        ["18–25", "26–35", "36–50", "50+"],
        index=None
    )

    gender = st.selectbox(
        "Select your gender",
        ["Female", "Male", "Prefer not to say"],
        index=None
    )

    if st.button("Next"):
        if age and gender:
            st.session_state.responses["demographics"] = {"Q1": age, "Q2": gender}
            st.session_state.page = 2
            st.rerun()
        else:
            st.warning("Please answer both questions.")

# ================= PAGE 2 : Q3–Q14 =================
elif st.session_state.page == 2:
    st.header("Investment Decision Scenarios")

    def ask(q, text, opts, section):
        st.session_state.responses[section][q] = st.radio(text, opts, index=None, key=q)

    ask("Q3","When new information contradicts your investment thesis, you usually:",
        ["A. Assume it is temporary noise","B. Wait for further confirmation",
         "C. Adjust expectations slightly","D. Re-examine the entire thesis",
         "E. Exit or reduce exposure"],"bias")

    ask("Q4","You bought a stock at ₹1,500; it now trades at ₹1,000. Which thought best reflects your reaction?",
        ["A. It should eventually return to ₹1,500","B. ₹1,500 remains a key reference for my decision",
         "C. Past prices matter less than future performance","D. The fall itself could indicate opportunity",
         "E. Price history alone should not guide decisions"],"bias")

    ask("Q5","When deciding whether to sell an investment, you rely most on:",
        ["A. The price you originally paid","B. The asset’s previous highest price",
         "C. Current valuation and fundamentals","D. Recent market sentiment and news",
         "E. Long-term expected returns"],"bias")

    ask("Q6","After a stock performs very well over the last few months, you believe:",
        ["A. The trend will continue","B. Momentum matters more than history",
         "C. Both trend and history matter","D. Long-term data is more reliable",
         "E. Short-term movements are irrelevant"],"bias")

    ask("Q7","Which presentation makes you more comfortable investing?",
        ["A. “90% success rate”","B. “Only 10% failure rate”",
         "C. Both equally","D. Absolute return numbers",
         "E. Long-term historical averages"],"bias")

    ask("Q8","After repeated news about market crashes, you:",
        ["A. Feel investing is riskier","B. Reduce exposure temporarily",
         "C. Re-check historical data","D. Proceed cautiously",
         "E. Stick strictly to long-term plans"],"bias")

    ask("Q9","Which situation feels most uncomfortable to you as an investor?",
        ["A. Selling an investment at a loss","B. Missing out on a potential gain",
         "C. Making a decision without sufficient information","D. Being wrong in front of others",
         "E. Realising a loss even when it improves future outcomes"],"bias")

    ask("Q10","After a series of profitable trades, you plan your next investment by:",
        ["A. Increasing position size significantly","B. Using the same strategy with minor tweaks",
         "C. Keeping position size unchanged","D. Diversifying to reduce reliance",
         "E. Reviewing assumptions behind past success"],"bias")

    ask("Q11","A stock is trending heavily on social media and business news. You:",
        ["A. Buy immediately","B. Invest a small amount","C. Track it closely first",
         "D. Research fundamentals independently","E. Avoid it due to hype"],"bias")

    ask("Q12","You have one stock with large gains and one with losses. You:",
        ["A. Sell the winner to lock profits","B. Hold the loser hoping for recovery",
         "C. Sell part of both","D. Rebalance based on targets",
         "E. Reassess both on fundamentals"],"bias")

    ask("Q13","You keep an old investment mainly because:",
        ["A. It feels familiar","B. Changing requires effort",
         "C. You haven’t reviewed alternatives","D. There’s no urgent reason",
         "E. You reassess periodically"],"bias")

    ask("Q14","When markets move sharply in a single day, you tend to:",
        ["A. Trade actively","B. Adjust positions quickly",
         "C. Pause and reassess","D. Stick to preset rules",
         "E. Avoid reacting"],"bias")

    if st.button("Next"):
        if all(st.session_state.responses["bias"].values()):
            st.session_state.page = 3
            st.rerun()
        else:
            st.warning("Please answer all questions.")

# ================= PAGE 3 : Q15–Q22 =================
elif st.session_state.page == 3:
    st.header("Personal Finance Preferences")

    def ask_risk(q, text, opts):
        st.session_state.responses["risk"][q] = st.radio(text, opts, index=None, key=q)

    ask_risk("Q15","Long-Term Wealth Goal (10–15 years)\nYou prefer to:",
        ["A. Protect capital even if growth is limited","B. Earn steady low-volatility returns",
         "C. Balance growth and safety","D. Accept volatility for higher growth",
         "E. Maximise growth despite fluctuations"])

    ask_risk("Q16","Retirement Horizon (20+ years away)\nYour approach would be:",
        ["A. Preserve savings","B. Focus on income assets",
         "C. Mix income and growth","D. Tilt toward growth early",
         "E. Aggressively grow capital"])

    ask_risk("Q17","Medium-Term Goal (5–7 years)\nYou would:",
        ["A. Keep funds fully safe","B. Use mostly low-risk instruments",
         "C. Combine safety with equity","D. Use growth assets initially",
         "E. Invest aggressively"])

    ask_risk("Q18","Reaction to a 10–15% Portfolio Decline\nYou would most likely:",
        ["A. Exit investments","B. Reduce exposure","C. Hold and wait",
         "D. Increase exposure","E. Rebalance strategically"])

    ask_risk("Q19","Risk–Return Preference\nWhich best describes you?",
        ["A. Lower risk, lower return","B. Moderate risk, moderate return",
         "C. Market-level risk and return","D. Higher risk for higher return",
         "E. Maximum return regardless of risk"])

    ask_risk("Q20","Volatility Attitude\nHow do you view market volatility?",
        ["A. Something to avoid","B. A reason to be cautious",
         "C. A normal part of investing","D. A potential opportunity",
         "E. A source of advantage"])

    ask_risk("Q21","Income vs Growth Orientation\nFor your long-term future, you value:",
        ["A. Stable income","B. Mostly income with some growth",
         "C. Equal income and growth","D. Mostly growth",
         "E. Growth first, income later"])

    ask_risk("Q22","Time vs Certainty Trade-off\nYou can reach your goal in:\n• 10 years with low risk, or\n• 6 years with high uncertainty\nYou would choose to:",
        ["A. Definitely choose safety","B. Lean toward safety",
         "C. Balance both","D. Prefer the faster route",
         "E. Strongly prefer speed despite risk"])

    if st.button("Submit Survey"):
        if all(st.session_state.responses["risk"].values()):
            st.session_state.page = 4
            st.rerun()
        else:
            st.warning("Please answer all questions.")

# ================= PAGE 4 : COMPLETION =================
elif st.session_state.page == 4:
    st.header("Assessment Completed")
    st.success("Your responses have been recorded successfully.")
