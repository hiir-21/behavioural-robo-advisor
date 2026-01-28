
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

/* RESULTS SECTION TITLES */
.results-title {
    color: #2df8c5;
    font-weight: 800;
    letter-spacing: 0.3px;
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
tabs = ["Home", "Method", "Biases", "Results", "About"]
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

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.button("Start Behavioural Assessment"):
            st.session_state.page = "Survey-Demographics"  # <-- FIXED
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

    ask_bias("Q3","When new information contradicts your investment thesis, you usually:",
        ["A. Assume it is temporary noise","B. Wait for further confirmation",
         "C. Adjust expectations slightly","D. Re-examine the entire thesis","E. Exit or reduce exposure"])

    ask_bias("Q4","You bought a stock at ₹1,500; it now trades at ₹1,000. Which thought best reflects your reaction?",
        ["A. It should eventually return to ₹1,500","B. ₹1,500 remains a key reference for my decision",
         "C. Past prices matter less than future performance","D. The fall itself could indicate opportunity",
         "E. Price history alone should not guide decisions"])

    ask_bias("Q5","When deciding whether to sell an investment, you rely most on:",
        ["A. The price you originally paid","B. The asset’s previous highest price",
         "C. Current valuation and fundamentals","D. Recent market sentiment and news",
         "E. Long-term expected returns"])

    ask_bias("Q6","After a stock performs very well over the last few months, you believe:",
        ["A. The trend will continue","B. Momentum matters more than history",
         "C. Both trend and history matter","D. Long-term data is more reliable",
         "E. Short-term movements are irrelevant"])

    ask_bias("Q7","Which presentation makes you more comfortable investing?",
        ["A. “90% success rate”","B. “Only 10% failure rate”","C. Both equally",
         "D. Absolute return numbers","E. Long-term historical averages"])

    ask_bias("Q8","After repeated news about market crashes, you:",
        ["A. Feel investing is riskier","B. Reduce exposure temporarily",
         "C. Re-check historical data","D. Proceed cautiously","E. Stick strictly to long-term plans"])

    ask_bias("Q9","Which situation feels most uncomfortable to you as an investor?",
        ["A. Selling an investment at a loss","B. Missing out on a potential gain",
         "C. Making a decision without sufficient information","D. Being wrong in front of others",
         "E. Realising a loss even when it improves future outcomes"])

    ask_bias("Q10","After a series of profitable trades, you plan your next investment by:",
        ["A. Increasing position size significantly","B. Using the same strategy with minor tweaks",
         "C. Keeping position size unchanged","D. Diversifying to reduce reliance",
         "E. Reviewing assumptions behind past success"])

    ask_bias("Q11","A stock is trending heavily on social media and business news. You:",
        ["A. Buy immediately","B. Invest a small amount","C. Track it closely first",
         "D. Research fundamentals independently","E. Avoid it due to hype"])

    ask_bias("Q12","You have one stock with large gains and one with losses. You:",
        ["A. Sell the winner to lock profits","B. Hold the loser hoping for recovery",
         "C. Sell part of both","D. Rebalance based on targets","E. Reassess both on fundamentals"])

    ask_bias("Q13","You keep an old investment mainly because:",
        ["A. It feels familiar","B. Changing requires effort",
         "C. You haven’t reviewed alternatives","D. There’s no urgent reason",
         "E. You reassess periodically"])

    ask_bias("Q14","When markets move sharply in a single day, you tend to:",
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

    ask_risk("Q15","Long-Term Wealth Goal (10–15 years)\nYou prefer to:",
        ["A. Protect capital even if growth is limited","B. Earn steady low-volatility returns",
         "C. Balance growth and safety","D. Accept volatility for higher growth",
         "E. Maximise growth despite fluctuations"])

    ask_risk("Q16","Retirement Horizon (20+ years away)\nYour approach would be:",
        ["A. Preserve savings","B. Focus on income assets","C. Mix income and growth",
         "D. Tilt toward growth early","E. Aggressively grow capital"])

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
        responses_numeric = {}

        # -------- BIAS QUESTIONS (REVERSE CODED) --------
        for q, ans in st.session_state.responses["bias"].items():
            # A → 5 (max bias), E → 1 (min bias)
            responses_numeric[q] = 6 - (["A","B","C","D","E"].index(ans[0]) + 1)
        
        # -------- RISK QUESTIONS (NORMAL CODED) --------
        for q, ans in st.session_state.responses["risk"].items():
            # A → 1 (conservative), E → 5 (aggressive)
            responses_numeric[q] = ["A","B","C","D","E"].index(ans[0]) + 1


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

        # ---------------- BFS CARD ----------------
        
        st.markdown(
            "<h2 class='results-title'>Behavioral Finance Score (BFS)</h2>",
            unsafe_allow_html=True
        )


        st.metric(
            "BFS",
            f"{bfs['bfs_score']} / {bfs['max_score']}",
            bfs["category"]
        )

        st.caption(
            "Your Behavioral Finance Score (BFS) is calculated out of **60**, "
            "based on **12 behavioural biases**, each evaluated from your survey responses. "
            "Higher scores indicate **greater susceptibility to behavioural biases**."
        )

        st.markdown(
            "_Each bias intensity score (e.g., **0.75**) is measured **out of 1**, "
            "where higher values indicate stronger influence on decision-making._"
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # ---------------- BIASES CARD ----------------
        
        st.subheader("Detected Behavioral Biases")

        st.markdown(
            "**Bias Intensity Scale**  \n"
            "• **High (0.75)** — Strong influence on decisions  \n"
            "• **Moderate (0.50)** — Situational influence  \n"
            "• **Low (0.25)** — Minimal influence"
        )

        st.markdown("---")

        for bias, data in bias_profile.items():
            st.write(
                f"**{bias}** — {data['level']} "
                f"(Score: {data['score']} / 1)"
            )

        st.markdown("</div>", unsafe_allow_html=True)

        # ---------------- RISK APPETITE CARD ----------------
        avg_risk = risk["average_score"]

        if avg_risk < 2:
            risk_line = (
                f"An average score of **{avg_risk:.2f}/5** indicates a "
                "**conservative risk profile**, with strong preference for stability "
                "and lower volatility."
            )
        elif avg_risk < 3.5:
            risk_line = (
                f"An average score of **{avg_risk:.2f}/5** indicates a "
                "**moderate risk tolerance**, balancing growth opportunities "
                "with risk control."
            )
        else:
            risk_line = (
                f"An average score of **{avg_risk:.2f}/5** indicates a "
                "**higher risk tolerance**, with comfort in volatility "
                "for potential long-term returns."
            )

        
        st.markdown(
            "<h2 class='results-title'>Risk Appetite Assessment</h2>",
            unsafe_allow_html=True
        )


        st.metric(
            "Average Risk Score",
            f"{avg_risk:.2f} / 5",
            risk["category"]
        )

        st.markdown(
            "**Score Explanation:**  \n"
            "Your risk appetite score is calculated on a **1–5 scale**, based solely "
            "on your responses to the assessment questions:"
        )

        st.markdown(
            "• **1** — Very conservative  \n"
            "• **3** — Balanced risk-taking  \n"
            "• **5** — Highly aggressive"
        )

        st.markdown(risk_line)

        st.markdown(
            "_This assessment reflects behavioural tendencies inferred from your answers, "
            "not financial advice or performance predictions._"
        )

        st.markdown("</div>", unsafe_allow_html=True)


# ==================================================
# STATIC PAGES
# ==================================================
# ==================================================
# METHOD
# ==================================================
elif st.session_state.page == "Method":

    st.header("Method")

    st.write(
        "This page explains the theoretical foundations and scoring mechanisms "
        "used to identify behavioural biases and risk appetite."
    )

    st.divider()

    # --------------------------------------------------
    # BEHAVIOURAL FINANCE SCORING (BFS)
    # --------------------------------------------------
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
    
        <h5 style="font-size:1.1rem; font-weight:600; margin-bottom:8px;">
        What We Analysed
        </h5>
    
        <ul style="color:#cfd6dd; font-size:0.92rem; line-height:1.6;">
            <li>Reactions to gains, losses, and price changes</li>
            <li>Responses to market news and trends</li>
            <li>Comfort with uncertainty and volatility</li>
            <li>Decision-making under pressure or social influence</li>
        </ul>
    
        <hr style="border:0.5px solid #2a2f36; margin:20px 0;">
    
        <h5 style="font-size:1.1rem; font-weight:600; margin-bottom:8px;">
        How the Score Works
        </h5>
    
        <ul style="color:#cfd6dd; font-size:0.92rem; line-height:1.6;">
            <li>BFS is calculated <strong>out of 60</strong>, based on <strong>12 behavioural biases</strong></li>
            <li>Each bias contributes equally to the final score</li>
            <li>Higher scores indicate greater susceptibility to behavioural biases</li>
            <li>Lower scores suggest more disciplined and emotionally neutral decisions</li>
        </ul>
    
        <p style="color:#9ba3af; font-size:0.9rem; margin-top:10px;">
        This score is diagnostic — it highlights tendencies, not mistakes.
        </p>
    
        <hr style="border:0.5px solid #2a2f36; margin:20px 0;">
    
        <h5 style="font-size:1.1rem; font-weight:600; margin-bottom:8px;">
        Understanding Bias Intensity
        </h5>
    
        <p style="color:#cfd6dd; font-size:0.92rem; line-height:1.6;">
        Each detected bias is assigned an <strong>intensity score between 0 and 1</strong>,
        where higher values indicate a stronger influence on decision-making.
        </p>
    
        <ul style="color:#cfd6dd; font-size:0.92rem; line-height:1.6;">
            <li><strong>0.00 – 0.33</strong> → Low influence</li>
            <li><strong>0.34 – 0.66</strong> → Moderate influence</li>
            <li><strong>0.67 – 1.00</strong> → High influence</li>
        </ul>
    
        <p style="color:#9ba3af; font-size:0.9rem; margin-top:10px;">
        Scores are based on patterns across multiple responses, not any single answer.
        </p>
        """, unsafe_allow_html=True)


    # --------------------------------------------------
    # RISK APPETITE SCORING
    # --------------------------------------------------
    with st.expander("Risk Appetite Scoring"):

        st.markdown("""
        <h4 style="font-size:1.3rem; font-weight:700; margin-bottom:10px;">
        How Your Risk Appetite Score Is Determined
        </h4>
        
        <p style="color:#cfd6dd; font-size:0.95rem; line-height:1.6;">
        Your <strong>Risk Appetite Score</strong> represents how comfortable you are with
        uncertainty, volatility, and potential losses when making investment decisions.
        </p>
        
        <p style="color:#cfd6dd; font-size:0.95rem; line-height:1.6;">
        Rather than relying on self-declared risk labels, the assessment evaluates
        <strong>behavioural patterns</strong> observed across multiple decision scenarios.
        </p>
        
        <hr style="border:0.5px solid #2a2f36; margin:20px 0;">
        
        <h5 style="font-size:1.1rem; font-weight:600; margin-bottom:8px;">
        What We Analysed
        </h5>
        
        <ul style="color:#cfd6dd; font-size:0.92rem; line-height:1.6;">
            <li>Reactions to portfolio gains and losses</li>
            <li>Willingness to tolerate short-term volatility</li>
            <li>Preference for safety versus growth</li>
            <li>Decision-making across different time horizons</li>
        </ul>
        
        <hr style="border:0.5px solid #2a2f36; margin:20px 0;">
        
        <h5 style="font-size:1.1rem; font-weight:600; margin-bottom:8px;">
        How the Score Works
        </h5>
        
        <ul style="color:#cfd6dd; font-size:0.92rem; line-height:1.6;">
            <li>Each response is scored on a <strong>1–5 scale</strong></li>
            <li>Lower values indicate conservative risk preferences</li>
            <li>Higher values indicate greater comfort with risk and volatility</li>
            <li>The final score reflects an <strong>average risk tendency</strong></li>
        </ul>
        
        <p style="color:#9ba3af; font-size:0.9rem; margin-top:10px;">
        This score captures behavioural tendencies inferred from your responses,
        not financial capacity or investment performance.
        </p>
        
        <hr style="border:0.5px solid #2a2f36; margin:20px 0;">
        
        <h5 style="font-size:1.1rem; font-weight:600; margin-bottom:8px;">
        Interpreting Risk Appetite Scores
        </h5>
        
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


    # --------------------------------------------------
    # BEHAVIOURAL–PORTFOLIO INTEGRATION
    # --------------------------------------------------
    with st.expander("Behavioural Bias and Portfolio Integration"):


        st.markdown("""
        This integration enables context-aware insights rather than generic
        recommendations, supporting disciplined decision-making.
        """)
        


    


elif st.session_state.page == "Biases":

    st.header("Biases")
        # --------------------------------------------------
    # BEHAVIOURAL BIASES EXPLAINED
    # --------------------------------------------------

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
            <p style="color:#cfd6dd; font-size:0.92rem; line-height:1.6;">
            {desc}
            </p>
            <p style="color:#9ba3af; font-size:0.9rem;">
            <em>Example: {example}</em>
            </p>
            """, unsafe_allow_html=True)

    bias_expander(
        "Confirmation Bias",
        "Confirmation bias occurs when investors actively look for information that supports their existing beliefs while downplaying or ignoring evidence that challenges them. Over time, this selective attention can strengthen confidence in an incorrect investment view and delay corrective decisions. It often creates emotional attachment to certain stocks or strategies, even when objective data suggests reevaluation.",
        "You believe a company is a great long-term investment, so you focus only on positive news and dismiss poor earnings or warnings as “temporary,” missing early signs of trouble."
    )

    bias_expander(
        "Anchoring",
        "Anchoring bias arises when investors rely too heavily on an initial reference point, such as a purchase price or past valuation. Future decisions are then made relative to this anchor, even when new information makes it irrelevant. This can distort judgement during changing market conditions and prevent timely decision-making.",
        "You bought a stock at ₹1,500 and refuse to sell until it returns to that price, even though the company’s outlook has worsened and the market has moved on."
    )

    bias_expander(
        "Recency Bias",
        "Recency bias occurs when investors place excessive importance on recent events while underestimating long-term trends or historical data. This can lead to overreaction to short-term performance, causing investors to chase recent winners or panic during temporary downturns, often resulting in poorly timed investment decisions.",
        "A stock has performed very well in recent months, so you invest heavily, assuming the trend will continue without checking long-term fundamentals."
    )

    bias_expander(
        "Framing Effect",
        "The framing effect happens when investment decisions are influenced by how information is presented rather than by the actual facts. Different wording, context, or emphasis can trigger different emotional reactions, even when the underlying information remains the same, leading to inconsistent or biased decision-making.",
        "You feel more confident about an investment described as having a “90% success rate” than one described as having a “10% failure rate,” even though both describe the same outcome."
    )

    bias_expander(
        "Risk Sensitivity",
        "Risk sensitivity reflects how strongly an investor emotionally reacts to perceived risk or uncertainty. Highly risk-sensitive individuals may allow fear or anxiety to dominate decision-making, leading to overly cautious behaviour or frequent strategy changes that are not supported by objective analysis or long-term goals.",
        "After repeatedly hearing news about market crashes, you avoid equity investments altogether, even though long-term data shows that downturns are a normal part of markets."
    )

    bias_expander(
        "Loss Aversion",
        "Loss aversion refers to the tendency to experience losses more intensely than equivalent gains. Investors often focus on avoiding losses rather than maximising overall returns, which can lead to irrational decisions such as holding onto losing investments for too long or avoiding beneficial risks altogether.",
        "You keep holding a falling stock to avoid “locking in” a loss, even when switching to a better investment could improve your portfolio."
    )

    bias_expander(
        "Overconfidence",
        "Overconfidence bias occurs when investors overestimate their knowledge, skills, or ability to predict market movements. This false sense of control can lead to excessive trading, insufficient diversification, and underestimation of risk, increasing the likelihood of poor long-term performance.",
        "After a few successful trades, you increase your position sizes, assuming your judgement is always correct, without considering the role of luck or market conditions."
    )

    bias_expander(
        "Herding",
        "Herding bias occurs when investors follow the actions of others instead of making independent decisions. Social influence, fear of missing out, and group behaviour often drive this bias, especially during market booms or crashes, leading to crowded trades and increased risk exposure.",
        "You buy a stock simply because it is trending on social media or everyone around you is investing in it, without understanding the underlying business."
    )

    bias_expander(
        "Disposition Effect",
        "The disposition effect describes the tendency to sell investments that have gained value too quickly while holding onto losing investments for too long. This behaviour is driven by the desire to realise gains and avoid regret associated with losses, often reducing overall portfolio efficiency.",
        "You sell a stock as soon as it shows a small profit but continue holding a losing stock, hoping it will recover, even when there is little reason to expect it will."
    )

    bias_expander(
        "Status Quo Bias",
        "Status quo bias is the preference to maintain existing choices rather than making changes, even when better alternatives exist. Familiarity, inertia, and perceived effort often prevent investors from reviewing or adjusting their portfolios, leading to missed opportunities for improvement.",
        "You keep the same investments for years without reviewing them, simply because changing them feels uncomfortable or requires extra effort."
    )

    bias_expander(
        "Emotional / Overtrading Bias",
        "Emotional or overtrading bias occurs when investment decisions are driven by emotions such as fear, excitement, or stress rather than rational analysis. This can result in frequent trading, poor timing, and higher transaction costs, ultimately harming long-term investment outcomes.",
        "During a highly volatile market day, you rapidly buy and sell assets based on fear or excitement instead of sticking to a long-term plan."
    )

    
    st.divider()


elif st.session_state.page == "About":
    st.header("About")
    st.info("This project is an academic behavioural finance prototype.")
