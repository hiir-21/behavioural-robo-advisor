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
# SESSION STATE
# --------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "responses" not in st.session_state:
    st.session_state.responses = {"demographics": {}, "bias": {}, "risk": {}}
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
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500&display=swap');

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background-color: #f5f3ef !important;
    font-family: 'DM Sans', sans-serif !important;
    color: #1a1a18 !important;
}
[data-testid="stHeader"]  { background-color: #f5f3ef !important; }
[data-testid="stSidebar"] { background-color: #efecea !important; }
.block-container { padding-top: 0 !important; padding-bottom: 2rem !important; max-width: 860px !important; }
#MainMenu, footer, header { visibility: hidden; }

/* ── ALL STREAMLIT BUTTONS — dark filled, readable ── */
.stButton > button {
    background: #1a1a18 !important;
    color: #f5f3ef !important;
    border: 1px solid #1a1a18 !important;
    border-radius: 0 !important;
    padding: 10px 22px !important;
    font-size: 13px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
    white-space: nowrap !important;
    transition: background 0.15s !important;
    margin-top: 0 !important;
    min-width: 0 !important;
    width: auto !important;
}
.stButton > button:hover { background: #2f2f2c !important; border-color: #2f2f2c !important; }

/* ── GHOST BUTTON — target by key ── */
button[kind="secondary"],
[data-testid="stButton"] button[kind="secondary"] {
    background: transparent !important;
    color: #1a1a18 !important;
    border: 1px solid #1a1a18 !important;
}

/* Specific ghost buttons by key */
[data-testid="stButton"]:has(button[data-testid*="home_method"]) button,
[data-testid="stButton"]:has(button[data-testid*="bias_back"]) button,
[data-testid="stButton"]:has(button[data-testid*="risk_back"]) button {
    background: transparent !important;
    color: #1a1a18 !important;
    border: 1px solid #c5a35a !important;
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

/* ── INLINE HTML NAVBAR ── */
.bra-nav-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 0 12px;
    border-bottom: 1px solid #e0ddd7;
    margin-bottom: 24px;
    flex-wrap: nowrap;
    gap: 0;
}
.bra-nav-links {
    display: flex;
    align-items: center;
    gap: 0;
    list-style: none;
    margin: 0; padding: 0;
    flex-wrap: nowrap;
}
.bra-nav-link {
    font-size: 13px;
    font-weight: 400;
    color: #6b6860 !important;
    padding: 6px 12px;
    cursor: pointer;
    text-decoration: none;
    white-space: nowrap;
    letter-spacing: 0.01em;
    background: none;
    border: none;
    font-family: 'DM Sans', sans-serif;
    transition: color 0.15s;
}
.bra-nav-link:hover { color: #1a1a18 !important; }
.bra-nav-link.active { color: #1a1a18 !important; font-weight: 500; }
.bra-nav-cta-btn {
    background: #1a1a18;
    color: #f5f3ef !important;
    border: none;
    padding: 8px 16px;
    font-size: 12px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    cursor: pointer;
    white-space: nowrap;
    letter-spacing: 0.01em;
    transition: background 0.15s;
    margin-left: 16px;
    flex-shrink: 0;
}
.bra-nav-cta-btn:hover { background: #2f2f2c; }

/* Progress bar colour fix */
[data-testid="stProgress"] > div > div {
    background-color: #c5a35a !important;
}

h1, h2, h3 {
    font-family: 'Instrument Serif', serif !important;
    font-weight: 400 !important;
    color: #1a1a18 !important;
    letter-spacing: -0.02em !important;
}

.card {
    background: #efecea;
    border: 1px solid #e0ddd7;
    border-radius: 0;
    padding: 28px 32px;
    margin-top: 16px;
}

.results-title {
    font-family: 'Instrument Serif', serif;
    font-size: 1.6rem;
    font-weight: 400;
    color: #1a1a18;
    letter-spacing: -0.02em;
    margin-bottom: 12px;
    display: block;
}

.summary-card {
    background: #efecea;
    border: 1px solid #c5a35a;
    border-left: 3px solid #c5a35a;
    padding: 20px 24px;
    margin-bottom: 20px;
}

.progress-label {
    font-size: 0.75rem;
    color: #9a9690;
    margin-bottom: 4px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    font-family: 'DM Sans', sans-serif;
}

hr { border-color: #e0ddd7 !important; }

[data-testid="stMetric"] {
    background: #efecea;
    border: 1px solid #e0ddd7;
    padding: 16px 20px;
}
[data-testid="stMetricLabel"] { color: #6b6860 !important; font-size: 12px !important; }
[data-testid="stMetricValue"] {
    font-family: 'Instrument Serif', serif !important;
    color: #1a1a18 !important;
}

/* ── SELECTBOX — label, placeholder, selected value all dark ── */
[data-testid="stSelectbox"] > div > div {
    border-radius: 0 !important;
    border-color: #d4d0c9 !important;
    background: #fff !important;
}
[data-testid="stSelectbox"] label,
[data-testid="stSelectbox"] label p,
[data-testid="stSelectbox"] span {
    color: #1a1a18 !important;
}
[data-testid="stSelectbox"] > div > div > div {
    color: #1a1a18 !important;
}

/* ── RADIO BUTTONS — all text dark ── */
[data-testid="stRadio"] label,
[data-testid="stRadio"] label p,
[data-testid="stRadio"] div,
[data-testid="stRadio"] span {
    color: #1a1a18 !important;
}
[data-testid="stRadio"] > label {
    color: #1a1a18 !important;
    font-weight: 500 !important;
    font-size: 14px !important;
}

/* ── ALL FORM LABELS ── */
label, label p, .stSelectbox label, .stRadio label {
    color: #1a1a18 !important;
}

/* ── GENERAL TEXT — catch-all for any missed elements ── */
p, span, div, li {
    color: #1a1a18;
}

/* ── CAPTIONS & HELP TEXT ── */
[data-testid="stCaptionContainer"] p,
small, .stCaption {
    color: #6b6860 !important;
}

/* ── WARNINGS / INFO ── */
[data-testid="stAlert"] p { color: #1a1a18 !important; }

/* ── PLOTLY CHARTS — fix text on light bg ── */
.js-plotly-plot .plotly .gtitle,
.js-plotly-plot .plotly text { fill: #1a1a18 !important; }

/* ── GHOST BUTTON — use data-key attribute trick ── */
[data-testid="baseButton-secondary"] {
    background: transparent !important;
    color: #1a1a18 !important;
    border: 1px solid #1a1a18 !important;
}
[data-testid="baseButton-secondary"]:hover {
    background: #1a1a18 !important;
    color: #f5f3ef !important;
}

/* ── EXPANDER ── */
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p {
    color: #1a1a18 !important;
    font-weight: 500 !important;
}
[data-testid="stExpander"] div p {
    color: #1a1a18 !important;
}

/* ── PROGRESS BAR TEXT ── */
[data-testid="stProgress"] { background: #e0ddd7 !important; }

.bra-logo {
    font-family: 'Instrument Serif', serif;
    font-size: 17px;
    color: #1a1a18;
    letter-spacing: -0.01em;
    padding: 6px 0;
}
.bra-logo span { color: #c5a35a; }

.bra-eyebrow {
    display: inline-flex; align-items: center; gap: 8px;
    font-size: 11px; font-weight: 500; letter-spacing: 0.1em;
    text-transform: uppercase; color: #6b6860; margin-bottom: 20px;
}
.bra-eyebrow-dot { width:6px; height:6px; border-radius:50%; background:#c5a35a; display:inline-block; }

.bra-h1 {
    font-family: 'Instrument Serif', serif !important;
    font-size: 52px !important; font-weight: 400 !important;
    line-height: 1.08 !important; letter-spacing: -0.025em !important;
    color: #1a1a18 !important; margin-bottom: 20px !important;
}
.bra-h1 em { font-style: italic; color: #c5a35a; }

.bra-hero-sub {
    font-size: 15px; font-weight: 300; color: #6b6860;
    line-height: 1.7; max-width: 480px; margin-bottom: 28px;
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
.bra-stat-num   { font-family: 'Instrument Serif', serif; font-size: 28px; color: #1a1a18; letter-spacing: -0.02em; line-height:1; }
.bra-stat-label { font-size: 10px; font-weight: 400; color: #9a9690; letter-spacing: 0.05em; text-transform: uppercase; margin-top: 4px; }

.bra-ticker-wrap {
    overflow: hidden; border-top: 1px solid #e0ddd7; border-bottom: 1px solid #e0ddd7;
    background: #efecea; padding: 10px 0; margin: 40px 0 0;
}
.bra-ticker { display: flex; white-space: nowrap; animation: bra-tick 26s linear infinite; }
.bra-ticker-item {
    display: inline-flex; align-items: center; gap: 10px; font-size: 11px;
    font-weight: 400; letter-spacing: 0.07em; text-transform: uppercase;
    color: #9a9690; padding: 0 24px; border-right: 1px solid #d4d0c9; flex-shrink: 0;
}
.bra-ticker-item span { color: #c5a35a; font-weight: 500; }
@keyframes bra-tick { from { transform: translateX(0); } to { transform: translateX(-50%); } }

.bra-section-header {
    display: flex; align-items: baseline; justify-content: space-between;
    margin: 40px 0 16px; border-bottom: 1px solid #e0ddd7; padding-bottom: 10px;
}
.bra-section-label { font-size: 11px; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; color: #9a9690; }
.bra-section-num   { font-family: 'Instrument Serif', serif; font-size: 13px; color: #c5a35a; }

.bra-cards { display: grid; grid-template-columns: 1fr 1fr; gap: 1px; background: #e0ddd7; border: 1px solid #e0ddd7; margin-bottom: 8px; }
.bra-card  { background: #f5f3ef; padding: 26px 24px; }
.bra-card-icon  { width:28px; height:28px; border:1px solid #d4d0c9; display:flex; align-items:center; justify-content:center; margin-bottom:14px; font-size:12px; color:#6b6860; }
.bra-card-title { font-size: 13px; font-weight: 500; color: #1a1a18; margin-bottom: 6px; }
.bra-card-desc  { font-size: 12px; font-weight: 300; color: #6b6860; line-height: 1.65; }

.bra-steps { display: grid; grid-template-columns: repeat(3,1fr); gap: 1px; background: #e0ddd7; border: 1px solid #e0ddd7; margin-bottom: 40px; }
.bra-step       { background: #f5f3ef; padding: 24px 20px; }
.bra-step-num   { font-family: 'Instrument Serif', serif; font-size: 32px; color: #d4d0c9; line-height:1; margin-bottom:12px; }
.bra-step-title { font-size: 13px; font-weight: 500; color: #1a1a18; margin-bottom: 5px; }
.bra-step-desc  { font-size: 12px; font-weight: 300; color: #6b6860; line-height: 1.6; }

.bra-footer-note { font-size: 11px; color: #9a9690; letter-spacing: 0.02em; margin-top: 40px; padding-top: 16px; border-top: 1px solid #e0ddd7; }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# NAVBAR — HTML links + query_params routing
# --------------------------------------------------
_page = st.session_state.page
_nav_tabs = ["Home", "Manual Assessment", "Results", "Method", "Biases", "About"]

def _link(tab, current):
    cls = "bra-nav-link active" if current == tab else "bra-nav-link"
    return f'<a class="{cls}" href="?nav={tab}">{tab}</a>'

_links = "".join(_link(t, _page) for t in _nav_tabs)

st.markdown(f"""
<div class="bra-nav-bar">
  <div class="bra-logo">Behavioural<span>.</span>Advisor</div>
  <nav class="bra-nav-links">{_links}</nav>
  <a href="?nav=RoboAdvisor" class="bra-nav-cta-btn">Quick Analysis →</a>
</div>
""", unsafe_allow_html=True)

# Handle navbar clicks via query params
_qp = st.query_params
if "nav" in _qp:
    _dest = _qp["nav"]
    if _dest != st.session_state.page:
        st.session_state.page = _dest
        st.query_params.clear()
        st.rerun()


# ==================================================
# HOME
# ==================================================
if st.session_state.page == "Home":

    st.markdown("""
    <p class="bra-h1">Invest smarter.<br>Understand your <em>biases</em> first.</p>
    <p class="bra-hero-sub">
      Identify the psychological patterns shaping your financial decisions —
      backed by behavioural finance research and demographic investor data.
    </p>
    """, unsafe_allow_html=True)

    btn_col1, btn_col2, _ = st.columns([1, 1, 2])
    with btn_col1:
        if st.button("Start Full Assessment", key="home_start"):
            st.session_state.page = "Survey-Demographics"
            st.rerun()
    with btn_col2:
        st.markdown('<div class="ghost-btn">', unsafe_allow_html=True)
        if st.button("Learn the method", key="home_method"):
            st.session_state.page = "Method"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # QUICK ANALYSIS — inline on home page
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="border-top:2px solid #1a1a18;padding-top:20px;margin-bottom:8px;">
      <span style="font-family:'Instrument Serif',serif;font-size:1.15rem;color:#1a1a18;">Quick Analysis</span>
      <span style="font-size:12px;color:#9a9690;margin-left:14px;">Instant demographic insights — no survey required</span>
    </div>
    """, unsafe_allow_html=True)

    qa_age_col, qa_gender_col, qa_btn_col = st.columns([2, 1.5, 1])
    with qa_age_col:
        qa_age = st.selectbox("Age group", ["18-25 years", "26-40 years", "41-55 years", "56-70 years", "70+ years"], key="home_qa_age", label_visibility="collapsed")
    with qa_gender_col:
        qa_gender = st.selectbox("Gender", ["Female", "Male"], key="home_qa_gender", label_visibility="collapsed")
    with qa_btn_col:
        if st.button("Analyse →", key="home_qa_run"):
            with st.spinner("Analysing..."):
                most_sector, least_sector, sector_avg = sector_analysis(qa_age, qa_gender)
                ml_sector   = predict_sector(qa_age, qa_gender)
                bias_result = get_dominant_bias(qa_age, qa_gender)
                bias        = bias_result.get("dominant", "Insufficient data")
            st.session_state.robo_result = {
                "age": qa_age, "gender": qa_gender, "bias": bias,
                "sector": most_sector, "least_sector": least_sector,
                "ml_sector": ml_sector, "sector_avg": sector_avg
            }
            st.session_state.page = "Results"
            st.rerun()

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

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
        <div class="bra-step-desc">Use Quick Analysis above for instant demographic insights, or take the full assessment for a detailed personal profile.</div>
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


# ==================================================
# ROBO ADVISOR — redirects to Home where QA lives
# ==================================================
elif st.session_state.page == "RoboAdvisor":
    st.session_state.page = "Home"
    st.rerun()


# ==================================================
# MANUAL ASSESSMENT ENTRY
# ==================================================
elif st.session_state.page == "Manual Assessment":

    st.header("Manual Behavioural Assessment")
    st.markdown("<p style='color:#6b6860;font-size:14px;margin-top:-8px;'>22 scenario-based questions. Takes about 5 minutes.</p>", unsafe_allow_html=True)
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        if st.button("Begin Assessment", key="manual_start", use_container_width=True):
            st.session_state.page = "Survey-Demographics"
            st.rerun()


# ==================================================
# SURVEY – DEMOGRAPHICS  (Step 1 of 3)
# ==================================================
elif st.session_state.page == "Survey-Demographics":

    st.markdown('<p class="progress-label">Step 1 of 3 — Basic Information</p>', unsafe_allow_html=True)
    st.progress(0.33)
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.header("Basic Information")

    age    = st.selectbox("Q1. Select your age group",  ["18–25", "26–35", "36–50", "50+"], index=None)
    gender = st.selectbox("Q2. Select your gender", ["Female", "Male", "Prefer not to say"], index=None)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    if st.button("Next →", key="demo_next"):
        if age and gender:
            st.session_state.responses["demographics"] = {"Q1": age, "Q2": gender}
            st.session_state.page = "Survey-Bias"
            st.rerun()
        else:
            st.warning("Please answer both questions.")


# ==================================================
# SURVEY – BIAS  (Step 2 of 3)
# ==================================================
elif st.session_state.page == "Survey-Bias":

    st.markdown('<p class="progress-label">Step 2 of 3 — Investment Decision Scenarios</p>', unsafe_allow_html=True)
    st.progress(0.66)
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.header("Investment Decision Scenarios")

    def ask_bias(q, text, opts):
        st.session_state.responses["bias"][q] = st.radio(text, opts, index=None, key=q)

    ask_bias("Q3",  "When new information contradicts your investment thesis, you usually:",
        ["A. Assume it is temporary noise", "B. Wait for further confirmation",
         "C. Adjust expectations slightly", "D. Re-examine the entire thesis", "E. Exit or reduce exposure"])
    ask_bias("Q4",  "You bought a stock at ₹1,500; it now trades at ₹1,000. Which thought best reflects your reaction?",
        ["A. It should eventually return to ₹1,500", "B. ₹1,500 remains a key reference for my decision",
         "C. Past prices matter less than future performance", "D. The fall itself could indicate opportunity",
         "E. Price history alone should not guide decisions"])
    ask_bias("Q5",  "When deciding whether to sell an investment, you rely most on:",
        ["A. The price you originally paid", "B. The asset's previous highest price",
         "C. Current valuation and fundamentals", "D. Recent market sentiment and news",
         "E. Long-term expected returns"])
    ask_bias("Q6",  "After a stock performs very well over the last few months, you believe:",
        ["A. The trend will continue", "B. Momentum matters more than history",
         "C. Both trend and history matter", "D. Long-term data is more reliable",
         "E. Short-term movements are irrelevant"])
    ask_bias("Q7",  "Which presentation makes you more comfortable investing?",
        ["A. \"90% success rate\"", "B. \"Only 10% failure rate\"", "C. Both equally",
         "D. Absolute return numbers", "E. Long-term historical averages"])
    ask_bias("Q8",  "After repeated news about market crashes, you:",
        ["A. Feel investing is riskier", "B. Reduce exposure temporarily",
         "C. Re-check historical data", "D. Proceed cautiously", "E. Stick strictly to long-term plans"])
    ask_bias("Q9",  "Which situation feels most uncomfortable to you as an investor?",
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
    back_col, next_col, _ = st.columns([1, 1, 3])
    with back_col:
        st.markdown('<div class="ghost-btn">', unsafe_allow_html=True)
        if st.button("← Back", key="bias_back"):
            st.session_state.page = "Survey-Demographics"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with next_col:
        if st.button("Next →", key="bias_next"):
            if all(st.session_state.responses["bias"].get(f"Q{i}") for i in range(3, 15)):
                st.session_state.page = "Survey-Risk"
                st.rerun()
            else:
                st.warning("Please answer all questions before continuing.")


# ==================================================
# SURVEY – RISK  (Step 3 of 3)
# ==================================================
elif st.session_state.page == "Survey-Risk":

    st.markdown('<p class="progress-label">Step 3 of 3 — Personal Finance Preferences</p>', unsafe_allow_html=True)
    st.progress(1.0)
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
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

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    back_col, submit_col, _ = st.columns([1, 1, 3])
    with back_col:
        st.markdown('<div class="ghost-btn">', unsafe_allow_html=True)
        if st.button("← Back", key="risk_back"):
            st.session_state.page = "Survey-Bias"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with submit_col:
        if st.button("Submit Survey", key="risk_submit"):
            responses_numeric = {}
            for q, ans in st.session_state.responses["bias"].items():
                responses_numeric[q] = 6 - (["A","B","C","D","E"].index(ans[0]) + 1)
            for q, ans in st.session_state.responses["risk"].items():
                responses_numeric[q] = ["A","B","C","D","E"].index(ans[0]) + 1
            st.session_state.analysis_result = generate_full_survey_analysis(responses_numeric)
            st.session_state.survey_completed = True
            st.session_state.page = "Results"
            st.rerun()


# ==================================================
# RESULTS
# ==================================================
elif st.session_state.page == "Results":

    st.header("Results")

    has_robo   = st.session_state.robo_result is not None
    has_survey = st.session_state.survey_completed

    if not has_robo and not has_survey:
        st.info("No analysis completed yet. Use Quick Analysis or take the Manual Assessment.")
        c1, c2, _ = st.columns([1, 1, 2])
        with c1:
            if st.button("Quick Analysis", key="res_robo"):
                st.session_state.page = "RoboAdvisor"
                st.rerun()
        with c2:
            if st.button("Start Assessment", key="res_survey"):
                st.session_state.page = "Survey-Demographics"
                st.rerun()

    # COMBINED SUMMARY
    if has_robo and has_survey:
        robo     = st.session_state.robo_result
        analysis = st.session_state.analysis_result
        bfs_sum  = analysis["behavioral_bias_analysis"]["bfs_summary"]
        risk_sum = analysis["risk_appetite_analysis"]

        st.markdown('<div class="summary-card"><p style="font-family:\'Instrument Serif\',serif;font-size:1.15rem;color:#1a1a18;margin:0 0 16px;">Your Investment Behaviour Summary</p></div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Dominant Bias", robo["bias"])
        with c2:
            st.metric("BFS Score", f"{bfs_sum['bfs_score']} / 60", bfs_sum["category"])
        with c3:
            st.metric("Risk Profile", risk_sum["category"], f"{risk_sum['average_score']:.2f} / 5")
        st.divider()

    # ROBO RESULTS
    if has_robo:
        robo = st.session_state.robo_result
        st.markdown("<span class='results-title'>Robo-Advisor Insight</span>", unsafe_allow_html=True)
        st.write(f"**Age Group:** {robo['age']}  |  **Gender:** {robo['gender']}")
        st.write(
            f"Based on behavioural patterns in the survey data, investors in this demographic "
            f"most commonly exhibit **{robo['bias']}**."
        )

        if robo["sector"] is None:
            st.warning("Insufficient sector data for this demographic. Try a different age group.")
        else:
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Most Preferred Sector", robo["sector"])
            with col_b:
                st.metric("ML Predicted Sector", robo["ml_sector"])
            st.caption(f"Least preferred sector for this demographic: **{robo['least_sector']}**")

            st.markdown("<p style='font-size:13px;font-weight:500;color:#1a1a18;margin:20px 0 8px;'>Average Sector Allocation</p>", unsafe_allow_html=True)
            sector_data = robo["sector_avg"]
            fig_sector  = go.Figure(go.Bar(
                x=list(sector_data.index),
                y=list(sector_data.values),
                marker=dict(color=list(sector_data.values),
                            colorscale=[[0,"#d4c4a0"],[1,"#c5a35a"]], showscale=False),
                text=[f"{v:.1f}%" for v in sector_data.values],
                textposition="outside",
                textfont=dict(color="#1a1a18", size=10)
            ))
            fig_sector.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#1a1a18", family="DM Sans"),
                xaxis=dict(tickangle=-35, gridcolor="#e0ddd7", tickfont=dict(size=11, color="#6b6860")),
                yaxis=dict(gridcolor="#e0ddd7", title="Avg Allocation (%)", tickfont=dict(color="#6b6860")),
                margin=dict(t=20, b=80, l=40, r=20), height=340
            )
            st.plotly_chart(fig_sector, use_container_width=True)

        st.divider()

    # SURVEY RESULTS
    if has_survey:
        analysis     = st.session_state.analysis_result
        bfs          = analysis["behavioral_bias_analysis"]["bfs_summary"]
        bias_profile = analysis["behavioral_bias_analysis"]["bias_profile"]
        risk         = analysis["risk_appetite_analysis"]

        st.markdown("<span class='results-title'>Behavioural Finance Score (BFS)</span>", unsafe_allow_html=True)
        st.metric("BFS", f"{bfs['bfs_score']} / {bfs['max_score']}", bfs["category"])
        st.caption("Calculated out of 60 across 12 behavioural biases. Higher = greater susceptibility.")

        st.markdown("<p style='font-size:13px;font-weight:500;color:#1a1a18;margin:24px 0 8px;'>Bias Intensity Profile</p>", unsafe_allow_html=True)

        bias_names  = list(bias_profile.keys())
        bias_scores = [bias_profile[b]["score"] for b in bias_names]
        bias_levels = [bias_profile[b]["level"] for b in bias_names]
        color_map   = {"High": "#c0392b", "Moderate": "#c5a35a", "Low": "#7aab8a"}
        bar_colors  = [color_map.get(lvl, "#9a9690") for lvl in bias_levels]

        fig_bias = go.Figure(go.Bar(
            x=bias_scores, y=bias_names, orientation="h",
            marker=dict(color=bar_colors),
            text=[f"{s:.2f} — {l}" for s, l in zip(bias_scores, bias_levels)],
            textposition="outside",
            textfont=dict(color="#1a1a18", size=11)
        ))
        fig_bias.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#1a1a18", family="DM Sans"),
            xaxis=dict(range=[0,1.3], gridcolor="#e0ddd7", title="Intensity (0–1)", tickfont=dict(color="#6b6860")),
            yaxis=dict(gridcolor="#e0ddd7", tickfont=dict(size=11, color="#1a1a18")),
            margin=dict(t=10, b=30, l=180, r=110), height=400,
            shapes=[
                dict(type="line", x0=0.33, x1=0.33, y0=-0.5, y1=len(bias_names)-0.5,
                     line=dict(color="#c5c0b8", width=1, dash="dot")),
                dict(type="line", x0=0.66, x1=0.66, y0=-0.5, y1=len(bias_names)-0.5,
                     line=dict(color="#c5c0b8", width=1, dash="dot")),
            ]
        )
        st.plotly_chart(fig_bias, use_container_width=True)
        st.caption("Dotted lines mark Low / Moderate / High thresholds at 0.33 and 0.66.")

        avg_risk = risk["average_score"]
        if avg_risk < 2:
            risk_line = f"A score of **{avg_risk:.2f}/5** indicates a **conservative risk profile** — strong preference for stability and capital protection."
        elif avg_risk < 3.5:
            risk_line = f"A score of **{avg_risk:.2f}/5** indicates a **moderate risk tolerance** — balancing growth with risk control."
        else:
            risk_line = f"A score of **{avg_risk:.2f}/5** indicates a **higher risk tolerance** — comfortable with volatility for long-term gains."

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown("<span class='results-title'>Risk Appetite Assessment</span>", unsafe_allow_html=True)
        st.metric("Average Risk Score", f"{avg_risk:.2f} / 5", risk["category"])
        st.markdown("**Scale:** 1 = Very conservative · 3 = Balanced · 5 = Highly aggressive")
        st.markdown(risk_line)
        st.caption("Reflects behavioural tendencies from your answers — not financial advice.")


# ==================================================
# METHOD
# ==================================================
elif st.session_state.page == "Method":

    st.header("Method")
    st.write("Theoretical foundations and scoring mechanisms used in this assessment.")
    st.divider()

    with st.expander("Behavioural Finance Scoring (BFS)"):
        st.markdown("""
        **BFS** reflects how strongly behavioural biases influence your investment decisions.

        - Calculated **out of 60** across **12 behavioural biases**
        - Each bias contributes equally to the total
        - Higher scores = greater susceptibility · Lower = more disciplined decisions

        **Bias intensity scale (0–1):**
        - 0.00–0.33 → Low influence
        - 0.34–0.66 → Moderate influence
        - 0.67–1.00 → High influence
        """)

    with st.expander("Risk Appetite Scoring (RAS)"):
        st.markdown("""
        The **Risk Appetite Score** captures comfort with uncertainty, evaluated through Q15–Q22.

        - Each response scored **1–5** (1 = conservative, 5 = aggressive)
        - Final score is the average across all eight questions

        **Interpretation:**
        - 1.0–2.0 → Conservative
        - 2.1–3.5 → Moderate / balanced
        - 3.6–5.0 → Aggressive
        """)

    with st.expander("Demographic Bias Inference (Robo-Advisor)"):
        st.markdown("""
        Quick Analysis uses pre-computed average bias scores per age group from
        the primary survey dataset (~135 respondents). The bias with the highest
        average score per age group is identified as dominant.

        Sector allocation is sourced from secondary data covering 220 investor
        profiles across 10 market sectors.
        """)

    with st.expander("Behavioural Bias and Portfolio Integration"):
        st.markdown("""
        Combining bias detection with sector preferences enables context-aware
        insights rather than generic recommendations, supporting more disciplined
        and informed investment decision-making.
        """)


# ==================================================
# BIASES
# ==================================================
elif st.session_state.page == "Biases":

    st.header("Behavioural Biases")
    st.write("Psychological patterns that commonly influence real-world investment behaviour.")
    st.divider()

    def bias_expander(title, desc, example):
        with st.expander(title):
            st.markdown(f"{desc}")
            st.markdown(f"*Example: {example}*")

    bias_expander("Confirmation Bias",
        "Investors seek information confirming existing beliefs while ignoring contradictory evidence. Strengthens incorrect views and delays corrective decisions.",
        "You focus only on positive news about a holding, dismissing poor earnings as \"temporary.\"")
    bias_expander("Anchoring",
        "Over-reliance on an initial reference point (e.g. purchase price) even when new information makes it irrelevant.",
        "You refuse to sell until a stock returns to ₹1,500 — the price you paid — even as fundamentals worsen.")
    bias_expander("Recency Bias",
        "Placing excessive importance on recent events while underestimating long-term trends.",
        "A stock performs well for three months, so you invest heavily assuming the trend continues.")
    bias_expander("Framing Effect",
        "Decisions influenced by how information is presented rather than its actual content.",
        "\"90% success rate\" feels safer than \"10% failure rate\" — even though they're identical.")
    bias_expander("Risk Sensitivity",
        "Emotional overreaction to perceived risk, leading to overly cautious or erratic behaviour.",
        "Repeated crash news causes you to exit equities entirely, despite long-term historical resilience.")
    bias_expander("Loss Aversion",
        "Losses feel more painful than equivalent gains feel rewarding, distorting rational decision-making.",
        "You hold a falling stock to avoid \"booking\" a loss, even when exiting would be rational.")
    bias_expander("Overconfidence",
        "Overestimating one's ability to predict markets, leading to excessive risk and under-diversification.",
        "After a few wins, you double position sizes without questioning whether luck played a role.")
    bias_expander("Herding",
        "Following the crowd rather than making independent, research-based decisions.",
        "You buy a trending stock purely because everyone around you is investing in it.")
    bias_expander("Disposition Effect",
        "Selling winners too early and holding losers too long to avoid the regret of realised losses.",
        "You sell at a small gain but keep a losing stock for months hoping for a recovery.")
    bias_expander("Status Quo Bias",
        "Preference for keeping existing investments unchanged due to inertia or familiarity.",
        "You haven't reviewed your portfolio in two years simply because changing it feels effortful.")
    bias_expander("Emotional / Overtrading Bias",
        "Letting fear, excitement, or stress drive frequent trades rather than a disciplined strategy.",
        "On a volatile day, you place multiple impulsive trades instead of sticking to your plan.")

    st.divider()


# ==================================================
# ABOUT
# ==================================================
elif st.session_state.page == "About":

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
        <li><strong>Secondary:</strong> Sector-wise allocation data across 220 investor profiles and 10 market sectors</li>
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
