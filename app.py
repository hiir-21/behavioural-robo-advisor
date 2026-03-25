import streamlit as st
import plotly.graph_objects as go
from survey_logic import generate_full_survey_analysis
from sector_analysis import sector_analysis
from ml_model import predict_sector
from bias_rules import get_dominant_bias

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Behavioural Robo-Advisor",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# SESSION STATE — initialized ONCE, never reset
# --------------------------------------------------
if "robo_result" not in st.session_state:
    st.session_state.robo_result = None
if "survey_completed" not in st.session_state:
    st.session_state.survey_completed = False
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "responses" not in st.session_state:
    st.session_state.responses = {"demographics": {}, "bias": {}, "risk": {}}
if "survey_step" not in st.session_state:
    st.session_state.survey_step = "demographics"

# --------------------------------------------------
# STYLES
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #f5f3ef !important;
    font-family: 'DM Sans', sans-serif !important;
    color: #1a1a18 !important;
}
[data-testid="stHeader"] { background-color: #f5f3ef !important; }
[data-testid="stSidebar"] { background-color: #efecea !important; }
.block-container { padding-top: 0 !important; padding-bottom: 2rem !important; max-width: 860px !important; }
#MainMenu, footer, header { visibility: hidden; }

/* ── NATIVE TABS STYLING — sits right of logo ── */
[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 1px solid #e0ddd7 !important;
    gap: 0 !important;
    background: transparent !important;
    padding-left: 24px !important;
}
[data-testid="stTabs"] button[role="tab"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 400 !important;
    color: #6b6860 !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
    padding: 8px 14px !important;
    white-space: nowrap !important;
}
[data-testid="stTabs"] button[role="tab"]:hover {
    color: #1a1a18 !important;
    background: transparent !important;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #1a1a18 !important;
    font-weight: 500 !important;
    border-bottom: 2px solid #1a1a18 !important;
    background: transparent !important;
}
[data-testid="stTabs"] [data-testid="stTabContent"] {
    padding-top: 24px !important;
}

/* ── BUTTONS — cream box, black border, black text ── */
.stButton > button {
    background: #f5f3ef !important;
    color: #1a1a18 !important;
    border: 1px solid #1a1a18 !important;
    border-radius: 0 !important;
    padding: 10px 22px !important;
    font-size: 13px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    white-space: nowrap !important;
    transition: all 0.15s !important;
    margin-top: 0 !important;
}
.stButton > button:hover {
    background: #1a1a18 !important;
    color: #f5f3ef !important;
}

.ghost-btn .stButton > button {
    background: transparent !important;
    color: #1a1a18 !important;
    border: 1px solid #1a1a18 !important;
}
.ghost-btn .stButton > button:hover {
    background: #1a1a18 !important;
    color: #f5f3ef !important;
}

/* ── HEADINGS ── */
h1, h2, h3 {
    font-family: 'Instrument Serif', serif !important;
    font-weight: 400 !important;
    color: #1a1a18 !important;
    letter-spacing: -0.02em !important;
}

/* ── SELECTBOX ── */
[data-testid="stSelectbox"] > div > div {
    border-radius: 0 !important;
    border-color: #d4d0c9 !important;
    background: #fff !important;
    color: #1a1a18 !important;
}
[data-testid="stSelectbox"] label,
[data-testid="stSelectbox"] label p,
[data-testid="stSelectbox"] span,
[data-testid="stSelectbox"] > div > div > div { color: #1a1a18 !important; }

/* Dropdown popup */
[data-baseweb="popover"], [data-baseweb="popover"] *,
[data-baseweb="menu"], [data-baseweb="menu"] *,
ul[role="listbox"], ul[role="listbox"] li,
div[role="listbox"], div[role="listbox"] * {
    background-color: #fff !important;
    color: #1a1a18 !important;
}
[data-baseweb="menu"] li:hover, ul[role="listbox"] li:hover {
    background-color: #f5f3ef !important;
}
[aria-selected="true"] { background-color: #efecea !important; color: #1a1a18 !important; }

/* ── RADIO ── */
[data-testid="stRadio"] label,
[data-testid="stRadio"] label p,
[data-testid="stRadio"] div,
[data-testid="stRadio"] span { color: #1a1a18 !important; }
[data-testid="stRadio"] > label { color: #1a1a18 !important; font-weight: 500 !important; }

/* ── ALL LABELS ── */
label, label p { color: #1a1a18 !important; }
p, span, div, li { color: #1a1a18; }
[data-testid="stCaptionContainer"] p, small { color: #6b6860 !important; }
[data-testid="stAlert"] p { color: #1a1a18 !important; }

/* ── METRICS ── */
[data-testid="stMetric"] {
    background: #efecea;
    border: 1px solid #e0ddd7;
    padding: 16px 20px;
}
[data-testid="stMetricLabel"] { color: #6b6860 !important; font-size: 12px !important; }
[data-testid="stMetricValue"] { font-family: 'Instrument Serif', serif !important; color: #1a1a18 !important; }

/* ── EXPANDER — force light background always ── */
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p { color: #1a1a18 !important; font-weight: 500 !important; }
[data-testid="stExpander"] { background: #f5f3ef !important; }
[data-testid="stExpander"] > div,
[data-testid="stExpander"] > div > div,
[data-testid="stExpander"] > div > div > div { background: #f5f3ef !important; background-color: #f5f3ef !important; }
details { background: #f5f3ef !important; }
details > div,
details > div * { background-color: #f5f3ef !important; color: #1a1a18 !important; }
details[open] summary ~ * { background-color: #f5f3ef !important; }
/* Override any dark theme Streamlit injects into expander content */
.streamlit-expanderContent,
.streamlit-expanderContent * {
    background-color: #f5f3ef !important;
    color: #1a1a18 !important;
}

/* ── PROGRESS ── */
[data-testid="stProgress"] > div > div { background-color: #c5a35a !important; }
[data-testid="stProgress"] { background: #e0ddd7 !important; }
.progress-label {
    font-size: 0.75rem; color: #9a9690; margin-bottom: 4px;
    letter-spacing: 0.05em; text-transform: uppercase;
}

/* ── CARDS / LAYOUT ── */
.card {
    background: #efecea; border: 1px solid #e0ddd7;
    border-radius: 0; padding: 28px 32px; margin-top: 16px;
}
.summary-card {
    background: #efecea; border: 1px solid #c5a35a;
    border-left: 3px solid #c5a35a; padding: 20px 24px; margin-bottom: 20px;
}
.results-title {
    font-family: 'Instrument Serif', serif; font-size: 1.6rem;
    font-weight: 400; color: #1a1a18; letter-spacing: -0.02em;
    margin-bottom: 12px; display: block;
}
hr { border-color: #e0ddd7 !important; }

/* ── HOME PAGE ── */
.bra-h1 {
    font-family: 'Instrument Serif', serif !important;
    font-size: 52px !important; font-weight: 400 !important;
    line-height: 1.08 !important; letter-spacing: -0.025em !important;
    color: #1a1a18 !important; margin-bottom: 20px !important;
}
.bra-h1 em { font-style: italic; color: #c5a35a; }
.bra-hero-sub {
    font-size: 15px; font-weight: 300; color: #6b6860;
    line-height: 1.7; max-width: 520px; margin-bottom: 8px;
}
.bra-stat-strip {
    border-top: 1px solid #e0ddd7; border-bottom: 1px solid #e0ddd7;
    background: #efecea; padding: 0; display: flex; margin: 32px 0 0;
}
.bra-stat-item {
    padding: 18px 36px 18px 0; display: flex; flex-direction: column;
    gap: 3px; flex-shrink: 0; border-right: 1px solid #e0ddd7; margin-right: 36px;
}
.bra-stat-item:last-child { border-right: none; margin-right: 0; }
.bra-stat-num { font-family: 'Instrument Serif', serif; font-size: 28px; color: #1a1a18; line-height:1; }
.bra-stat-label { font-size: 10px; color: #9a9690; letter-spacing: 0.05em; text-transform: uppercase; margin-top: 4px; }
.bra-ticker-wrap {
    overflow: hidden; border-top: 1px solid #e0ddd7; border-bottom: 1px solid #e0ddd7;
    background: #efecea; padding: 10px 0; margin: 32px 0 0;
}
.bra-ticker { display: flex; white-space: nowrap; animation: bra-tick 26s linear infinite; }
.bra-ticker-item {
    display: inline-flex; align-items: center; gap: 10px; font-size: 11px;
    letter-spacing: 0.07em; text-transform: uppercase;
    color: #9a9690; padding: 0 24px; border-right: 1px solid #d4d0c9; flex-shrink: 0;
}
.bra-ticker-item span { color: #c5a35a; font-weight: 500; }
@keyframes bra-tick { from { transform: translateX(0); } to { transform: translateX(-50%); } }
.bra-section-header {
    display: flex; align-items: baseline; justify-content: space-between;
    margin: 40px 0 16px; border-bottom: 1px solid #e0ddd7; padding-bottom: 10px;
}
.bra-section-label { font-size: 11px; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; color: #9a9690; }
.bra-section-num { font-family: 'Instrument Serif', serif; font-size: 13px; color: #c5a35a; }
.bra-cards { display: grid; grid-template-columns: 1fr 1fr; gap: 1px; background: #e0ddd7; border: 1px solid #e0ddd7; margin-bottom: 8px; }
.bra-card { background: #f5f3ef; padding: 26px 24px; }
.bra-card-icon { width:28px; height:28px; border:1px solid #d4d0c9; display:flex; align-items:center; justify-content:center; margin-bottom:14px; font-size:12px; color:#6b6860; }
.bra-card-title { font-size: 13px; font-weight: 500; color: #1a1a18; margin-bottom: 6px; }
.bra-card-desc { font-size: 12px; font-weight: 300; color: #6b6860; line-height: 1.65; }
.bra-steps { display: grid; grid-template-columns: repeat(3,1fr); gap: 1px; background: #e0ddd7; border: 1px solid #e0ddd7; margin-bottom: 40px; }
.bra-step { background: #f5f3ef; padding: 24px 20px; }
.bra-step-num { font-family: 'Instrument Serif', serif; font-size: 32px; color: #d4d0c9; line-height:1; margin-bottom:12px; }
.bra-step-title { font-size: 13px; font-weight: 500; color: #1a1a18; margin-bottom: 5px; }
.bra-step-desc { font-size: 12px; font-weight: 300; color: #6b6860; line-height: 1.6; }
.bra-footer-note { font-size: 11px; color: #9a9690; margin-top: 40px; padding-top: 16px; border-top: 1px solid #e0ddd7; }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOGO
# --------------------------------------------------
st.markdown("""
<div style="font-family:'Instrument Serif',serif;font-size:17px;color:#1a1a18;
            letter-spacing:-0.01em;padding:16px 0 4px;">
  Behavioural Robo Advisor
</div>
""", unsafe_allow_html=True)

# ==================================================
# TABS — Streamlit native tabs = zero page reloads
# Session state is FULLY preserved between tab clicks
# ==================================================
tab_home, tab_manual, tab_results, tab_method, tab_biases, tab_about = st.tabs(
    ["Home", "Manual Assessment", "Results", "Method", "Biases", "About"]
)


# ══════════════════════════════════════════════════
# TAB 1: HOME + QUICK ANALYSIS
# ══════════════════════════════════════════════════
with tab_home:

    st.markdown("""
    <p class="bra-h1">Invest smarter.</p>
    <p class="bra-hero-sub">
      Identify the psychological patterns shaping your financial decisions —
      backed by behavioural finance research and demographic investor data.
    </p>
    """, unsafe_allow_html=True)

    # QUICK ANALYSIS WIDGET
    st.markdown("""
    <div style="border:1px solid #1a1a18;padding:24px 24px 16px;background:#f5f3ef;margin-top:4px;">
      <div style="font-family:'Instrument Serif',serif;font-size:1.3rem;color:#1a1a18;margin-bottom:4px;">Quick Analysis</div>
      <div style="font-size:12px;color:#9a9690;margin-bottom:16px;">
        Select your demographic for instant behavioural insights — no survey required.
      </div>
    </div>
    """, unsafe_allow_html=True)

    qa_c1, qa_c2, qa_c3 = st.columns([2, 1.5, 1])
    with qa_c1:
        st.markdown("<p style='font-size:11px;color:#9a9690;letter-spacing:0.05em;text-transform:uppercase;margin-bottom:4px;'>Age group</p>", unsafe_allow_html=True)
        qa_age = st.selectbox("Age", ["Choose", "18-25 years", "26-40 years", "41-55 years", "56-70 years", "70+ years"],
                              key="qa_age", label_visibility="collapsed")
    with qa_c2:
        st.markdown("<p style='font-size:11px;color:#9a9690;letter-spacing:0.05em;text-transform:uppercase;margin-bottom:4px;'>Gender</p>", unsafe_allow_html=True)
        qa_gender = st.selectbox("Gender", ["Choose", "Female", "Male"],
                                 key="qa_gender", label_visibility="collapsed")
    with qa_c3:
        st.markdown("<p style='font-size:11px;color:transparent;margin-bottom:4px;'>.</p>", unsafe_allow_html=True)
        qa_run = st.button("Analyse →", key="qa_run")

    st.markdown("<div style='padding:10px 24px;background:#efecea;border:1px solid #1a1a18;border-top:none;font-size:11px;color:#9a9690;margin-bottom:8px;'>Or use the Manual Assessment tab for a detailed personal bias profile and risk score.</div>", unsafe_allow_html=True)

    if qa_run:
        if qa_age == "Choose" or qa_gender == "Choose":
            st.warning("Please select both age group and gender.")
        else:
            with st.spinner("Analysing demographic patterns..."):
                most_sector, least_sector, sector_avg = sector_analysis(qa_age, qa_gender)
                ml_sector   = predict_sector(qa_age, qa_gender)
                bias_result = get_dominant_bias(qa_age, qa_gender)
                bias        = bias_result.get("dominant", "Insufficient data")
            # Store in session state — persists across all tab clicks
            st.session_state.robo_result = {
                "age": qa_age, "gender": qa_gender, "bias": bias,
                "sector": most_sector, "least_sector": least_sector,
                "ml_sector": ml_sector, "sector_avg": sector_avg
            }
            st.success("Analysis complete! View full results in the Results tab.")

    # Show inline preview if QA already done
    if st.session_state.robo_result:
        r = st.session_state.robo_result
        st.markdown(f"""
        <div style="border-left:3px solid #c5a35a;padding:12px 20px;background:#efecea;margin-top:12px;">
          <div style="font-size:11px;color:#9a9690;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:6px;">Last analysis — {r['age']} · {r['gender']}</div>
          <div style="font-size:13px;color:#1a1a18;">Dominant bias: <strong>{r['bias']}</strong> &nbsp;·&nbsp; Top sector: <strong>{r['sector'] or 'N/A'}</strong></div>
        </div>
        """, unsafe_allow_html=True)

    # Rest of home page
    st.markdown("""
    <div class="bra-stat-strip">
      <div class="bra-stat-item"><div class="bra-stat-num">11</div><div class="bra-stat-label">Biases tracked</div></div>
      <div class="bra-stat-item"><div class="bra-stat-num">22</div><div class="bra-stat-label">Survey questions</div></div>
      <div class="bra-stat-item"><div class="bra-stat-num">5</div><div class="bra-stat-label">Age cohorts</div></div>
      <div class="bra-stat-item"><div class="bra-stat-num">2</div><div class="bra-stat-label">Analysis modes</div></div>
      <div class="bra-stat-item"><div class="bra-stat-num">BFS</div><div class="bra-stat-label">Proprietary scoring</div></div>
    </div>

    <div class="bra-ticker-wrap">
      <div class="bra-ticker">
        <div class="bra-ticker-item">Confirmation Bias <span>›</span></div>
        <div class="bra-ticker-item">Loss Aversion <span>›</span></div>
        <div class="bra-ticker-item">Anchoring <span>›</span></div>
        <div class="bra-ticker-item">Herding <span>›</span></div>
        <div class="bra-ticker-item">Overconfidence <span>›</span></div>
        <div class="bra-ticker-item">Recency Bias <span>›</span></div>
        <div class="bra-ticker-item">Framing Effect <span>›</span></div>
        <div class="bra-ticker-item">Disposition Effect <span>›</span></div>
        <div class="bra-ticker-item">Status Quo Bias <span>›</span></div>
        <div class="bra-ticker-item">Risk Sensitivity <span>›</span></div>
        <div class="bra-ticker-item">Overtrading Bias <span>›</span></div>
        <div class="bra-ticker-item">Confirmation Bias <span>›</span></div>
        <div class="bra-ticker-item">Loss Aversion <span>›</span></div>
        <div class="bra-ticker-item">Anchoring <span>›</span></div>
        <div class="bra-ticker-item">Herding <span>›</span></div>
        <div class="bra-ticker-item">Overconfidence <span>›</span></div>
        <div class="bra-ticker-item">Recency Bias <span>›</span></div>
        <div class="bra-ticker-item">Framing Effect <span>›</span></div>
        <div class="bra-ticker-item">Disposition Effect <span>›</span></div>
        <div class="bra-ticker-item">Status Quo Bias <span>›</span></div>
        <div class="bra-ticker-item">Risk Sensitivity <span>›</span></div>
        <div class="bra-ticker-item">Overtrading Bias <span>›</span></div>
      </div>
    </div>

    <div class="bra-section-header">
      <div class="bra-section-label">What you get</div>
      <div class="bra-section-num">01</div>
    </div>
    <div class="bra-cards">
      <div class="bra-card">
        <div class="bra-card-icon">&#9678;</div>
        <div class="bra-card-title">Behavioural Finance Score</div>
        <div class="bra-card-desc">A single score out of 60 quantifying how strongly cognitive biases influence your investment decisions.</div>
      </div>
      <div class="bra-card">
        <div class="bra-card-icon">&#9638;</div>
        <div class="bra-card-title">Bias Intensity Profile</div>
        <div class="bra-card-desc">Visualise each of 11 biases — rated Low, Moderate, or High — based on your real scenario responses.</div>
      </div>
      <div class="bra-card">
        <div class="bra-card-icon">&#9672;</div>
        <div class="bra-card-title">Risk Appetite Classification</div>
        <div class="bra-card-desc">Understand whether your financial temperament is conservative, moderate, or aggressive — and why.</div>
      </div>
      <div class="bra-card">
        <div class="bra-card-icon">&#9677;</div>
        <div class="bra-card-title">Demographic Sector Insights</div>
        <div class="bra-card-desc">See how investors in your age group allocate across sectors — powered by real survey data.</div>
      </div>
    </div>

    <div class="bra-section-header">
      <div class="bra-section-label">How it works</div>
      <div class="bra-section-num">02</div>
    </div>
    <div class="bra-steps">
      <div class="bra-step">
        <div class="bra-step-num">01</div>
        <div class="bra-step-title">Choose your path</div>
        <div class="bra-step-desc">Use Quick Analysis above for instant demographic insights, or take the full Manual Assessment for a detailed personal profile.</div>
      </div>
      <div class="bra-step">
        <div class="bra-step-num">02</div>
        <div class="bra-step-title">Answer scenario questions</div>
        <div class="bra-step-desc">22 carefully designed questions test your real decision-making instincts — not what you think you should do.</div>
      </div>
      <div class="bra-step">
        <div class="bra-step-num">03</div>
        <div class="bra-step-title">Get your results</div>
        <div class="bra-step-desc">Receive a bias profile, BFS score, risk classification, and sector allocation — all in one dashboard.</div>
      </div>
    </div>
    <div class="bra-footer-note">Academic project · Not financial advice · For research purposes only</div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════
# TAB 2: MANUAL ASSESSMENT (multi-step inside one tab)
# ══════════════════════════════════════════════════
with tab_manual:

    if st.session_state.survey_completed:
        st.markdown("""
        <div style="border-left:3px solid #7aab8a;padding:12px 20px;background:#efecea;margin-bottom:20px;font-size:13px;color:#1a1a18;">
          Manual Assessment already completed. Your results are in the Results tab.
        </div>
        """, unsafe_allow_html=True)
        if st.button("Retake Assessment", key="retake"):
            st.session_state.survey_completed = False
            st.session_state.analysis_result = None
            st.session_state.responses = {"demographics": {}, "bias": {}, "risk": {}}
            st.session_state.survey_step = "demographics"
            st.rerun()

    else:
        step = st.session_state.survey_step

        # ── STEP 1: DEMOGRAPHICS ──
        if step == "demographics":
            st.markdown('<p class="progress-label">Step 1 of 3 — Basic Information</p>', unsafe_allow_html=True)
            st.progress(0.33)
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            st.header("Basic Information")

            s_age    = st.selectbox("Q1. Select your age group",  ["18–25", "26–35", "36–50", "50+"], index=None, key="s_age")
            s_gender = st.selectbox("Q2. Select your gender", ["Female", "Male", "Prefer not to say"], index=None, key="s_gender")

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if st.button("Next →", key="demo_next"):
                if s_age and s_gender:
                    st.session_state.responses["demographics"] = {"Q1": s_age, "Q2": s_gender}
                    st.session_state.survey_step = "bias"
                    st.rerun()
                else:
                    st.warning("Please answer both questions.")

        # ── STEP 2: BIAS QUESTIONS ──
        elif step == "bias":
            st.markdown('<p class="progress-label">Step 2 of 3 — Investment Decision Scenarios</p>', unsafe_allow_html=True)
            st.progress(0.66)
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            st.header("Investment Decision Scenarios")

            def ask_bias(q, text, opts):
                st.session_state.responses["bias"][q] = st.radio(text, opts, index=None, key=f"b_{q}")

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

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            bc, nc, _ = st.columns([1, 1, 3])
            with bc:
                st.markdown('<div class="ghost-btn">', unsafe_allow_html=True)
                if st.button("← Back", key="bias_back"):
                    st.session_state.survey_step = "demographics"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with nc:
                if st.button("Next →", key="bias_next"):
                    if all(st.session_state.responses["bias"].get(f"Q{i}") for i in range(3, 15)):
                        st.session_state.survey_step = "risk"
                        st.rerun()
                    else:
                        st.warning("Please answer all questions.")

        # ── STEP 3: RISK QUESTIONS ──
        elif step == "risk":
            st.markdown('<p class="progress-label">Step 3 of 3 — Personal Finance Preferences</p>', unsafe_allow_html=True)
            st.progress(1.0)
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            st.header("Personal Finance Preferences")

            def ask_risk(q, text, opts):
                st.session_state.responses["risk"][q] = st.radio(text, opts, index=None, key=f"r_{q}")

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

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            bc2, sc, _ = st.columns([1, 1, 3])
            with bc2:
                st.markdown('<div class="ghost-btn">', unsafe_allow_html=True)
                if st.button("← Back", key="risk_back"):
                    st.session_state.survey_step = "bias"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with sc:
                if st.button("Submit Survey", key="risk_submit"):
                    responses_numeric = {}
                    for q, ans in st.session_state.responses["bias"].items():
                        responses_numeric[q] = 6 - (["A","B","C","D","E"].index(ans[0]) + 1)
                    for q, ans in st.session_state.responses["risk"].items():
                        responses_numeric[q] = ["A","B","C","D","E"].index(ans[0]) + 1
                    st.session_state.analysis_result = generate_full_survey_analysis(responses_numeric)
                    st.session_state.survey_completed = True
                    st.session_state.survey_step = "demographics"
                    st.success("Assessment complete! View your results in the Results tab.")
                    st.rerun()


# ══════════════════════════════════════════════════
# TAB 3: RESULTS
# ══════════════════════════════════════════════════
with tab_results:

    has_robo   = st.session_state.robo_result is not None
    has_survey = st.session_state.survey_completed

    st.header("Results")

    # ── EMPTY STATE ──
    if not has_robo and not has_survey:
        st.markdown("""
        <div style="border:1px solid #e0ddd7;background:#efecea;padding:28px 32px;margin-bottom:20px;">
          <div style="font-family:'Instrument Serif',serif;font-size:1.3rem;color:#1a1a18;margin-bottom:8px;">No analysis completed yet</div>
          <div style="font-size:13px;color:#6b6860;">
            Go to the <strong>Home</strong> tab to run a Quick Analysis, or use the
            <strong>Manual Assessment</strong> tab to take the full survey.
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── NUDGE: only QA done ──
    elif has_robo and not has_survey:
        st.markdown("""
        <div style="border-left:3px solid #c5a35a;padding:10px 18px;background:#efecea;margin-bottom:20px;font-size:13px;color:#6b6860;">
          Quick Analysis complete. Switch to the <strong>Manual Assessment</strong> tab for a personal BFS score and bias profile.
        </div>
        """, unsafe_allow_html=True)

    # ── NUDGE: only survey done ──
    elif has_survey and not has_robo:
        st.markdown("""
        <div style="border-left:3px solid #c5a35a;padding:10px 18px;background:#efecea;margin-bottom:20px;font-size:13px;color:#6b6860;">
          Manual Assessment complete. Go to the <strong>Home</strong> tab to also run a Quick Analysis for demographic sector insights.
        </div>
        """, unsafe_allow_html=True)

    # ── COMBINED SUMMARY — both done ──
    if has_robo and has_survey:
        robo    = st.session_state.robo_result
        an      = st.session_state.analysis_result
        bfs_sum = an["behavioral_bias_analysis"]["bfs_summary"]
        ras     = an["risk_appetite_analysis"]

        st.markdown('<div class="summary-card"><p style="font-family:\'Instrument Serif\',serif;font-size:1.15rem;color:#1a1a18;margin:0 0 12px;">Your Investment Behaviour Summary</p></div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("Dominant Bias", robo["bias"])
        with c2: st.metric("BFS Score", f"{bfs_sum['bfs_score']} / 60", bfs_sum["category"])
        with c3: st.metric("Risk Profile", ras["category"], f"{ras['average_score']:.2f} / 5")
        st.divider()

    # ── ROBO RESULTS ──
    if has_robo:
        robo = st.session_state.robo_result
        st.markdown("<span class='results-title'>Quick Analysis — Demographic Insight</span>", unsafe_allow_html=True)
        st.write(f"**Age Group:** {robo['age']}  |  **Gender:** {robo['gender']}")
        st.write(f"Investors in this demographic most commonly exhibit **{robo['bias']}**.")

        if robo["sector"] is None:
            st.warning("Insufficient sector data for this demographic.")
        else:
            col_a, col_b = st.columns(2)
            with col_a: st.metric("Most Preferred Sector", robo["sector"])
            with col_b: st.metric("ML Predicted Sector", robo["ml_sector"])
            st.caption(f"Least preferred: **{robo['least_sector']}**")

            sector_data = robo["sector_avg"]
            fig_s = go.Figure(go.Bar(
                x=list(sector_data.index), y=list(sector_data.values),
                marker=dict(color=list(sector_data.values), colorscale=[[0,"#d4c4a0"],[1,"#c5a35a"]], showscale=False),
                text=[f"{v:.1f}%" for v in sector_data.values],
                textposition="outside", textfont=dict(color="#1a1a18", size=10)
            ))
            fig_s.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#1a1a18", family="DM Sans"),
                xaxis=dict(tickangle=-35, gridcolor="#e0ddd7", tickfont=dict(size=11, color="#6b6860")),
                yaxis=dict(gridcolor="#e0ddd7", title="Avg Allocation (%)", tickfont=dict(color="#6b6860")),
                margin=dict(t=20, b=80, l=40, r=20), height=340
            )
            st.plotly_chart(fig_s, use_container_width=True)

        if has_survey:
            st.divider()

    # ── SURVEY RESULTS ──
    if has_survey:
        an           = st.session_state.analysis_result
        bfs          = an["behavioral_bias_analysis"]["bfs_summary"]
        bias_profile = an["behavioral_bias_analysis"]["bias_profile"]
        risk         = an["risk_appetite_analysis"]

        st.markdown("<span class='results-title'>Manual Assessment — Behavioural Finance Score</span>", unsafe_allow_html=True)
        st.metric("BFS", f"{bfs['bfs_score']} / {bfs['max_score']}", bfs["category"])
        st.caption("Out of 60 across 12 behavioural biases. Higher = greater susceptibility.")

        st.markdown("<p style='font-size:13px;font-weight:500;color:#1a1a18;margin:24px 0 8px;'>Bias Intensity Profile</p>", unsafe_allow_html=True)

        bias_names  = list(bias_profile.keys())
        bias_scores = [bias_profile[b]["score"] for b in bias_names]
        bias_levels = [bias_profile[b]["level"] for b in bias_names]
        cmap        = {"High": "#c0392b", "Moderate": "#c5a35a", "Low": "#7aab8a"}
        bcolors     = [cmap.get(l, "#9a9690") for l in bias_levels]

        fig_b = go.Figure(go.Bar(
            x=bias_scores, y=bias_names, orientation="h",
            marker=dict(color=bcolors),
            text=[f"{s:.2f} — {l}" for s, l in zip(bias_scores, bias_levels)],
            textposition="outside", textfont=dict(color="#1a1a18", size=11)
        ))
        fig_b.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#1a1a18", family="DM Sans"),
            xaxis=dict(range=[0,1.3], gridcolor="#e0ddd7", title="Intensity (0–1)", tickfont=dict(color="#6b6860")),
            yaxis=dict(gridcolor="#e0ddd7", tickfont=dict(size=11, color="#1a1a18")),
            margin=dict(t=10, b=30, l=180, r=110), height=400,
            shapes=[
                dict(type="line", x0=0.33, x1=0.33, y0=-0.5, y1=len(bias_names)-0.5, line=dict(color="#c5c0b8", width=1, dash="dot")),
                dict(type="line", x0=0.66, x1=0.66, y0=-0.5, y1=len(bias_names)-0.5, line=dict(color="#c5c0b8", width=1, dash="dot")),
            ]
        )
        st.plotly_chart(fig_b, use_container_width=True)
        st.caption("Dotted lines mark Low / Moderate / High thresholds at 0.33 and 0.66.")

        avg_risk = risk["average_score"]
        risk_line = (
            f"A score of **{avg_risk:.2f}/5** indicates a **conservative risk profile**." if avg_risk < 2 else
            f"A score of **{avg_risk:.2f}/5** indicates **moderate risk tolerance**." if avg_risk < 3.5 else
            f"A score of **{avg_risk:.2f}/5** indicates **higher risk tolerance**."
        )
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown("<span class='results-title'>Risk Appetite Assessment</span>", unsafe_allow_html=True)
        st.metric("Average Risk Score", f"{avg_risk:.2f} / 5", risk["category"])
        st.markdown("**Scale:** 1 = Very conservative · 3 = Balanced · 5 = Highly aggressive")
        st.markdown(risk_line)
        st.caption("Reflects behavioural tendencies — not financial advice.")


# ══════════════════════════════════════════════════
# TAB 4: METHOD
# ══════════════════════════════════════════════════
with tab_method:
    st.header("Method")
    st.write("Theoretical foundations and scoring mechanisms used in this assessment.")
    st.divider()

    with st.expander("Behavioural Finance Scoring (BFS)"):
        st.markdown("""
        **BFS** reflects how strongly behavioural biases influence investment decisions.

        - Calculated **out of 60** across **12 behavioural biases**
        - Each bias contributes equally · Higher = greater susceptibility

        **Bias intensity (0–1):**
        - 0.00–0.33 → Low · 0.34–0.66 → Moderate · 0.67–1.00 → High
        """)

    with st.expander("Risk Appetite Scoring (RAS)"):
        st.markdown("""
        Captures comfort with uncertainty through Q15–Q22.

        - Each response scored **1–5** (1 = conservative, 5 = aggressive)
        - Final score = average across all eight questions

        **Interpretation:** 1.0–2.0 Conservative · 2.1–3.5 Moderate · 3.6–5.0 Aggressive
        """)

    with st.expander("Demographic Bias Inference (Quick Analysis)"):
        st.markdown("""
        Uses pre-computed average bias scores per age group from ~135 primary survey respondents.
        The bias with the highest average score is identified as dominant for that demographic.
        Sector allocation covers 220 investor profiles across 10 market sectors.
        """)

    with st.expander("Behavioural Bias and Portfolio Integration"):
        st.markdown("""
        Combining bias detection with sector preferences enables context-aware insights
        rather than generic recommendations, supporting more disciplined decision-making.
        """)


# ══════════════════════════════════════════════════
# TAB 5: BIASES
# ══════════════════════════════════════════════════
with tab_biases:
    st.header("Behavioural Biases")
    st.write("Psychological patterns that commonly influence real-world investment behaviour.")
    st.divider()

    def bias_card(title, desc, example):
        with st.expander(title):
            st.markdown(desc)
            st.markdown(f"*Example: {example}*")

    bias_card("Confirmation Bias",
        "Seeking information that confirms existing beliefs while ignoring contradictory evidence.",
        "You dismiss poor earnings as \"temporary\" because you believe the company is a great investment.")
    bias_card("Anchoring",
        "Over-reliance on an initial reference point even when new information makes it irrelevant.",
        "You refuse to sell until a stock returns to ₹1,500 — the price you paid — even as fundamentals worsen.")
    bias_card("Recency Bias",
        "Placing excessive importance on recent events while underestimating long-term trends.",
        "A stock performs well for three months, so you invest heavily assuming the trend continues.")
    bias_card("Framing Effect",
        "Decisions influenced by how information is presented rather than its actual content.",
        "\"90% success rate\" feels safer than \"10% failure rate\" — even though they're identical.")
    bias_card("Risk Sensitivity",
        "Emotional overreaction to perceived risk, leading to overly cautious or erratic behaviour.",
        "Repeated crash news causes you to exit equities entirely, despite historical resilience.")
    bias_card("Loss Aversion",
        "Losses feel more painful than equivalent gains feel rewarding.",
        "You hold a falling stock to avoid \"booking\" a loss, even when exiting would be rational.")
    bias_card("Overconfidence",
        "Overestimating one's ability to predict markets, leading to excessive risk.",
        "After a few wins, you double position sizes without questioning whether luck played a role.")
    bias_card("Herding",
        "Following the crowd rather than making independent, research-based decisions.",
        "You buy a trending stock purely because everyone around you is investing in it.")
    bias_card("Disposition Effect",
        "Selling winners too early and holding losers too long.",
        "You sell at a small gain but keep a losing stock for months hoping for a recovery.")
    bias_card("Status Quo Bias",
        "Preference for keeping existing investments unchanged due to inertia.",
        "You haven't reviewed your portfolio in two years because changing it feels effortful.")
    bias_card("Emotional / Overtrading Bias",
        "Letting fear or excitement drive frequent trades rather than a disciplined strategy.",
        "On a volatile day, you place multiple impulsive trades instead of sticking to your plan.")

    st.divider()


# ══════════════════════════════════════════════════
# TAB 6: ABOUT
# ══════════════════════════════════════════════════
with tab_about:
    st.header("About This Project")

    st.markdown("""
    <div class="card">
    <h3>Overview</h3>
    <p>The Behavioural Robo-Advisor is an academic project analysing how psychological biases
    and demographic patterns influence investment decisions. Unlike traditional financial tools
    that focus only on returns and risk, this system integrates behavioural finance principles
    for deeper investor insights.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h3>Objectives</h3>
    <ul>
        <li>Identify behavioural biases in investment decisions among Indian investors</li>
        <li>Develop a Behavioural Finance Scoring System (BFS)</li>
        <li>Analyse patterns across age and gender groups</li>
        <li>Provide data-driven and self-assessment insights through a functional prototype</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h3>Data</h3>
    <ul>
        <li><strong>Primary:</strong> ~135 survey responses from Indian investors</li>
        <li><strong>Secondary:</strong> Sector-wise allocation across 220 investor profiles and 10 market sectors</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h3>Research Basis</h3>
    <ul>
        <li>Barber &amp; Odean (2001) — Gender, Overconfidence and Stock Investment</li>
        <li>Shefrin &amp; Statman (2000) — Behavioural Portfolio Theory</li>
        <li>Pompian (2012) — Behavioural Finance and Investor Types</li>
        <li>NISM and SEBI Investor Reports (2022–2024)</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h3>Disclaimer</h3>
    <p>This tool is developed for academic and research purposes only.
    It does not constitute financial advice or investment recommendations.</p>
    </div>
    """, unsafe_allow_html=True)
