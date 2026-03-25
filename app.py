import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from survey_logic import generate_full_survey_analysis
from sector_analysis import sector_analysis
from ml_model import predict_sector

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

if "robo_result" not in st.session_state:
    st.session_state.robo_result = None

# --------------------------------------------------
# STYLES
# --------------------------------------------------
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #0f2027, #000000 70%);
    color: white;
}

.app-title {
    text-align: center;
    font-size: 2rem;
    font-weight: 800;
    margin-top: 20px;
}

.navbar {
    display: flex;
    justify-content: center;
    gap: 18px;
    margin: 30px 0 25px;
}

.nav-btn > button {
    padding: 12px 28px;
    border-radius: 999px;
    border: none;
    font-weight: 600;
    background: #0d1117;
    color: #c9d1d9;
    white-space: nowrap;
    min-width: 140px;
    text-align: center;
}

/* BUG FIX 2: closed the unclosed nav-btn-active block */
.nav-btn-active > button {
    background: linear-gradient(135deg, #2df8c5, #1cb5e0);
    color: black;
    white-space: nowrap;
    font-size: 16px;
}

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

.stButton > button {
    background: linear-gradient(135deg, #2df8c5, #1cb5e0);
    color: black;
    border-radius: 999px;
    padding: 14px 36px;
    border: none;
    font-weight: 600;
    margin-top: 35px;
}

.card {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(14px);
    border-radius: 18px;
    padding: 28px;
    margin-top: 30px;
    border: 1px solid rgba(255,255,255,0.08);
}

.results-title {
    color: #2df8c5;
    font-weight: 800;
    letter-spacing: 0.3px;
}

.summary-card {
    background: rgba(45,248,197,0.06);
    border: 1px solid rgba(45,248,197,0.2);
    border-radius: 18px;
    padding: 24px 28px;
    margin-bottom: 28px;
}

.progress-label {
    font-size: 0.85rem;
    color: #9ba3af;
    margin-bottom: 4px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# APP TITLE
# --------------------------------------------------
st.markdown('<div class="app-title">Behavioural Robo-Advisor</div>', unsafe_allow_html=True)

# --------------------------------------------------
# NAV BAR
# --------------------------------------------------
tabs = ["Home","Manual Assessment","Results","Method","Biases","About"]
cols = st.columns([1.2,2.4,1.2,1.2,1.2,1.2])

for col, tab in zip(cols, tabs):
    with col:
        cls = "nav-btn-active" if st.session_state.page == tab else "nav-btn"
        st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
        if st.button(tab, key=f"nav-{tab}", use_container_width=True):
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
        scenario-based psychology and demographic investor behaviour.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Start Behavioural Assessment"):
            st.session_state.page = "RoboAdvisor"
            st.rerun()


# ==================================================
# ROBO ADVISOR PAGE
# ==================================================
elif st.session_state.page == "RoboAdvisor":

    st.header("Robo-Advisor Analysis")

    # BUG FIX 1: age group values now match CSV format ("18-25 years")
    age = st.selectbox("Select Age Group",
        ["18-25 years", "26-40 years", "41-55 years", "56-70 years", "70+ years"]
    )

    # BUG FIX 4: removed "Prefer not to say"
    gender = st.selectbox("Select Gender",
        ["Female", "Male"]
    )

    if st.button("Run Analysis"):

        # ---------- STATISTICAL ANALYSIS ----------
        most_sector, least_sector, sector_avg = sector_analysis(age, gender)

        # ---------- ML PREDICTION ----------
        ml_sector = predict_sector(age, gender)

        # BUG FIX 3: removed duplicate hardcoded bias lines
        # bias_rules.py will be wired here once implemented
        from bias_rules import get_dominant_bias
        bias_result = get_dominant_bias(age, gender)
        bias = bias_result.get("dominant", "Insufficient data")

        st.session_state.robo_result = {
            "age": age,
            "gender": gender,
            "bias": bias,
            "sector": most_sector,
            "least_sector": least_sector,
            "ml_sector": ml_sector,
            "sector_avg": sector_avg
        }

        # FIX 13: auto-redirect to Results page
        st.session_state.page = "Results"
        st.rerun()


# ==================================================
# MANUAL ASSESSMENT ENTRY
# ==================================================
elif st.session_state.page == "Manual Assessment":

    st.header("Manual Behavioural Assessment")
    st.write(
        "Answer scenario-based questions to receive a personalized behavioural analysis."
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Start Manual Assessment", use_container_width=True):
            st.session_state.page = "Survey-Demographics"
            st.rerun()


# ==================================================
# SURVEY – DEMOGRAPHICS  (Step 1 of 3)
# ==================================================
elif st.session_state.page == "Survey-Demographics":

    # FIX 9: progress indicator
    st.markdown('<p class="progress-label">Step 1 of 3 — Basic Information</p>', unsafe_allow_html=True)
    st.progress(0.33)

    st.header("Basic Information")

    age = st.selectbox("Q1. Select your age group",
                       ["18–25", "26–35", "36–50", "50+"], index=None)

    gender = st.selectbox("Q2. Select your gender",
                          ["Female", "Male", "Prefer not to say"], index=None)

    if st.button("Next →"):
        if age and gender:
            st.session_state.responses["demographics"] = {"Q1": age, "Q2": gender}
            st.session_state.page = "Survey-Bias"
            st.rerun()
        else:
            st.warning("Please answer both questions.")


# ==================================================
# SURVEY – BIAS (Q3–Q14)   (Step 2 of 3)
# ==================================================
elif st.session_state.page == "Survey-Bias":

    # FIX 9: progress indicator
    st.markdown('<p class="progress-label">Step 2 of 3 — Investment Decision Scenarios</p>', unsafe_allow_html=True)
    st.progress(0.66)

    st.header("Investment Decision Scenarios")

    def ask_bias(q, text, opts):
        st.session_state.responses["bias"][q] = st.radio(text, opts, index=None, key=q)

    ask_bias("Q3", "When new information contradicts your investment thesis, you usually:",
        ["A. Assume it is temporary noise", "B. Wait for further confirmation",
         "C. Adjust expectations slightly", "D. Re-examine the entire thesis", "E. Exit or reduce exposure"])

    ask_bias("Q4", "You bought a stock at ₹1,500; it now trades at ₹1,000. Which thought best reflects your reaction?",
        ["A. It should eventually return to ₹1,500", "B. ₹1,500 remains a key reference for my decision",
         "C. Past prices matter less than future performance", "D. The fall itself could indicate opportunity",
         "E. Price history alone should not guide decisions"])

    ask_bias("Q5", "When deciding whether to sell an investment, you rely most on:",
        ["A. The price you originally paid", "B. The asset's previous highest price",
         "C. Current valuation and fundamentals", "D. Recent market sentiment and news",
         "E. Long-term expected returns"])

    ask_bias("Q6", "After a stock performs very well over the last few months, you believe:",
        ["A. The trend will continue", "B. Momentum matters more than history",
         "C. Both trend and history matter", "D. Long-term data is more reliable",
         "E. Short-term movements are irrelevant"])

    ask_bias("Q7", "Which presentation makes you more comfortable investing?",
        ["A. \"90% success rate\"", "B. \"Only 10% failure rate\"", "C. Both equally",
         "D. Absolute return numbers", "E. Long-term historical averages"])

    ask_bias("Q8", "After repeated news about market crashes, you:",
        ["A. Feel investing is riskier", "B. Reduce exposure temporarily",
         "C. Re-check historical data", "D. Proceed cautiously", "E. Stick strictly to long-term plans"])

    ask_bias("Q9", "Which situation feels most uncomfortable to you as an investor?",
        ["A. Selling an investment at a loss", "B. Missing out on a potential gain",
         "C. Making a decision without sufficient information", "D. Being wrong in front of others",
         "E. Realising a loss even when it improves future outcomes"])

    ask_bias("Q10", "After a series of profitable trades, you plan your next investment by:",
        ["A. Increasing position size significantly", "B. Using the same strategy with minor tweaks",
         "C. Keeping position size unchanged", "D. Diversifying to reduce reliance",
         "E. Reviewing assumptions behind past success"])

    ask_bias("Q11", "A stock is trending heavily on social media and business news. You:",
        ["A. Buy immediately", "B. Invest a small amount", "C. Track it closely first",
         "D. Research fundamentals independently", "E. Avoid it due to hype"])

    ask_bias("Q12", "You have one stock with large gains and one with losses. You:",
        ["A. Sell the winner to lock profits", "B. Hold the loser hoping for recovery",
         "C. Sell part of both", "D. Rebalance based on targets", "E. Reassess both on fundamentals"])

    ask_bias("Q13", "You keep an old investment mainly because:",
        ["A. It feels familiar", "B. Changing requires effort",
         "C. You haven't reviewed alternatives", "D. There's no urgent reason",
         "E. You reassess periodically"])

    ask_bias("Q14", "When markets move sharply in a single day, you tend to:",
        ["A. Trade actively", "B. Adjust positions quickly",
         "C. Pause and reassess", "D. Stick to preset rules", "E. Avoid reacting"])

    col_back, col_next = st.columns([1, 1])

    # FIX 10: Back button
    with col_back:
        if st.button("← Back"):
            st.session_state.page = "Survey-Demographics"
            st.rerun()

    with col_next:
        if st.button("Next →"):
            if all(st.session_state.responses["bias"].get(f"Q{i}") for i in range(3, 15)):
                st.session_state.page = "Survey-Risk"
                st.rerun()
            else:
                st.warning("Please answer all questions before continuing.")


# ==================================================
# SURVEY – RISK (Q15–Q22)   (Step 3 of 3)
# ==================================================
elif st.session_state.page == "Survey-Risk":

    # FIX 9: progress indicator
    st.markdown('<p class="progress-label">Step 3 of 3 — Personal Finance Preferences</p>', unsafe_allow_html=True)
    st.progress(1.0)

    st.header("Personal Finance Preferences")

    def ask_risk(q, text, opts):
        st.session_state.responses["risk"][q] = st.radio(text, opts, index=None, key=q)

    ask_risk("Q15", "Long-Term Wealth Goal (10–15 years)\nYou prefer to:",
        ["A. Protect capital even if growth is limited", "B. Earn steady low-volatility returns",
         "C. Balance growth and safety", "D. Accept volatility for higher growth",
         "E. Maximise growth despite fluctuations"])

    ask_risk("Q16", "Retirement Horizon (20+ years away)\nYour approach would be:",
        ["A. Preserve savings", "B. Focus on income assets", "C. Mix income and growth",
         "D. Tilt toward growth early", "E. Aggressively grow capital"])

    ask_risk("Q17", "Medium-Term Goal (5–7 years)\nYou would:",
        ["A. Keep funds fully safe", "B. Use mostly low-risk instruments",
         "C. Combine safety with equity", "D. Use growth assets initially",
         "E. Invest aggressively"])

    ask_risk("Q18", "Reaction to a 10–15% Portfolio Decline\nYou would most likely:",
        ["A. Exit investments", "B. Reduce exposure", "C. Hold and wait",
         "D. Increase exposure", "E. Rebalance strategically"])

    ask_risk("Q19", "Risk–Return Preference\nWhich best describes you?",
        ["A. Lower risk, lower return", "B. Moderate risk, moderate return",
         "C. Market-level risk and return", "D. Higher risk for higher return",
         "E. Maximum return regardless of risk"])

    ask_risk("Q20", "Volatility Attitude\nHow do you view market volatility?",
        ["A. Something to avoid", "B. A reason to be cautious",
         "C. A normal part of investing", "D. A potential opportunity",
         "E. A source of advantage"])

    ask_risk("Q21", "Income vs Growth Orientation\nFor your long-term future, you value:",
        ["A. Stable income", "B. Mostly income with some growth",
         "C. Equal income and growth", "D. Mostly growth",
         "E. Growth first, income later"])

    ask_risk("Q22", "Time vs Certainty Trade-off\nYou can reach your goal in:\n• 10 years with low risk, or\n• 6 years with high uncertainty\nYou would choose to:",
        ["A. Definitely choose safety", "B. Lean toward safety",
         "C. Balance both", "D. Prefer the faster route",
         "E. Strongly prefer speed despite risk"])

    col_back, col_submit = st.columns([1, 1])

    # FIX 10: Back button
    with col_back:
        if st.button("← Back"):
            st.session_state.page = "Survey-Bias"
            st.rerun()

    with col_submit:
        if st.button("Submit Survey"):
            responses_numeric = {}

            # BIAS QUESTIONS — reverse coded: A→5 (max bias), E→1 (min bias)
            for q, ans in st.session_state.responses["bias"].items():
                responses_numeric[q] = 6 - (["A", "B", "C", "D", "E"].index(ans[0]) + 1)

            # RISK QUESTIONS — normal coded: A→1 (conservative), E→5 (aggressive)
            for q, ans in st.session_state.responses["risk"].items():
                responses_numeric[q] = ["A", "B", "C", "D", "E"].index(ans[0]) + 1

            st.session_state.analysis_result = generate_full_survey_analysis(responses_numeric)
            st.session_state.survey_completed = True
            st.session_state.page = "Results"
            st.rerun()


# ==================================================
# RESULTS
# ==================================================
elif st.session_state.page == "Results":

    st.header("Results")

    has_robo = st.session_state.robo_result is not None
    has_survey = st.session_state.survey_completed

    # ==================================================
    # FIX 16: COMBINED SUMMARY CARD (shown when both paths completed)
    # ==================================================
    if has_robo and has_survey:
        robo = st.session_state.robo_result
        analysis = st.session_state.analysis_result
        bfs_sum = analysis["behavioral_bias_analysis"]["bfs_summary"]
        risk_sum = analysis["risk_appetite_analysis"]

        st.markdown("""
        <div class="summary-card">
            <h3 style="color:#2df8c5; margin-top:0;">Your Investment Behaviour Summary</h3>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Dominant Bias", robo["bias"])
        with c2:
            st.metric("BFS Score", f"{bfs_sum['bfs_score']} / 60", bfs_sum["category"])
        with c3:
            st.metric("Risk Profile", risk_sum["category"], f"{risk_sum['average_score']:.2f} / 5")

        st.divider()

    # ==================================================
    # ROBO ADVISOR RESULTS
    # ==================================================
    if has_robo:
        robo = st.session_state.robo_result

        st.markdown("<h2 class='results-title'>Robo-Advisor Insight</h2>", unsafe_allow_html=True)

        st.write(f"**Age Group:** {robo['age']}")
        st.write(f"**Gender:** {robo['gender']}")

        st.write(
            f"Based on behavioural patterns observed in the survey data, "
            f"investors in this demographic most commonly exhibit **{robo['bias']}**."
        )

        # BUG FIX 5: graceful handling when sector data is unavailable
        if robo["sector"] is None:
            st.warning(
                "Sector preference data is insufficient for this demographic group. "
                "Try selecting a different age group."
            )
        else:
            st.write(
                f"Secondary data analysis suggests that investors in this group "
                f"most frequently allocate to the **{robo['sector']} sector**, "
                f"while the **least preferred sector** is **{robo['least_sector']}**."
            )
            st.write(f"**ML Prediction:** Predicted preferred sector is **{robo['ml_sector']}**")

            st.subheader("Average Sector Allocation for Your Demographic")

            # FIX 15: Plotly themed bar chart replacing st.bar_chart
            sector_data = robo["sector_avg"]
            fig_sector = go.Figure(go.Bar(
                x=list(sector_data.index),
                y=list(sector_data.values),
                marker=dict(
                    color=list(sector_data.values),
                    colorscale=[[0, "#1cb5e0"], [1, "#2df8c5"]],
                    showscale=False
                ),
                text=[f"{v:.1f}%" for v in sector_data.values],
                textposition="outside",
                textfont=dict(color="#c9d1d9", size=11)
            ))
            fig_sector.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#c9d1d9"),
                xaxis=dict(
                    tickangle=-35,
                    gridcolor="rgba(255,255,255,0.05)",
                    tickfont=dict(size=11)
                ),
                yaxis=dict(
                    gridcolor="rgba(255,255,255,0.05)",
                    title="Avg Allocation (%)"
                ),
                margin=dict(t=20, b=80, l=40, r=20),
                height=360
            )
            st.plotly_chart(fig_sector, use_container_width=True)

        st.divider()

    # ==================================================
    # MANUAL SURVEY RESULTS
    # ==================================================
    if not has_survey:
        st.warning("Manual behavioural assessment has not been completed yet.")
    else:
        analysis = st.session_state.analysis_result
        bfs = analysis["behavioral_bias_analysis"]["bfs_summary"]
        bias_profile = analysis["behavioral_bias_analysis"]["bias_profile"]
        risk = analysis["risk_appetite_analysis"]

        # ---------------- BFS SCORE ----------------
        st.markdown("<h2 class='results-title'>Behavioral Finance Score (BFS)</h2>", unsafe_allow_html=True)

        st.metric(
            "BFS",
            f"{bfs['bfs_score']} / {bfs['max_score']}",
            bfs["category"]
        )

        st.caption(
            "Your BFS is calculated out of **60**, based on **12 behavioural biases**. "
            "Higher scores indicate greater susceptibility to behavioural biases."
        )

        # ---------------- FIX 14: BIAS PROFILE CHART ----------------
        st.subheader("Detected Behavioural Biases")

        bias_names = list(bias_profile.keys())
        bias_scores = [bias_profile[b]["score"] for b in bias_names]
        bias_levels = [bias_profile[b]["level"] for b in bias_names]

        color_map = {"High": "#e05c5c", "Moderate": "#e0a85c", "Low": "#5ce0b8"}
        bar_colors = [color_map.get(lvl, "#7f77dd") for lvl in bias_levels]

        fig_bias = go.Figure(go.Bar(
            x=bias_scores,
            y=bias_names,
            orientation="h",
            marker=dict(color=bar_colors),
            text=[f"{s:.2f} — {l}" for s, l in zip(bias_scores, bias_levels)],
            textposition="outside",
            textfont=dict(color="#c9d1d9", size=11)
        ))
        fig_bias.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#c9d1d9"),
            xaxis=dict(
                range=[0, 1.25],
                gridcolor="rgba(255,255,255,0.05)",
                title="Intensity (0 – 1)"
            ),
            yaxis=dict(
                gridcolor="rgba(255,255,255,0.05)",
                tickfont=dict(size=11)
            ),
            margin=dict(t=10, b=30, l=180, r=100),
            height=420,
            shapes=[
                dict(type="line", x0=0.33, x1=0.33, y0=-0.5, y1=len(bias_names) - 0.5,
                     line=dict(color="rgba(255,255,255,0.15)", width=1, dash="dot")),
                dict(type="line", x0=0.66, x1=0.66, y0=-0.5, y1=len(bias_names) - 0.5,
                     line=dict(color="rgba(255,255,255,0.15)", width=1, dash="dot")),
            ]
        )
        st.plotly_chart(fig_bias, use_container_width=True)

        st.caption("Dashed lines mark Low / Moderate / High thresholds at 0.33 and 0.66.")

        # ---------------- RISK APPETITE ----------------
        avg_risk = risk["average_score"]

        if avg_risk < 2:
            risk_line = (
                f"An average score of **{avg_risk:.2f}/5** indicates a "
                "**conservative risk profile**, with strong preference for stability and lower volatility."
            )
        elif avg_risk < 3.5:
            risk_line = (
                f"An average score of **{avg_risk:.2f}/5** indicates a "
                "**moderate risk tolerance**, balancing growth opportunities with risk control."
            )
        else:
            risk_line = (
                f"An average score of **{avg_risk:.2f}/5** indicates a "
                "**higher risk tolerance**, with comfort in volatility for potential long-term returns."
            )

        st.markdown("<h2 class='results-title'>Risk Appetite Assessment</h2>", unsafe_allow_html=True)

        st.metric(
            "Average Risk Score",
            f"{avg_risk:.2f} / 5",
            risk["category"]
        )

        st.markdown(
            "**Score scale:** 1 = Very conservative · 3 = Balanced · 5 = Highly aggressive"
        )

        st.markdown(risk_line)

        st.markdown(
            "_This assessment reflects behavioural tendencies inferred from your answers, "
            "not financial advice or performance predictions._"
        )


# ==================================================
# METHOD PAGE
# ==================================================
elif st.session_state.page == "Method":

    st.header("Method")

    st.write(
        "This page explains the theoretical foundations and scoring mechanisms "
        "used to identify behavioural biases and risk appetite."
    )

    st.divider()

    with st.expander("Behavioural Finance Scoring (BFS)"):
        st.markdown("""
        <h4 style="font-size:1.4rem; font-weight:700; margin-bottom:10px;">
        How Your Behavioural Finance Score Is Calculated
        </h4>

        <p style="color:#cfd6dd; font-size:0.95rem; line-height:1.6;">
        Your <strong>Behavioural Finance Score (BFS)</strong> reflects how strongly
        behavioural biases influence your investment decisions. It is derived from
        how you responded to realistic, scenario-based investment questions.
        </p>

        <p style="color:#cfd6dd; font-size:0.95rem; line-height:1.6;">
        Instead of asking you to label yourself, the assessment identifies
        <strong>patterns in your decision-making</strong> that commonly affect
        real-world investors.
        </p>

        <hr style="border:0.5px solid #2a2f36; margin:20px 0;">

        <h5 style="font-size:1.1rem; font-weight:600; margin-bottom:8px;">How the Score Works</h5>

        <ul style="color:#cfd6dd; font-size:0.92rem; line-height:1.6;">
            <li>BFS is calculated <strong>out of 60</strong>, based on <strong>12 behavioural biases</strong></li>
            <li>Each bias contributes equally to the final score</li>
            <li>Higher scores indicate greater susceptibility to behavioural biases</li>
            <li>Lower scores suggest more disciplined and emotionally neutral decisions</li>
        </ul>

        <hr style="border:0.5px solid #2a2f36; margin:20px 0;">

        <h5 style="font-size:1.1rem; font-weight:600; margin-bottom:8px;">Understanding Bias Intensity</h5>

        <ul style="color:#cfd6dd; font-size:0.92rem; line-height:1.6;">
            <li><strong>0.00 – 0.33</strong> → Low influence</li>
            <li><strong>0.34 – 0.66</strong> → Moderate influence</li>
            <li><strong>0.67 – 1.00</strong> → High influence</li>
        </ul>

        <p style="color:#9ba3af; font-size:0.9rem; margin-top:10px;">
        This score is diagnostic — it highlights tendencies, not mistakes.
        </p>
        """, unsafe_allow_html=True)

    with st.expander("Risk Appetite Scoring"):
        st.markdown("""
        <h4 style="font-size:1.3rem; font-weight:700; margin-bottom:10px;">
        How Your Risk Appetite Score Is Determined
        </h4>

        <p style="color:#cfd6dd; font-size:0.95rem; line-height:1.6;">
        Your <strong>Risk Appetite Score</strong> represents how comfortable you are with
        uncertainty, volatility, and potential losses when making investment decisions.
        </p>

        <hr style="border:0.5px solid #2a2f36; margin:20px 0;">

        <h5 style="font-size:1.1rem; font-weight:600; margin-bottom:8px;">How the Score Works</h5>

        <ul style="color:#cfd6dd; font-size:0.92rem; line-height:1.6;">
            <li>Each response is scored on a <strong>1–5 scale</strong></li>
            <li>Lower values indicate conservative risk preferences</li>
            <li>Higher values indicate greater comfort with risk and volatility</li>
            <li>The final score reflects an <strong>average risk tendency</strong></li>
        </ul>

        <hr style="border:0.5px solid #2a2f36; margin:20px 0;">

        <h5 style="font-size:1.1rem; font-weight:600; margin-bottom:8px;">Interpreting Risk Appetite Scores</h5>

        <ul style="color:#cfd6dd; font-size:0.92rem; line-height:1.6;">
            <li><strong>1.0 – 2.0</strong> → Conservative risk appetite</li>
            <li><strong>2.1 – 3.5</strong> → Moderate / balanced risk appetite</li>
            <li><strong>3.6 – 5.0</strong> → Aggressive risk appetite</li>
        </ul>

        <p style="color:#9ba3af; font-size:0.9rem; margin-top:10px;">
        Results are based on patterns across multiple questions, ensuring that
        no single response disproportionately influences the outcome.
        </p>
        """, unsafe_allow_html=True)

    with st.expander("Behavioural Bias and Portfolio Integration"):
        st.markdown("""
        This integration enables context-aware insights rather than generic
        recommendations, supporting disciplined decision-making.
        """)


# ==================================================
# BIASES PAGE
# ==================================================
elif st.session_state.page == "Biases":

    st.header("Biases")

    st.markdown("""
    <h3 style="font-size:1.6rem; font-weight:800; margin-bottom:18px;">
    Behavioural Biases Explained
    </h3>

    <p style="color:#cfd6dd; font-size:0.95rem; line-height:1.6;">
    The assessment identifies psychological patterns that commonly influence
    real-world investment behaviour. These biases affect how investors
    process information, perceive risk, and act under uncertainty.
    </p>
    """, unsafe_allow_html=True)

    def bias_expander(title, desc, example):
        with st.expander(title):
            st.markdown(f"""
            <p style="color:#cfd6dd; font-size:0.92rem; line-height:1.6;">{desc}</p>
            <p style="color:#9ba3af; font-size:0.9rem;"><em>Example: {example}</em></p>
            """, unsafe_allow_html=True)

    bias_expander(
        "Confirmation Bias",
        "Confirmation bias occurs when investors actively look for information that supports their existing beliefs while downplaying or ignoring evidence that challenges them. Over time, this selective attention can strengthen confidence in an incorrect investment view and delay corrective decisions.",
        "You believe a company is a great long-term investment, so you focus only on positive news and dismiss poor earnings as \"temporary,\" missing early signs of trouble."
    )
    bias_expander(
        "Anchoring",
        "Anchoring bias arises when investors rely too heavily on an initial reference point, such as a purchase price or past valuation. Future decisions are then made relative to this anchor, even when new information makes it irrelevant.",
        "You bought a stock at ₹1,500 and refuse to sell until it returns to that price, even though the company's outlook has worsened."
    )
    bias_expander(
        "Recency Bias",
        "Recency bias occurs when investors place excessive importance on recent events while underestimating long-term trends. This can lead to overreaction to short-term performance, causing investors to chase recent winners or panic during temporary downturns.",
        "A stock has performed very well in recent months, so you invest heavily, assuming the trend will continue without checking long-term fundamentals."
    )
    bias_expander(
        "Framing Effect",
        "The framing effect happens when investment decisions are influenced by how information is presented rather than by the actual facts. Different wording can trigger different emotional reactions, even when the underlying information remains the same.",
        "You feel more confident about an investment described as having a \"90% success rate\" than one described as a \"10% failure rate,\" even though both describe the same outcome."
    )
    bias_expander(
        "Risk Sensitivity",
        "Risk sensitivity reflects how strongly an investor emotionally reacts to perceived risk or uncertainty. Highly risk-sensitive individuals may allow fear or anxiety to dominate decision-making, leading to overly cautious behaviour.",
        "After repeatedly hearing news about market crashes, you avoid equity investments altogether, even though long-term data shows that downturns are a normal part of markets."
    )
    bias_expander(
        "Loss Aversion",
        "Loss aversion refers to the tendency to experience losses more intensely than equivalent gains. Investors often focus on avoiding losses rather than maximising overall returns, leading to irrational decisions such as holding onto losing investments for too long.",
        "You keep holding a falling stock to avoid \"locking in\" a loss, even when switching to a better investment could improve your portfolio."
    )
    bias_expander(
        "Overconfidence",
        "Overconfidence bias occurs when investors overestimate their knowledge, skills, or ability to predict market movements. This can lead to excessive trading, insufficient diversification, and underestimation of risk.",
        "After a few successful trades, you increase your position sizes, assuming your judgement is always correct, without considering the role of luck."
    )
    bias_expander(
        "Herding",
        "Herding bias occurs when investors follow the actions of others instead of making independent decisions. Social influence and fear of missing out often drive this bias, leading to crowded trades and increased risk exposure.",
        "You buy a stock simply because it is trending on social media, without understanding the underlying business."
    )
    bias_expander(
        "Disposition Effect",
        "The disposition effect describes the tendency to sell investments that have gained value too quickly while holding onto losing investments for too long. This is driven by the desire to realise gains and avoid regret associated with losses.",
        "You sell a stock as soon as it shows a small profit but continue holding a losing stock, hoping it will recover."
    )
    bias_expander(
        "Status Quo Bias",
        "Status quo bias is the preference to maintain existing choices rather than making changes, even when better alternatives exist. Familiarity and inertia often prevent investors from reviewing or adjusting their portfolios.",
        "You keep the same investments for years without reviewing them, simply because changing them feels uncomfortable."
    )
    bias_expander(
        "Emotional / Overtrading Bias",
        "Emotional or overtrading bias occurs when investment decisions are driven by emotions such as fear, excitement, or stress rather than rational analysis. This can result in frequent trading, poor timing, and higher transaction costs.",
        "During a highly volatile market day, you rapidly buy and sell assets based on fear or excitement instead of sticking to a long-term plan."
    )

    st.divider()


# ==================================================
# ABOUT PAGE
# ==================================================
elif st.session_state.page == "About":

    st.header("About This Project")

    st.markdown("""
    <div class="card">
    <h3>Overview</h3>
    <p>
    The Behavioural Robo-Advisor is an academic project that analyzes how
    psychological biases and demographic patterns influence investment decisions.
    </p>
    <p>
    Unlike traditional financial tools that focus only on returns and risk,
    this system integrates behavioural finance principles to provide deeper
    insights into investor decision-making.
    </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h3>Objective</h3>
    <ul>
        <li>Identify behavioural biases in investment decisions</li>
        <li>Measure individual risk appetite</li>
        <li>Analyze patterns across age and gender groups</li>
        <li>Provide data-driven and self-assessment insights</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h3>How It Works</h3>
    <p>The platform provides two modes of analysis:</p>
    <ul>
        <li><strong>Robo-Advisor Analysis:</strong> Uses demographic data to infer
        behavioural patterns and sector preferences.</li>
        <li><strong>Manual Assessment:</strong> A scenario-based survey that evaluates
        behavioural biases and risk appetite using structured scoring logic.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h3>Data Used</h3>
    <ul>
        <li><strong>Primary Data:</strong> Survey responses collected from participants</li>
        <li><strong>Secondary Data:</strong> Sector-wise investment allocation by demographic groups</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h3>Key Features</h3>
    <ul>
        <li>Behavioural Finance Score (BFS)</li>
        <li>Bias detection and intensity analysis</li>
        <li>Risk appetite classification</li>
        <li>Demographic-based investment insights</li>
        <li>Combined results dashboard</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h3>Disclaimer</h3>
    <p>
    This tool is developed for academic and research purposes only.
    It does not provide financial advice or investment recommendations.
    </p>
    </div>
    """, unsafe_allow_html=True)
