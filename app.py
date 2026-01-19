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

# ---------- SURVEY SECTION ----------
if st.session_state.start:

    st.header("Behavioural Finance Survey")

    st.markdown("### Section I: Behavioural Biases")

    age = st.selectbox("Age Group", ["18–25", "26–35", "36–50", "50+"])
    gender = st.selectbox("Gender", ["Female", "Male", "Prefer not to say"])

    responses = {}

    def ask_question(qno, question, options):
        responses[qno] = st.radio(question, options, key=qno)

    # --- Cognitive Biases ---
    st.subheader("A. Cognitive Biases")

    ask_question(
        "Q1_Confirmation",
        "1. When new information contradicts your investment thesis, you usually:",
        ["A. Assume it is temporary noise",
         "B. Wait for further confirmation",
         "C. Adjust expectations slightly",
         "D. Re-examine the entire thesis",
         "E. Exit or reduce exposure"]
    )

    ask_question(
        "Q2_Anchoring1",
        "2. You bought a stock at ₹1,500; it now trades at ₹1,000. Which thought best reflects your reaction?",
        ["A. It should eventually return to ₹1,500",
         "B. ₹1,500 remains a key reference for my decision",
         "C. Past prices matter less than future performance",
         "D. The fall itself could indicate opportunity",
         "E. Price history alone should not guide decisions"]
    )

    ask_question(
        "Q3_Anchoring2",
        "3. When deciding whether to sell an investment, you rely most on:",
        ["A. The price I originally paid",
         "B. The asset’s previous highest price",
         "C. Current valuation and fundamentals",
         "D. Recent market sentiment and news",
         "E. Long-term expected returns"]
    )

    ask_question(
        "Q4_Recency",
        "4. After a stock performs very well over the last few months, you believe:",
        ["A. The trend will continue",
         "B. Momentum matters more than history",
         "C. Both trend and history matter",
         "D. Long-term data is more reliable",
         "E. Short-term movements are irrelevant"]
    )

    ask_question(
        "Q5_Framing",
        "5. Which presentation makes you more comfortable investing?",
        ["A. 90% success rate",
         "B. Only 10% failure rate",
         "C. Both equally",
         "D. Absolute return numbers",
         "E. Long-term historical averages"]
    )

    ask_question(
        "Q6_Availability",
        "6. After repeated news about market crashes, you:",
        ["A. Feel investing is riskier",
         "B. Reduce exposure temporarily",
         "C. Re-check historical data",
         "D. Proceed cautiously",
         "E. Stick strictly to long-term plans"]
    )

    # --- Emotional Biases ---
    st.subheader("B. Emotional Biases")

    ask_question(
        "Q7_LossAversion",
        "7. Which situation feels most uncomfortable to you as an investor?",
        ["A. Selling an investment at a loss",
         "B. Missing out on a potential gain",
         "C. Making a decision without sufficient information",
         "D. Being wrong in front of others",
         "E. Realising a loss even when it improves future outcomes"]
    )

    ask_question(
        "Q8_Overconfidence",
        "8. After a series of profitable trades, you plan your next investment by:",
        ["A. Increasing position size significantly",
         "B. Using the same strategy with minor tweaks",
         "C. Keeping position size unchanged",
         "D. Diversifying to reduce reliance",
         "E. Reviewing assumptions behind past success"]
    )

    ask_question(
        "Q9_Herd",
        "9. A stock is trending heavily on social media and business news. You:",
        ["A. Buy immediately",
         "B. Invest a small amount",
         "C. Track it closely first",
         "D. Research fundamentals independently",
         "E. Avoid it due to hype"]
    )

    ask_question(
        "Q10_Disposition",
        "10. You have one stock with large gains and one with losses. You:",
        ["A. Sell the winner to lock profits",
         "B. Hold the loser hoping for recovery",
         "C. Sell part of both",
         "D. Rebalance based on targets",
         "E. Reassess both on fundamentals"]
    )

    ask_question(
        "Q11_StatusQuo",
        "11. You keep an old investment mainly because:",
        ["A. It feels familiar",
         "B. Changing requires effort",
         "C. You haven’t reviewed alternatives",
         "D. There’s no urgent reason",
         "E. You reassess periodically"]
    )

    ask_question(
        "Q12_Impulsivity",
        "12. When markets move sharply in a single day, you tend to:",
        ["A. Trade actively",
         "B. Adjust positions quickly",
         "C. Pause and reassess",
         "D. Stick to preset rules",
         "E. Avoid reacting"]
    )

    # --- Risk Appetite ---
    st.markdown("### Section II: Personal Finance & Risk Appetite")

    ask_question(
        "Q13_LongTerm",
        "13. Long-term wealth goal (10–15 years):",
        ["A. Protect capital",
         "B. Low-volatility returns",
         "C. Balance growth and safety",
         "D. Accept volatility",
         "E. Maximise growth"]
    )

    ask_question(
        "Q14_Retirement",
        "14. Retirement horizon (20+ years away):",
        ["A. Preserve savings",
         "B. Focus on income",
         "C. Mix income and growth",
         "D. Tilt toward growth",
         "E. Aggressively grow capital"]
    )

    ask_question(
        "Q15_MediumTerm",
        "15. Medium-term goal (5–7 years):",
        ["A. Fully safe",
         "B. Mostly low-risk",
         "C. Safety + equity",
         "D. Growth assets early",
         "E. Invest aggressively"]
    )

    ask_question(
        "Q16_Drawdown",
        "16. Reaction to a 10–15% portfolio decline:",
        ["A. Exit investments",
         "B. Reduce exposure",
         "C. Hold and wait",
         "D. Increase exposure",
         "E. Rebalance strategically"]
    )

    ask_question(
        "Q17_RiskReturn",
        "17. Risk–return preference:",
        ["A. Lower risk, lower return",
         "B. Moderate risk",
         "C. Market-level risk",
         "D. Higher risk",
         "E. Maximum return regardless"]
    )

    ask_question(
        "Q18_Volatility",
        "18. Your view on market volatility:",
        ["A. Avoid it",
         "B. Be cautious",
         "C. Normal part",
         "D. Opportunity",
         "E. Advantage"]
    )

    ask_question(
        "Q19_IncomeGrowth",
        "19. Income vs growth orientation:",
        ["A. Stable income",
         "B. Mostly income",
         "C. Equal",
         "D. Mostly growth",
         "E. Growth first"]
    )

    ask_question(
        "Q20_TimeRisk",
        "20. Time vs certainty trade-off:",
        ["A. Choose safety",
         "B. Lean safety",
         "C. Balance both",
         "D. Faster route",
         "E. Speed despite risk"]
    )

    if st.button("Submit Survey"):
        st.success("Survey submitted successfully.")
        st.write("Responses captured. Behavioural analysis will be shown next.")
        st.session_state.responses = responses
