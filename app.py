import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Behavioural Robo-Advisor",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- GLOBAL CSS ----------------
st.markdown("""
<style>

/* Hide Streamlit sidebar */
section[data-testid="stSidebar"] {
    display: none;
}

/* Top Navigation Bar */
.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 50px;
    background: linear-gradient(90deg, #0f2027, #000000);
    border-bottom: 1px solid #1f2933;
}

.nav-left {
    font-size: 1.5rem;
    font-weight: 800;
    color: white;
}

.nav-center {
    display: flex;
    gap: 28px;
}

.nav-center button {
    background: none;
    border: none;
    color: #cbd5e1;
    font-size: 1rem;
    cursor: pointer;
}

.nav-center button:hover {
    color: white;
}

.nav-right button {
    background: #22c55e;
    color: black;
    border: none;
    padding: 10px 24px;
    border-radius: 999px;
    font-weight: 700;
    cursor: pointer;
}

.hero {
    text-align: center;
    padding: 90px 20px;
}

.hero h1 {
    font-size: 3.2rem;
    font-weight: 800;
}

.hero p {
    font-size: 1.1rem;
    color: #94a3b8;
    max-width: 720px;
    margin: auto;
}

.footer {
    text-align: center;
    color: #64748b;
    font-size: 0.85rem;
    margin-top: 40px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- NAV BAR ----------------
nav = st.container()
with nav:
    c1, c2, c3 = st.columns([2, 3, 1])

    with c1:
        st.markdown('<div class="nav-left">🧠 Behavioural Robo-Advisor</div>', unsafe_allow_html=True)

    with c2:
        col_h, col_m, col_b, col_a = st.columns(4)
        with col_h:
            if st.button("Home"):
                st.switch_page("app.py")
        with col_m:
            if st.button("Methodology"):
                st.switch_page("pages/methodology.py")
        with col_b:
            if st.button("Biases"):
                st.switch_page("pages/biases.py")
        with col_a:
            if st.button("About"):
                st.switch_page("pages/about.py")

    with c3:
        if st.button("Start Assessment"):
            st.switch_page("pages/methodology.py")

st.divider()

# ---------------- HOME CONTENT ----------------
st.markdown("""
<div class="hero">
    <h1>Decode Your Investment Behaviour</h1>
    <p>
    Identify behavioural biases and risk preferences influencing investment
    decisions using scenario-based behavioural finance assessment.
    This tool is strictly for academic analysis.
    </p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1,2,1])
with c2:
    if st.button("Begin Behavioural Assessment"):
        st.switch_page("pages/methodology.py")

st.markdown("""
<div class="footer">
    Session-based analysis • No data stored • Academic research prototype
</div>
""", unsafe_allow_html=True)

# ================= DEMOGRAPHICS =================
elif st.session_state.view == "survey_demographics":
    st.header("Basic Information")

    age = st.selectbox("Select your age group", ["18–25","26–35","36–50","50+"], index=None)
    gender = st.selectbox("Select your gender", ["Female","Male","Prefer not to say"], index=None)

    if st.button("Next"):
        if age and gender:
            st.session_state.responses["demographics"] = {"Q1": age, "Q2": gender}
            st.session_state.view = "survey_bias"
            st.rerun()
        else:
            st.warning("Please answer both questions.")

# ================= BIAS QUESTIONS =================
elif st.session_state.view == "survey_bias":
    st.header("Investment Decision Scenarios")

    def ask(q, text, opts):
        st.session_state.responses["bias"][q] = st.radio(text, opts, index=None, key=q)

    bias_questions = [
        ("Q3","When new information contradicts your investment thesis, you usually:",
         ["A. Assume it is temporary noise","B. Wait for further confirmation",
          "C. Adjust expectations slightly","D. Re-examine the entire thesis","E. Exit or reduce exposure"]),
        ("Q4","You bought a stock at ₹1,500; it now trades at ₹1,000:",
         ["A. It should return to ₹1,500","B. ₹1,500 is a key reference",
          "C. Past prices matter less","D. The fall may indicate opportunity","E. Price history should not guide decisions"]),
        ("Q5","When deciding whether to sell an investment, you rely most on:",
         ["A. Original price","B. Previous high","C. Fundamentals","D. Market sentiment","E. Long-term returns"]),
        ("Q6","After a stock performs very well recently:",
         ["A. Trend continues","B. Momentum matters","C. Both matter","D. Long-term data","E. Short-term moves irrelevant"]),
        ("Q7","Which presentation makes you more comfortable?",
         ["A. 90% success","B. 10% failure","C. Both equally","D. Absolute returns","E. Long-term averages"]),
        ("Q8","After repeated market crash news:",
         ["A. Investing feels riskier","B. Reduce exposure","C. Re-check data","D. Proceed cautiously","E. Stick to long-term plans"]),
        ("Q9","Most uncomfortable situation:",
         ["A. Booking a loss","B. Missing gains","C. Unclear decision","D. Being wrong publicly","E. Small loss for long-term gain"]),
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
            st.session_state.view = "survey_risk"
            st.rerun()
        else:
            st.warning("Please answer all questions.")

# ================= RISK QUESTIONS =================
elif st.session_state.view == "survey_risk":
    st.header("Personal Finance Preferences")

    def ask_risk(q, text, opts):
        st.session_state.responses["risk"][q] = st.radio(text, opts, index=None, key=q)

    risk_questions = [
        ("Q15","Long-term goal preference (10–15 years):",
         ["A. Protect capital","B. Low volatility","C. Balanced","D. High growth","E. Max growth"]),
        ("Q16","Retirement horizon approach:",
         ["A. Preserve savings","B. Income focus","C. Balanced","D. Growth early","E. Aggressive growth"]),
        ("Q17","Medium-term goal (5–7 years):",
         ["A. Fully safe","B. Mostly safe","C. Balanced","D. Growth-oriented","E. Aggressive"]),
        ("Q18","Reaction to 10–15% loss:",
         ["A. Exit","B. Reduce exposure","C. Hold","D. Increase exposure","E. Rebalance"]),
        ("Q19","Risk-return preference:",
         ["A. Low-low","B. Moderate","C. Market","D. High-high","E. Max return"]),
        ("Q20","Volatility view:",
         ["A. Avoid","B. Cautious","C. Normal","D. Opportunity","E. Advantage"]),
        ("Q21","Income vs growth:",
         ["A. Income","B. Mostly income","C. Balanced","D. Mostly growth","E. Growth first"]),
        ("Q22","Time vs certainty trade-off:",
         ["A. Safety","B. Lean safety","C. Balance","D. Faster route","E. Speed despite risk"])
    ]

    for q in risk_questions:
        ask_risk(*q)

    if st.button("Submit Survey"):
        if all(st.session_state.responses["risk"].values()):
            st.session_state.view = "analysis"
            st.rerun()
        else:
            st.warning("Please answer all questions.")

# ================= ANALYSIS =================
elif st.session_state.view == "analysis":
    st.header("Assessment Results")

    responses = {}
    for section in ["bias","risk"]:
        for q, ans in st.session_state.responses[section].items():
            responses[q] = ["A","B","C","D","E"].index(ans.split(".")[0]) + 1

    analysis = generate_full_survey_analysis(responses)

    st.session_state.results.append({
        "timestamp": datetime.now(),
        "analysis": analysis
    })

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

# ================= RESULTS =================
elif st.session_state.view == "results":
    st.header("Previous Assessments")

    if not st.session_state.results:
        st.info("No assessments completed yet.")
    else:
        for i, r in enumerate(st.session_state.results):
            with st.expander(f"Assessment {i+1} — {r['timestamp'].strftime('%d %b %Y %H:%M')}"):
                st.json(r["analysis"])

# ================= STATIC VIEWS =================
elif st.session_state.view == "methodology":
    show_methodology()

elif st.session_state.view == "biases":
    show_biases()

elif st.session_state.view == "about":
    show_about()
