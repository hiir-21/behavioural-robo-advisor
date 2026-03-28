import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from survey_logic import generate_full_survey_analysis
from sector_analysis import sector_analysis
from ml_model import predict_sector
from bias_rules import get_dominant_bias
from portfolio_logic import analyse_portfolio, validate_upload, REQUIRED_COLS

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
if "portfolio_result" not in st.session_state:
    st.session_state.portfolio_result = None

# --------------------------------------------------
# GLOBAL STYLES
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #f5f3ef !important;
    font-family: 'DM Sans', sans-serif !important;
    color: #1a1a18 !important;
}
[data-testid="stHeader"]  { background-color: #f5f3ef !important; }
[data-testid="stSidebar"] { background-color: #efecea !important; }
.block-container {
    padding-top: 0 !important;
    padding-bottom: 2rem !important;
    max-width: 860px !important;
}
#MainMenu, footer, header { visibility: hidden; }

/* ── TABS ── */
[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 1px solid #e0ddd7 !important;
    gap: 0 !important;
    background: transparent !important;
    padding-left: 200px !important;
}
[data-testid="stTabs"] button[role="tab"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 400 !important;
    color: #9a9690 !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
    padding: 10px 14px !important;
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
[data-testid="stTabs"] [role="tablist"]::after,
[data-testid="stTabs"] [role="tablist"] > div:last-child {
    background-color: #1a1a18 !important;
}
[data-testid="stTabs"] [data-testid="stTabContent"] {
    padding-top: 28px !important;
}

/* ── BUTTONS ── */
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
    border: 1px solid #d4d0c9 !important;
}
.ghost-btn .stButton > button:hover {
    background: #1a1a18 !important;
    color: #f5f3ef !important;
    border-color: #1a1a18 !important;
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
[data-testid="stSelectbox"] > div > div > div { color: #1a1a18 !important; }
[data-baseweb="popover"], [data-baseweb="popover"] *,
[data-baseweb="menu"], [data-baseweb="menu"] *,
ul[role="listbox"], ul[role="listbox"] li {
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

/* ── TEXT / LABELS ── */
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
[data-testid="stMetricLabel"] {
    color: #6b6860 !important; font-size: 11px !important;
    letter-spacing: 0.04em !important; text-transform: uppercase !important;
}
[data-testid="stMetricValue"] { font-family: 'Instrument Serif', serif !important; color: #1a1a18 !important; }
[data-testid="stMetricDelta"] { font-size: 11px !important; }

/* ── EXPANDER ── */
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p { color: #1a1a18 !important; font-weight: 500 !important; }
[data-testid="stExpander"] { background: #f5f3ef !important; }
[data-testid="stExpander"] > div,
[data-testid="stExpander"] > div > div { background: #f5f3ef !important; }
details { background: #f5f3ef !important; }
details > div, details > div * { background-color: #f5f3ef !important; color: #1a1a18 !important; }
.streamlit-expanderContent,
.streamlit-expanderContent * { background-color: #f5f3ef !important; color: #1a1a18 !important; }

/* ── DOWNLOAD BUTTON ── */
[data-testid="stDownloadButton"] button {
    background: #1a1a18 !important;
    color: #f5f3ef !important;
    border: 1px solid #1a1a18 !important;
    border-radius: 0 !important;
}
[data-testid="stDownloadButton"] button:hover { background: #2f2f2c !important; }
[data-testid="stDownloadButton"] button p,
[data-testid="stDownloadButton"] button span { color: #f5f3ef !important; }

/* ── FILE UPLOADER — dashed gold border ── */
[data-testid="stFileUploader"] button {
    background: #1a1a18 !important;
    color: #f5f3ef !important;
    border: 1px solid #1a1a18 !important;
}
[data-testid="stFileUploader"] button * { color: #f5f3ef !important; }
[data-testid="stFileUploader"] section {
    background: #efecea !important;
    border: 1.5px dashed #c5a35a !important;
    border-radius: 0 !important;
}
[data-testid="stFileUploader"] section p,
[data-testid="stFileUploader"] section span,
[data-testid="stFileUploader"] section small { color: #1a1a18 !important; }
[data-testid="stFileUploaderFile"] * { color: #1a1a18 !important; background: transparent !important; }

/* ── PROGRESS ── */
[data-testid="stProgress"] > div > div { background-color: #c5a35a !important; }
[data-testid="stProgress"] { background: #e0ddd7 !important; border-radius: 0 !important; }

/* ── DIVIDER ── */
hr { border-color: #e0ddd7 !important; }

/* ── SHARED LAYOUT CLASSES ── */
.card {
    background: #efecea; border: 1px solid #e0ddd7;
    border-radius: 0; padding: 28px 32px; margin-top: 16px;
}
.section-header {
    display: flex; align-items: baseline; justify-content: space-between;
    border-bottom: 1px solid #e0ddd7; padding-bottom: 10px; margin-bottom: 16px;
}
.section-label {
    font-size: 11px; font-weight: 500; letter-spacing: 0.1em;
    text-transform: uppercase; color: #9a9690;
}
.section-num { font-family: 'Instrument Serif', serif; font-size: 13px; color: #c5a35a; }
.progress-label {
    font-size: 11px; color: #9a9690; margin-bottom: 6px;
    letter-spacing: 0.05em; text-transform: uppercase;
}

/* ── HOME ── */
.bra-eyebrow {
    display: inline-flex; align-items: center; gap: 8px;
    font-size: 10px; font-weight: 500; letter-spacing: 0.1em;
    text-transform: uppercase; color: #9a9690; margin-bottom: 20px;
}
.bra-eyebrow-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #c5a35a; display: inline-block; flex-shrink: 0;
}
.bra-h1 {
    font-family: 'Instrument Serif', serif !important;
    font-size: 52px !important; font-weight: 400 !important;
    line-height: 1.08 !important; letter-spacing: -0.025em !important;
    color: #1a1a18 !important; margin-bottom: 18px !important;
}
.bra-h1 em { font-style: italic; color: #c5a35a; }
.bra-hero-sub {
    font-size: 15px; font-weight: 300; color: #6b6860;
    line-height: 1.7; max-width: 520px; margin-bottom: 6px;
}
.bra-stat-strip {
    border-top: 1px solid #e0ddd7; border-bottom: 1px solid #e0ddd7;
    background: #efecea; display: flex; margin: 28px 0 0; overflow-x: auto;
}
.bra-stat-item {
    padding: 16px 32px 16px 0; display: flex; flex-direction: column;
    gap: 3px; flex-shrink: 0; border-right: 1px solid #e0ddd7; margin-right: 32px;
}
.bra-stat-item:last-child { border-right: none; margin-right: 0; }
.bra-stat-num { font-family: 'Instrument Serif', serif; font-size: 26px; color: #1a1a18; line-height: 1; }
.bra-stat-label { font-size: 10px; color: #9a9690; letter-spacing: 0.06em; text-transform: uppercase; margin-top: 3px; }
.bra-ticker-wrap {
    overflow: hidden; border-top: 1px solid #e0ddd7; border-bottom: 1px solid #e0ddd7;
    background: #efecea; padding: 9px 0; margin: 28px 0 0;
}
.bra-ticker { display: flex; white-space: nowrap; animation: bra-tick 26s linear infinite; }
.bra-ticker-item {
    display: inline-flex; align-items: center; gap: 8px; font-size: 10px;
    letter-spacing: 0.07em; text-transform: uppercase; color: #9a9690;
    padding: 0 22px; border-right: 1px solid #d4d0c9; flex-shrink: 0;
}
.bra-ticker-item span { color: #c5a35a; font-weight: 500; }
@keyframes bra-tick { from { transform: translateX(0); } to { transform: translateX(-50%); } }
.bra-cards {
    display: grid; grid-template-columns: 1fr 1fr; gap: 1px;
    background: #e0ddd7; border: 1px solid #e0ddd7; margin-bottom: 2px;
}
.bra-card { background: #f5f3ef; padding: 24px 22px; transition: background 0.15s; }
.bra-card:hover { background: #efecea; }
.bra-card-icon {
    width: 28px; height: 28px; border: 1px solid #d4d0c9;
    display: flex; align-items: center; justify-content: center;
    margin-bottom: 14px; font-size: 12px; color: #c5a35a;
}
.bra-card-title { font-size: 13px; font-weight: 500; color: #1a1a18; margin-bottom: 6px; }
.bra-card-desc { font-size: 12px; font-weight: 300; color: #6b6860; line-height: 1.65; }
.bra-steps {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px;
    background: #e0ddd7; border: 1px solid #e0ddd7; margin-bottom: 36px;
}
.bra-step { background: #f5f3ef; padding: 22px 20px; }
.bra-step-num { font-family: 'Instrument Serif', serif; font-size: 30px; color: #d4d0c9; line-height: 1; margin-bottom: 10px; }
.bra-step-title { font-size: 13px; font-weight: 500; color: #1a1a18; margin-bottom: 5px; }
.bra-step-desc { font-size: 12px; font-weight: 300; color: #6b6860; line-height: 1.6; }
.bra-footer-note {
    font-size: 11px; color: #9a9690; margin-top: 36px;
    padding-top: 14px; border-top: 1px solid #e0ddd7;
}

/* ── QUICK ANALYSIS WIDGET ── */
.qa-widget-header {
    background: #1a1a18; padding: 11px 18px;
    display: flex; justify-content: space-between; align-items: center;
    border: 1px solid #1a1a18;
}
.qa-widget-title { font-family: 'Instrument Serif', serif; font-size: 15px; color: #f5f3ef; }
.qa-widget-sub { font-size: 10px; color: #9a9690; letter-spacing: 0.04em; }
.qa-field-label {
    font-size: 10px; color: #9a9690; letter-spacing: 0.06em;
    text-transform: uppercase; margin-bottom: 4px;
}
.qa-hint {
    font-size: 11px; color: #9a9690; padding: 7px 18px;
    background: #efecea; border: 1px solid #1a1a18; border-top: none;
}
.qa-result-strip {
    border-left: 3px solid #c5a35a; padding: 12px 18px;
    background: #efecea; margin-top: 12px;
}
.qa-result-meta { font-size: 10px; color: #9a9690; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 5px; }
.qa-result-body { font-size: 13px; color: #1a1a18; }

/* ── SURVEY ── */
.survey-q-label {
    font-size: 10px; font-weight: 500; color: #c5a35a;
    letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 4px;
}
.survey-divider { border-top: 1px solid #e0ddd7; margin: 20px 0 16px; }

/* ── RESULTS — BFS block ── */
.bfs-block {
    background: #1a1a18; padding: 24px 22px;
    display: flex; flex-direction: column; justify-content: center;
}
.bfs-score-num { font-family: 'Instrument Serif', serif; font-size: 56px; color: #f5f3ef; line-height: 1; }
.bfs-score-denom { font-size: 18px; color: #6b6860; margin-left: 4px; }
.bfs-score-label { font-size: 10px; color: #9a9690; letter-spacing: 0.06em; text-transform: uppercase; margin-top: 6px; }
.bfs-category { font-size: 11px; color: #c5a35a; margin-top: 10px; letter-spacing: 0.04em; font-weight: 500; }

/* ── RESULTS — bias bars ── */
.bias-bar-row { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.bias-bar-name { font-size: 11px; color: #1a1a18; width: 148px; flex-shrink: 0; text-align: right; }
.bias-bar-track { flex: 1; height: 5px; background: #e0ddd7; }
.bias-bar-fill { height: 100%; }
.bias-tag { font-size: 9px; padding: 2px 7px; font-weight: 500; flex-shrink: 0; min-width: 32px; text-align: center; letter-spacing: 0.03em; }
.bias-tag-high { background: #fcebeb; color: #a32d2d; }
.bias-tag-mod  { background: #faeeda; color: #854f0b; }
.bias-tag-low  { background: #eaf3de; color: #3b6d11; }

/* ── RESULTS — risk row ── */
.risk-score-box {
    background: #efecea; border: 1px solid #e0ddd7; padding: 16px 18px;
}
.risk-interp-box {
    background: #efecea; border: 1px solid #e0ddd7; padding: 16px 18px;
    font-size: 13px; color: #6b6860; line-height: 1.65;
}

/* ── PORTFOLIO — holdings table ── */
.portfolio-table { width: 100%; border-collapse: collapse; font-size: 12px; }
.portfolio-table th {
    text-align: left; padding: 8px 10px;
    border-bottom: 1.5px solid #1a1a18; color: #1a1a18;
    font-size: 11px; font-weight: 500; letter-spacing: 0.02em; white-space: nowrap;
}
.portfolio-table td { padding: 9px 10px; border-bottom: 1px solid #e0ddd7; color: #1a1a18; }
.portfolio-table tr:hover td { background: #efecea; }
.p-badge { padding: 2px 8px; font-size: 10px; font-weight: 500; letter-spacing: 0.02em; }
.p-badge-profit { background: #eaf3de; color: #3b6d11; }
.p-badge-loss   { background: #fcebeb; color: #a32d2d; }
.p-badge-flat   { background: #f5f3ef; color: #6b6860; border: 1px solid #e0ddd7; }

/* ── PORTFOLIO — bias insight card ── */
.insight-card {
    border: 1px solid #e0ddd7; border-left: 4px solid #c5a35a;
    padding: 20px 24px; background: #f5f3ef; margin-top: 16px;
}
.insight-card.triggered { border-left-color: #a32d2d; }
.insight-tag { font-size: 10px; color: #9a9690; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 8px; }
.insight-title { font-family: 'Instrument Serif', serif; font-size: 1.15rem; color: #1a1a18; margin-bottom: 8px; }
.insight-body { font-size: 13px; color: #1a1a18; line-height: 1.65; margin-bottom: 10px; }
.insight-action { font-size: 12px; color: #6b6860; border-top: 1px solid #e0ddd7; padding-top: 10px; }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOGO
# --------------------------------------------------
st.markdown("""
<style>
.bra-inline-logo {
    font-family: 'Instrument Serif', serif;
    font-size: 16px; color: #1a1a18; letter-spacing: -0.01em;
    position: absolute; top: 0; left: 0; padding: 12px 0 0 0;
    pointer-events: none; white-space: nowrap; z-index: 10;
}
.bra-inline-logo span { color: #c5a35a; }
</style>
<div class="bra-inline-logo">Behavioural<span>.</span>Advisor</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# TABS
# --------------------------------------------------
tab_home, tab_manual, tab_results, tab_portfolio, tab_method, tab_biases, tab_about = st.tabs(
    ["Home", "Manual Assessment", "Results", "Portfolio", "Method", "Biases", "About"]
)


# ══════════════════════════════════════════════════
# TAB 1 — HOME + QUICK ANALYSIS
# ══════════════════════════════════════════════════
with tab_home:

    st.markdown("""
    <div class="bra-eyebrow">
        <span class="bra-eyebrow-dot"></span>
        Behavioural Finance &middot; India-focused
    </div>
    <p class="bra-h1">Invest smarter.<br>Understand your <em>biases</em> first.</p>
    <p class="bra-hero-sub">
        Identify the psychological patterns shaping your financial decisions &mdash;
        backed by behavioural finance research and demographic investor data.
    </p>
    """, unsafe_allow_html=True)

    # Quick Analysis dark-header widget
    st.markdown("""
    <div class="qa-widget-header">
        <div class="qa-widget-title">Quick Analysis</div>
        <div class="qa-widget-sub">Instant demographic insight &mdash; no survey required</div>
    </div>
    """, unsafe_allow_html=True)

    qa_c1, qa_c2, qa_c3 = st.columns([2, 1.5, 1])
    with qa_c1:
        st.markdown('<p class="qa-field-label">Age group</p>', unsafe_allow_html=True)
        qa_age = st.selectbox("Age", ["Choose", "18-25 years", "26-40 years", "41-55 years", "56-70 years", "70+ years"],
                              key="qa_age", label_visibility="collapsed")
    with qa_c2:
        st.markdown('<p class="qa-field-label">Gender</p>', unsafe_allow_html=True)
        qa_gender = st.selectbox("Gender", ["Choose", "Female", "Male"],
                                 key="qa_gender", label_visibility="collapsed")
    with qa_c3:
        st.markdown('<p style="font-size:10px;color:transparent;margin-bottom:4px;">.</p>', unsafe_allow_html=True)
        qa_run = st.button("Analyse \u2192", key="qa_run")

    st.markdown("""
    <div class="qa-hint">
        Or use the <strong style="color:#1a1a18;">Manual Assessment</strong> tab for a full personal bias profile and BFS score.
    </div>
    """, unsafe_allow_html=True)

    if qa_run:
        if qa_age == "Choose" or qa_gender == "Choose":
            st.warning("Please select both age group and gender.")
        else:
            with st.spinner("Analysing demographic patterns..."):
                most_sector, least_sector, sector_avg = sector_analysis(qa_age, qa_gender)
                ml_sector   = predict_sector(qa_age, qa_gender)
                bias_result = get_dominant_bias(qa_age, qa_gender)
                bias        = bias_result.get("dominant", "Insufficient data")
            st.session_state.robo_result = {
                "age": qa_age, "gender": qa_gender, "bias": bias,
                "sector": most_sector, "least_sector": least_sector,
                "ml_sector": ml_sector, "sector_avg": sector_avg
            }
            st.success("Analysis complete \u2014 view full results in the Results tab.")

    if st.session_state.robo_result:
        r = st.session_state.robo_result
        st.markdown(f"""
        <div class="qa-result-strip">
            <div class="qa-result-meta">Last analysis &mdash; {r['age']} &middot; {r['gender']}</div>
            <div class="qa-result-body">Dominant bias: <strong>{r['bias']}</strong> &nbsp;&middot;&nbsp; Top sector: <strong>{r['sector'] or 'N/A'}</strong></div>
        </div>
        """, unsafe_allow_html=True)

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
        <div class="bra-ticker-item">Confirmation Bias <span>&rsaquo;</span></div>
        <div class="bra-ticker-item">Loss Aversion <span>&rsaquo;</span></div>
        <div class="bra-ticker-item">Anchoring <span>&rsaquo;</span></div>
        <div class="bra-ticker-item">Herding <span>&rsaquo;</span></div>
        <div class="bra-ticker-item">Overconfidence <span>&rsaquo;</span></div>
        <div class="bra-ticker-item">Recency Bias <span>&rsaquo;</span></div>
        <div class="bra-ticker-item">Framing Effect <span>&rsaquo;</span></div>
        <div class="bra-ticker-item">Disposition Effect <span>&rsaquo;</span></div>
        <div class="bra-ticker-item">Status Quo Bias <span>&rsaquo;</span></div>
        <div class="bra-ticker-item">Risk Sensitivity <span>&rsaquo;</span></div>
        <div class="bra-ticker-item">Overtrading Bias <span>&rsaquo;</span></div>
        <div class="bra-ticker-item">Confirmation Bias <span>&rsaquo;</span></div>
        <div class="bra-ticker-item">Loss Aversion <span>&rsaquo;</span></div>
        <div class="bra-ticker-item">Anchoring <span>&rsaquo;</span></div>
        <div class="bra-ticker-item">Herding <span>&rsaquo;</span></div>
        <div class="bra-ticker-item">Overconfidence <span>&rsaquo;</span></div>
        <div class="bra-ticker-item">Recency Bias <span>&rsaquo;</span></div>
        <div class="bra-ticker-item">Framing Effect <span>&rsaquo;</span></div>
        <div class="bra-ticker-item">Disposition Effect <span>&rsaquo;</span></div>
        <div class="bra-ticker-item">Status Quo Bias <span>&rsaquo;</span></div>
        <div class="bra-ticker-item">Risk Sensitivity <span>&rsaquo;</span></div>
        <div class="bra-ticker-item">Overtrading Bias <span>&rsaquo;</span></div>
      </div>
    </div>
    <div class="section-header" style="margin-top:36px;">
        <div class="section-label">What you get</div>
        <div class="section-num">01</div>
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
            <div class="bra-card-desc">Visualise each of 11 biases &mdash; rated Low, Moderate, or High &mdash; based on your real scenario responses.</div>
        </div>
        <div class="bra-card">
            <div class="bra-card-icon">&#9672;</div>
            <div class="bra-card-title">Risk Appetite Classification</div>
            <div class="bra-card-desc">Understand whether your financial temperament is conservative, moderate, or aggressive &mdash; and why.</div>
        </div>
        <div class="bra-card">
            <div class="bra-card-icon">&#9677;</div>
            <div class="bra-card-title">Demographic Sector Insights</div>
            <div class="bra-card-desc">See how investors in your age group allocate across sectors &mdash; powered by real survey data.</div>
        </div>
    </div>
    <div class="section-header" style="margin-top:32px;">
        <div class="section-label">How it works</div>
        <div class="section-num">02</div>
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
            <div class="bra-step-desc">22 carefully designed questions test your real decision-making instincts &mdash; not what you think you should do.</div>
        </div>
        <div class="bra-step">
            <div class="bra-step-num">03</div>
            <div class="bra-step-title">Get your results</div>
            <div class="bra-step-desc">Receive a bias profile, BFS score, risk classification, and sector allocation &mdash; all in one dashboard.</div>
        </div>
    </div>
    <div class="bra-footer-note">Academic project &middot; Not financial advice &middot; For research purposes only</div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════
# TAB 2 — MANUAL ASSESSMENT
# ══════════════════════════════════════════════════
with tab_manual:

    if st.session_state.survey_completed:
        st.markdown("""
        <div style="border-left:3px solid #7aab8a;padding:12px 20px;background:#efecea;margin-bottom:20px;font-size:13px;color:#1a1a18;">
            Manual Assessment already completed. Your results are in the <strong>Results</strong> tab.
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

        # ── STEP 1 ──
        if step == "demographics":
            st.markdown('<p class="progress-label">Step 1 of 3 &mdash; Basic Information</p>', unsafe_allow_html=True)
            st.progress(0.33)
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            st.header("Basic Information")
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

            st.markdown('<p class="survey-q-label">Q1 &mdash; Age group</p>', unsafe_allow_html=True)
            s_age = st.selectbox("Age group", ["18\u201325", "26\u201335", "36\u201350", "50+"], index=None, key="s_age", label_visibility="collapsed")
            st.markdown('<div class="survey-divider"></div>', unsafe_allow_html=True)

            st.markdown('<p class="survey-q-label">Q2 &mdash; Gender</p>', unsafe_allow_html=True)
            s_gender = st.selectbox("Gender", ["Female", "Male", "Prefer not to say"], index=None, key="s_gender", label_visibility="collapsed")

            st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
            if st.button("Next \u2192", key="demo_next"):
                if s_age and s_gender:
                    st.session_state.responses["demographics"] = {"Q1": s_age, "Q2": s_gender}
                    st.session_state.survey_step = "bias"
                    st.rerun()
                else:
                    st.warning("Please answer both questions.")

        # ── STEP 2 ──
        elif step == "bias":
            st.markdown('<p class="progress-label">Step 2 of 3 &mdash; Investment Decision Scenarios</p>', unsafe_allow_html=True)
            st.progress(0.66)
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            st.header("Investment Decision Scenarios")
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

            def ask_bias(q, label, text, opts):
                st.markdown(f'<p class="survey-q-label">{label}</p>', unsafe_allow_html=True)
                st.session_state.responses["bias"][q] = st.radio(text, opts, index=None, key=f"b_{q}", label_visibility="collapsed")
                st.markdown('<div class="survey-divider"></div>', unsafe_allow_html=True)

            ask_bias("Q3",  "Q3 \u2014 Confirmation Bias",
                "When new information contradicts your investment thesis, you usually:",
                ["A. Assume it is temporary noise", "B. Wait for further confirmation",
                 "C. Adjust expectations slightly", "D. Re-examine the entire thesis", "E. Exit or reduce exposure"])
            ask_bias("Q4",  "Q4 \u2014 Anchoring",
                "You bought a stock at \u20b91,500; it now trades at \u20b91,000. Which thought best reflects your reaction?",
                ["A. It should eventually return to \u20b91,500", "B. \u20b91,500 remains a key reference for my decision",
                 "C. Past prices matter less than future performance", "D. The fall itself could indicate opportunity",
                 "E. Price history alone should not guide decisions"])
            ask_bias("Q5",  "Q5 \u2014 Anchoring",
                "When deciding whether to sell an investment, you rely most on:",
                ["A. The price you originally paid", "B. The asset\u2019s previous highest price",
                 "C. Current valuation and fundamentals", "D. Recent market sentiment and news",
                 "E. Long-term expected returns"])
            ask_bias("Q6",  "Q6 \u2014 Recency Bias",
                "After a stock performs very well over the last few months, you believe:",
                ["A. The trend will continue", "B. Momentum matters more than history",
                 "C. Both trend and history matter", "D. Long-term data is more reliable",
                 "E. Short-term movements are irrelevant"])
            ask_bias("Q7",  "Q7 \u2014 Framing Effect",
                "Which presentation makes you more comfortable investing?",
                ['A. "90% success rate"', 'B. "Only 10% failure rate"', "C. Both equally",
                 "D. Absolute return numbers", "E. Long-term historical averages"])
            ask_bias("Q8",  "Q8 \u2014 Risk Sensitivity",
                "After repeated news about market crashes, you:",
                ["A. Feel investing is riskier", "B. Reduce exposure temporarily",
                 "C. Re-check historical data", "D. Proceed cautiously", "E. Stick strictly to long-term plans"])
            ask_bias("Q9",  "Q9 \u2014 Loss Aversion",
                "Which situation feels most uncomfortable to you as an investor?",
                ["A. Selling an investment at a loss", "B. Missing out on a potential gain",
                 "C. Making a decision without sufficient information", "D. Being wrong in front of others",
                 "E. Realising a loss even when it improves future outcomes"])
            ask_bias("Q10", "Q10 \u2014 Overconfidence",
                "After a series of profitable trades, you plan your next investment by:",
                ["A. Increasing position size significantly", "B. Using the same strategy with minor tweaks",
                 "C. Keeping position size unchanged", "D. Diversifying to reduce reliance",
                 "E. Reviewing assumptions behind past success"])
            ask_bias("Q11", "Q11 \u2014 Herding",
                "A stock is trending heavily on social media and business news. You:",
                ["A. Buy immediately", "B. Invest a small amount", "C. Track it closely first",
                 "D. Research fundamentals independently", "E. Avoid it due to hype"])
            ask_bias("Q12", "Q12 \u2014 Disposition Effect",
                "You have one stock with large gains and one with losses. You:",
                ["A. Sell the winner to lock profits", "B. Hold the loser hoping for recovery",
                 "C. Sell part of both", "D. Rebalance based on targets", "E. Reassess both on fundamentals"])
            ask_bias("Q13", "Q13 \u2014 Status Quo Bias",
                "You keep an old investment mainly because:",
                ["A. It feels familiar", "B. Changing requires effort",
                 "C. You haven\u2019t reviewed alternatives", "D. There\u2019s no urgent reason",
                 "E. You reassess periodically"])
            ask_bias("Q14", "Q14 \u2014 Overtrading Bias",
                "When markets move sharply in a single day, you tend to:",
                ["A. Trade actively", "B. Adjust positions quickly",
                 "C. Pause and reassess", "D. Stick to preset rules", "E. Avoid reacting"])

            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            bc, nc, _ = st.columns([1, 1, 3])
            with bc:
                st.markdown('<div class="ghost-btn">', unsafe_allow_html=True)
                if st.button("\u2190 Back", key="bias_back"):
                    st.session_state.survey_step = "demographics"
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            with nc:
                if st.button("Next \u2192", key="bias_next"):
                    if all(st.session_state.responses["bias"].get(f"Q{i}") for i in range(3, 15)):
                        st.session_state.survey_step = "risk"
                        st.rerun()
                    else:
                        st.warning("Please answer all questions.")

        # ── STEP 3 ──
        elif step == "risk":
            st.markdown('<p class="progress-label">Step 3 of 3 &mdash; Personal Finance Preferences</p>', unsafe_allow_html=True)
            st.progress(1.0)
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            st.header("Personal Finance Preferences")
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

            def ask_risk(q, label, text, opts):
                st.markdown(f'<p class="survey-q-label">{label}</p>', unsafe_allow_html=True)
                st.session_state.responses["risk"][q] = st.radio(text, opts, index=None, key=f"r_{q}", label_visibility="collapsed")
                st.markdown('<div class="survey-divider"></div>', unsafe_allow_html=True)

            ask_risk("Q15", "Q15 \u2014 Long-Term Wealth Goal",
                "Long-Term Wealth Goal (10\u201315 years) \u2014 You prefer to:",
                ["A. Protect capital even if growth is limited", "B. Earn steady low-volatility returns",
                 "C. Balance growth and safety", "D. Accept volatility for higher growth",
                 "E. Maximise growth despite fluctuations"])
            ask_risk("Q16", "Q16 \u2014 Retirement Horizon",
                "Retirement Horizon (20+ years away) \u2014 Your approach would be:",
                ["A. Preserve savings", "B. Focus on income assets", "C. Mix income and growth",
                 "D. Tilt toward growth early", "E. Aggressively grow capital"])
            ask_risk("Q17", "Q17 \u2014 Medium-Term Goal",
                "Medium-Term Goal (5\u20137 years) \u2014 You would:",
                ["A. Keep funds fully safe", "B. Use mostly low-risk instruments",
                 "C. Combine safety with equity", "D. Use growth assets initially",
                 "E. Invest aggressively"])
            ask_risk("Q18", "Q18 \u2014 Portfolio Decline Reaction",
                "Reaction to a 10\u201315% Portfolio Decline \u2014 You would most likely:",
                ["A. Exit investments", "B. Reduce exposure", "C. Hold and wait",
                 "D. Increase exposure", "E. Rebalance strategically"])
            ask_risk("Q19", "Q19 \u2014 Risk\u2013Return Preference",
                "Risk\u2013Return Preference \u2014 Which best describes you?",
                ["A. Lower risk, lower return", "B. Moderate risk, moderate return",
                 "C. Market-level risk and return", "D. Higher risk for higher return",
                 "E. Maximum return regardless of risk"])
            ask_risk("Q20", "Q20 \u2014 Volatility Attitude",
                "Volatility Attitude \u2014 How do you view market volatility?",
                ["A. Something to avoid", "B. A reason to be cautious",
                 "C. A normal part of investing", "D. A potential opportunity",
                 "E. A source of advantage"])
            ask_risk("Q21", "Q21 \u2014 Income vs Growth",
                "Income vs Growth Orientation \u2014 For your long-term future, you value:",
                ["A. Stable income", "B. Mostly income with some growth",
                 "C. Equal income and growth", "D. Mostly growth",
                 "E. Growth first, income later"])
            ask_risk("Q22", "Q22 \u2014 Time vs Certainty",
                "Time vs Certainty Trade-off \u2014 10 years with low risk, or 6 years with high uncertainty. You choose:",
                ["A. Definitely choose safety", "B. Lean toward safety",
                 "C. Balance both", "D. Prefer the faster route",
                 "E. Strongly prefer speed despite risk"])

            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            bc2, sc, _ = st.columns([1, 1, 3])
            with bc2:
                st.markdown('<div class="ghost-btn">', unsafe_allow_html=True)
                if st.button("\u2190 Back", key="risk_back"):
                    st.session_state.survey_step = "bias"
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            with sc:
                if st.button("Submit Survey", key="risk_submit"):
                    responses_numeric = {}
                    for q, ans in st.session_state.responses["bias"].items():
                        responses_numeric[q] = 6 - (["A", "B", "C", "D", "E"].index(ans[0]) + 1)
                    for q, ans in st.session_state.responses["risk"].items():
                        responses_numeric[q] = ["A", "B", "C", "D", "E"].index(ans[0]) + 1
                    st.session_state.analysis_result = generate_full_survey_analysis(responses_numeric)
                    st.session_state.survey_completed = True
                    st.session_state.survey_step = "demographics"
                    st.success("Assessment complete \u2014 view your results in the Results tab.")
                    st.rerun()


# ══════════════════════════════════════════════════
# TAB 3 — RESULTS
# ══════════════════════════════════════════════════
with tab_results:

    has_robo   = st.session_state.robo_result is not None
    has_survey = st.session_state.survey_completed

    st.header("Results")

    if not has_robo and not has_survey:
        st.markdown("""
        <div style="border:1px solid #e0ddd7;background:#efecea;padding:28px 32px;margin-top:8px;">
            <div style="font-family:'Instrument Serif',serif;font-size:1.2rem;color:#1a1a18;margin-bottom:8px;">No analysis completed yet</div>
            <div style="font-size:13px;color:#6b6860;line-height:1.6;">
                Go to the <strong style="color:#1a1a18;">Home</strong> tab to run a Quick Analysis,
                or use <strong style="color:#1a1a18;">Manual Assessment</strong> for the full survey.
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif has_robo and not has_survey:
        st.markdown("""
        <div style="border-left:3px solid #c5a35a;padding:10px 18px;background:#efecea;margin-bottom:20px;font-size:13px;color:#6b6860;">
            Quick Analysis complete. Switch to <strong style="color:#1a1a18;">Manual Assessment</strong> for a personal BFS score and bias profile.
        </div>
        """, unsafe_allow_html=True)
    elif has_survey and not has_robo:
        st.markdown("""
        <div style="border-left:3px solid #c5a35a;padding:10px 18px;background:#efecea;margin-bottom:20px;font-size:13px;color:#6b6860;">
            Manual Assessment complete. Go to <strong style="color:#1a1a18;">Home</strong> to also run a Quick Analysis for demographic sector insights.
        </div>
        """, unsafe_allow_html=True)

    # Combined summary card
    if has_robo and has_survey:
        robo    = st.session_state.robo_result
        an      = st.session_state.analysis_result
        bfs_sum = an["behavioral_bias_analysis"]["bfs_summary"]
        ras     = an["risk_appetite_analysis"]
        st.markdown("""
        <div style="background:#efecea;border:1px solid #c5a35a;border-left:3px solid #c5a35a;padding:14px 20px;margin-bottom:18px;">
            <div style="font-family:'Instrument Serif',serif;font-size:1.05rem;color:#1a1a18;">Your Investment Behaviour Summary</div>
        </div>
        """, unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("Dominant Bias", robo["bias"])
        with c2: st.metric("BFS Score", f"{bfs_sum['bfs_score']} / 60", bfs_sum["category"])
        with c3: st.metric("Risk Profile", ras["category"], f"{ras['average_score']:.2f} / 5")
        st.divider()

    # Robo results
    if has_robo:
        robo = st.session_state.robo_result
        st.markdown("""
        <div class="section-header">
            <div class="section-label">Quick Analysis &mdash; demographic insight</div>
            <div class="section-num">01</div>
        </div>
        """, unsafe_allow_html=True)

        r1, r2, r3 = st.columns(3)
        with r1:
            st.markdown(f"""
            <div style="background:#efecea;border:1px solid #e0ddd7;padding:14px 16px;">
                <div style="font-size:10px;color:#9a9690;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:6px;">Age &amp; Gender</div>
                <div style="font-size:13px;font-weight:500;color:#1a1a18;">{robo['age']}</div>
                <div style="font-size:12px;color:#6b6860;margin-top:2px;">{robo['gender']}</div>
            </div>
            """, unsafe_allow_html=True)
        with r2:
            st.markdown(f"""
            <div style="background:#efecea;border:1px solid #e0ddd7;padding:14px 16px;">
                <div style="font-size:10px;color:#9a9690;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:6px;">Dominant Bias</div>
                <div style="font-size:13px;font-weight:500;color:#1a1a18;">{robo['bias']}</div>
            </div>
            """, unsafe_allow_html=True)
        with r3:
            top_sec = robo['sector'] or 'N/A'
            ml_sec  = robo['ml_sector'] or 'N/A'
            least   = robo['least_sector'] or 'N/A'
            st.markdown(f"""
            <div style="background:#efecea;border:1px solid #e0ddd7;padding:14px 16px;">
                <div style="font-size:10px;color:#9a9690;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:6px;">Top Sector</div>
                <div style="font-size:13px;font-weight:500;color:#1a1a18;">{top_sec}</div>
                <div style="font-size:11px;color:#c5a35a;margin-top:3px;">ML: {ml_sec} &middot; Least: {least}</div>
            </div>
            """, unsafe_allow_html=True)

        if robo["sector"] is not None:
            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
            sector_data = robo["sector_avg"]
            fig_s = go.Figure(go.Bar(
                x=list(sector_data.index), y=list(sector_data.values),
                marker=dict(color=list(sector_data.values),
                            colorscale=[[0, "#e8dfc8"], [1, "#c5a35a"]], showscale=False),
                text=[f"{v:.1f}%" for v in sector_data.values],
                textposition="outside", textfont=dict(color="#6b6860", size=10)
            ))
            fig_s.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#1a1a18", family="DM Sans"),
                xaxis=dict(tickangle=-35, gridcolor="#e0ddd7", tickfont=dict(size=11, color="#6b6860")),
                yaxis=dict(gridcolor="#e0ddd7", title="Avg Allocation (%)", tickfont=dict(color="#6b6860")),
                margin=dict(t=20, b=80, l=40, r=20), height=300
            )
            st.plotly_chart(fig_s, use_container_width=True)
        else:
            st.warning("Insufficient sector data for this demographic.")

        if has_survey:
            st.divider()

    # Survey results
    if has_survey:
        an           = st.session_state.analysis_result
        bfs          = an["behavioral_bias_analysis"]["bfs_summary"]
        bias_profile = an["behavioral_bias_analysis"]["bias_profile"]
        risk         = an["risk_appetite_analysis"]

        st.markdown("""
        <div class="section-header">
            <div class="section-label">Manual Assessment &mdash; BFS &amp; bias profile</div>
            <div class="section-num">02</div>
        </div>
        """, unsafe_allow_html=True)

        # BFS dark block alongside inline bias bars
        bfs_col, bars_col = st.columns([1, 2.2])

        with bfs_col:
            st.markdown(f"""
            <div class="bfs-block">
                <div style="font-size:10px;color:#9a9690;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:10px;">Behavioural Finance Score</div>
                <div>
                    <span class="bfs-score-num">{bfs['bfs_score']}</span>
                    <span class="bfs-score-denom">/ {bfs['max_score']}</span>
                </div>
                <div class="bfs-score-label">out of 60 &middot; 12 biases</div>
                <div class="bfs-category">{bfs['category'].upper()}</div>
            </div>
            """, unsafe_allow_html=True)

        with bars_col:
            st.markdown("<div style='font-size:10px;color:#9a9690;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:10px;'>Bias intensity profile</div>", unsafe_allow_html=True)
            sorted_biases = sorted(bias_profile.items(), key=lambda x: x[1]["score"], reverse=True)
            bars_html = ""
            for bias_name, info in sorted_biases:
                score = info["score"]
                level = info["level"]
                pct   = round(score * 100, 1)
                if level == "High":
                    fill_color = "#c0392b"; tag_cls = "bias-tag-high"
                elif level == "Moderate":
                    fill_color = "#c5a35a"; tag_cls = "bias-tag-mod"
                else:
                    fill_color = "#7aab8a"; tag_cls = "bias-tag-low"
                bars_html += f"""
                <div class="bias-bar-row">
                    <div class="bias-bar-name">{bias_name}</div>
                    <div class="bias-bar-track"><div class="bias-bar-fill" style="width:{pct}%;background:{fill_color};"></div></div>
                    <div class="bias-tag {tag_cls}">{level}</div>
                </div>"""
            st.markdown(f'<div>{bars_html}</div>', unsafe_allow_html=True)
            st.markdown("<div style='font-size:10px;color:#9a9690;margin-top:6px;'>Normalised intensity (0&ndash;1 scale) &middot; dotted lines at 0.33 and 0.66</div>", unsafe_allow_html=True)

        # Risk score + interpretation side by side
        avg_risk = risk["average_score"]
        if avg_risk < 2:
            risk_interp = "Prefers stability and capital protection, with limited tolerance for volatility."
        elif avg_risk < 3.5:
            risk_interp = "Willing to accept moderate volatility for balanced growth, with some focus on long-term appreciation."
        else:
            risk_interp = "Comfortable with higher volatility for long-term growth; prioritises capital appreciation over short-term income."

        st.markdown("""
        <div class="section-header" style="margin-top:24px;">
            <div class="section-label">Risk Appetite Assessment</div>
            <div class="section-num">03</div>
        </div>
        """, unsafe_allow_html=True)

        ra_col, ri_col = st.columns([1, 2.2])
        with ra_col:
            st.markdown(f"""
            <div class="risk-score-box">
                <div style="font-size:10px;color:#9a9690;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:8px;">Average score</div>
                <div style="font-family:'Instrument Serif',serif;font-size:38px;color:#1a1a18;line-height:1;">{avg_risk:.2f}</div>
                <div style="font-size:10px;color:#9a9690;margin-top:3px;">out of 5</div>
                <div style="font-size:11px;color:#c5a35a;margin-top:10px;font-weight:500;">{risk['category'].upper()}</div>
            </div>
            """, unsafe_allow_html=True)
        with ri_col:
            st.markdown(f"""
            <div class="risk-interp-box">
                <div style="font-size:10px;color:#9a9690;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:8px;">Interpretation</div>
                <div style="font-size:13px;color:#1a1a18;line-height:1.65;">{risk_interp}</div>
                <div style="font-size:11px;color:#9a9690;margin-top:12px;padding-top:10px;border-top:1px solid #e0ddd7;">
                    Scale: 1 = Very conservative &middot; 3 = Balanced &middot; 5 = Highly aggressive
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.caption("Reflects behavioural tendencies — not financial advice.")


# ══════════════════════════════════════════════════
# TAB 4 — PORTFOLIO ANALYSIS
# ══════════════════════════════════════════════════
with tab_portfolio:

    st.header("Portfolio Analysis")
    st.markdown("<p style='color:#6b6860;font-size:14px;margin-top:-6px;margin-bottom:20px;'>Upload your holdings to get allocation analysis, return metrics, and bias-aware insights.</p>", unsafe_allow_html=True)

    import io
    sample = pd.DataFrame({
        "Stock":               ["Reliance Industries", "Infosys", "HDFC Bank", "TCS", "Tata Motors"],
        "Sector":              ["Energy", "Technology", "Finance", "Technology", "Consumer Goods"],
        "Quantity":            [10, 5, 8, 3, 20],
        "Buy Price (INR)":     [2400, 1500, 1600, 3500, 450],
        "Current Price (INR)": [2800, 1700, 1750, 3800, 520],
    })
    buf = io.BytesIO()
    sample.to_csv(buf, index=False)
    buf.seek(0)
    st.download_button(
        label="Download sample template (CSV)",
        data=buf, file_name="portfolio_template.csv",
        mime="text/csv", key="dl_template"
    )
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Drop your CSV or Excel file here, or click to browse",
        type=["csv", "xlsx"], key="portfolio_upload"
    )

    if uploaded:
        try:
            raw_df = pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_excel(uploaded)
            valid, err = validate_upload(raw_df)
            if not valid:
                st.error(f"File error: {err}")
            else:
                dominant_bias = None
                if st.session_state.robo_result:
                    dominant_bias = st.session_state.robo_result.get("bias")
                if st.session_state.survey_completed and st.session_state.analysis_result:
                    bp = st.session_state.analysis_result["behavioral_bias_analysis"]["bias_profile"]
                    dominant_bias = max(bp, key=lambda b: bp[b]["score"])
                result = analyse_portfolio(raw_df, dominant_bias=dominant_bias)
                st.session_state.portfolio_result = result
        except Exception as e:
            st.error(f"Could not read file: {e}")

    if st.session_state.portfolio_result:
        res  = st.session_state.portfolio_result
        summ = res["summary"]
        div  = res["diversification"]
        sa   = res["sector_alloc"]
        bi   = res["bias_insight"]

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="section-header">
            <div class="section-label">Portfolio Summary</div>
            <div class="section-num">01</div>
        </div>
        """, unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)
        with m1: st.metric("Total Invested",  f"\u20b9{summ['total_invested']:,.0f}")
        with m2: st.metric("Current Value",   f"\u20b9{summ['total_current']:,.0f}",
                           f"{'▲' if summ['total_gain'] >= 0 else '▼'} \u20b9{abs(summ['total_gain']):,.0f}")
        with m3: st.metric("Overall Return",  f"{summ['total_return']:+.2f}%")
        with m4: st.metric("Holdings",        summ["n_holdings"])

        m5, m6, m7 = st.columns(3)
        with m5: st.metric("Best Performer",  summ["best_holding"],  f"{summ['best_return']:+.1f}%")
        with m6: st.metric("Worst Performer", summ["worst_holding"], f"{summ['worst_return']:+.1f}%")
        with m7: st.metric("Diversification", div["level"])

        if res["flags"]:
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            for flag in res["flags"]:
                st.warning(flag)

        st.divider()

        st.markdown("""
        <div class="section-header">
            <div class="section-label">Sector Allocation</div>
            <div class="section-num">02</div>
        </div>
        """, unsafe_allow_html=True)
        fig_sa = go.Figure(go.Bar(
            x=list(sa.index), y=list(sa.values),
            marker=dict(color=list(sa.values), colorscale=[[0, "#e8dfc8"], [1, "#c5a35a"]], showscale=False),
            text=[f"{v:.1f}%" for v in sa.values],
            textposition="outside", textfont=dict(color="#6b6860", size=11)
        ))
        fig_sa.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#1a1a18", family="DM Sans"),
            xaxis=dict(tickangle=-30, gridcolor="#e0ddd7", tickfont=dict(size=11, color="#6b6860")),
            yaxis=dict(gridcolor="#e0ddd7", title="Allocation (%)", tickfont=dict(color="#6b6860")),
            margin=dict(t=20, b=70, l=40, r=20), height=300
        )
        st.plotly_chart(fig_sa, use_container_width=True)

        st.divider()

        st.markdown("""
        <div class="section-header">
            <div class="section-label">Holdings Detail</div>
            <div class="section-num">03</div>
        </div>
        """, unsafe_allow_html=True)
        st.caption("Green = profit · Red = loss · Values in INR")

        holdings  = res["holdings"].copy()
        rows_html = ""
        for _, row in holdings.iterrows():
            ret = row["Return (%)"]
            gl  = row["Gain / Loss (INR)"]
            if ret > 0:
                ret_color = "#2e7d32"; gl_color = "#2e7d32"
                badge = '<span class="p-badge p-badge-profit">▲ PROFIT</span>'
            elif ret < 0:
                ret_color = "#c62828"; gl_color = "#c62828"
                badge = '<span class="p-badge p-badge-loss">▼ LOSS</span>'
            else:
                ret_color = "#6b6860"; gl_color = "#6b6860"
                badge = '<span class="p-badge p-badge-flat">— FLAT</span>'
            rows_html += f"""
            <tr>
                <td style="font-weight:500;">{row['Stock']}</td>
                <td style="color:#6b6860;">{row['Sector']}</td>
                <td style="text-align:right;">{int(row['Quantity'])}</td>
                <td style="text-align:right;">\u20b9{row['Buy Price (INR)']:,.0f}</td>
                <td style="text-align:right;">\u20b9{row['Current Price (INR)']:,.0f}</td>
                <td style="text-align:right;">\u20b9{row['Invested Value (INR)']:,.0f}</td>
                <td style="text-align:right;">\u20b9{row['Current Value (INR)']:,.0f}</td>
                <td style="text-align:right;font-weight:500;color:{gl_color};">\u20b9{gl:+,.0f}</td>
                <td style="text-align:right;font-weight:500;color:{ret_color};">{ret:+.2f}%</td>
                <td style="text-align:center;">{badge}</td>
            </tr>"""

        st.markdown(f"""
        <div style="overflow-x:auto;margin-top:8px;">
        <table class="portfolio-table">
          <thead>
            <tr>
              <th>Stock</th><th>Sector</th><th style="text-align:right;">Qty</th>
              <th style="text-align:right;">Buy</th><th style="text-align:right;">Now</th>
              <th style="text-align:right;">Invested</th><th style="text-align:right;">Value</th>
              <th style="text-align:right;">Gain / Loss</th><th style="text-align:right;">Return</th>
              <th style="text-align:center;">Status</th>
            </tr>
          </thead>
          <tbody>{rows_html}</tbody>
        </table>
        </div>
        """, unsafe_allow_html=True)

        if bi:
            st.markdown("""
            <div class="section-header" style="margin-top:24px;">
                <div class="section-label">Behavioural Insight</div>
                <div class="section-num">04</div>
            </div>
            """, unsafe_allow_html=True)
            triggered_cls = "triggered" if bi["triggered"] else ""
            indicator     = "▲ Pattern detected in your portfolio" if bi["triggered"] else "ℹ Pattern worth being aware of"
            st.markdown(f"""
            <div class="insight-card {triggered_cls}">
                <div class="insight-tag">{indicator}</div>
                <div class="insight-title">{bi['bias']}</div>
                <div class="insight-body">{bi['insight']}</div>
                <div class="insight-action"><strong>Suggested action:</strong> {bi['action']}</div>
            </div>
            """, unsafe_allow_html=True)
            if not (st.session_state.robo_result or st.session_state.survey_completed):
                st.info("Complete the Quick Analysis or Manual Assessment to get a personalised bias-portfolio connection.")

    elif not uploaded:
        st.markdown("""
        <div style="border:1px solid #e0ddd7;background:#efecea;padding:24px 28px;margin-top:4px;">
            <div style="font-family:'Instrument Serif',serif;font-size:1.1rem;color:#1a1a18;margin-bottom:14px;">Expected file format</div>
            <table style="font-size:12px;color:#1a1a18;border-collapse:collapse;width:100%;">
                <tr style="border-bottom:1px solid #e0ddd7;">
                    <th style="text-align:left;padding:6px 12px 6px 0;font-weight:500;">Column</th>
                    <th style="text-align:left;padding:6px 12px;font-weight:500;">Description</th>
                    <th style="text-align:left;padding:6px 0;font-weight:500;">Example</th>
                </tr>
                <tr style="border-bottom:1px solid #e0ddd7;"><td style="padding:6px 12px 6px 0;color:#c5a35a;font-weight:500;">Stock</td><td style="padding:6px 12px;color:#6b6860;">Company name</td><td style="padding:6px 0;color:#6b6860;">Reliance Industries</td></tr>
                <tr style="border-bottom:1px solid #e0ddd7;"><td style="padding:6px 12px 6px 0;color:#c5a35a;font-weight:500;">Sector</td><td style="padding:6px 12px;color:#6b6860;">Market sector</td><td style="padding:6px 0;color:#6b6860;">Energy</td></tr>
                <tr style="border-bottom:1px solid #e0ddd7;"><td style="padding:6px 12px 6px 0;color:#c5a35a;font-weight:500;">Quantity</td><td style="padding:6px 12px;color:#6b6860;">Shares held</td><td style="padding:6px 0;color:#6b6860;">10</td></tr>
                <tr style="border-bottom:1px solid #e0ddd7;"><td style="padding:6px 12px 6px 0;color:#c5a35a;font-weight:500;">Buy Price (INR)</td><td style="padding:6px 12px;color:#6b6860;">Price paid per share</td><td style="padding:6px 0;color:#6b6860;">2400</td></tr>
                <tr><td style="padding:6px 12px 6px 0;color:#c5a35a;font-weight:500;">Current Price (INR)</td><td style="padding:6px 12px;color:#6b6860;">Today's market price</td><td style="padding:6px 0;color:#6b6860;">2800</td></tr>
            </table>
            <div style="font-size:11px;color:#9a9690;margin-top:12px;">Download the sample template above to get started quickly.</div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════
# TAB 5 — METHOD
# ══════════════════════════════════════════════════
with tab_method:
    st.header("Method")
    st.markdown("<p style='color:#6b6860;font-size:14px;margin-top:-6px;margin-bottom:20px;'>Theoretical foundations and scoring mechanisms used in this assessment.</p>", unsafe_allow_html=True)
    st.divider()

    with st.expander("Behavioural Finance Scoring (BFS)"):
        st.markdown("""
        **BFS** reflects how strongly behavioural biases influence investment decisions.

        - Calculated **out of 60** across **12 behavioural biases**
        - Each bias contributes equally · Higher score = greater susceptibility
        - Lower scores suggest more disciplined, emotionally neutral decision-making

        **Bias intensity thresholds (0–1 scale):**
        - 0.00–0.33 → Low · 0.34–0.66 → Moderate · 0.67–1.00 → High

        **BFS categories:**
        - ≤ 28 → Low Bias-Prone · 29–44 → Moderately Bias-Prone · 45+ → Highly Bias-Prone
        """)

    with st.expander("Risk Appetite Scoring (RAS)"):
        st.markdown("""
        Captures comfort with uncertainty and volatility through Q15–Q22.

        - Each response scored **1–5** (A = 1 conservative → E = 5 aggressive)
        - Final score = average across all eight questions

        **Interpretation:**
        - 1.0–2.0 → Conservative · 2.1–3.5 → Moderate · 3.6–5.0 → Aggressive
        """)

    with st.expander("Demographic Bias Inference (Quick Analysis)"):
        st.markdown("""
        Uses pre-computed average bias scores per age group derived from ~135 primary survey respondents.
        The bias with the highest average score is identified as dominant for that demographic.
        Sector allocation data covers 220 investor profiles across 10 market sectors.
        A Decision Tree classifier trained on this data provides an ML-based sector prediction.
        """)

    with st.expander("Behavioural Bias and Portfolio Integration"):
        st.markdown("""
        When a portfolio is uploaded alongside a completed bias assessment, the system links
        the dominant bias to patterns in the actual holdings — such as sector concentration,
        winner/loser holding ratios, or allocation skews. This enables context-aware insights
        rather than generic recommendations, supporting more disciplined decision-making.
        """)


# ══════════════════════════════════════════════════
# TAB 6 — BIASES
# ══════════════════════════════════════════════════
with tab_biases:
    st.header("Behavioural Biases")
    st.markdown("<p style='color:#6b6860;font-size:14px;margin-top:-6px;margin-bottom:20px;'>Psychological patterns that commonly influence real-world investment behaviour.</p>", unsafe_allow_html=True)
    st.divider()

    def bias_card(title, desc, example):
        with st.expander(title):
            st.markdown(desc)
            st.markdown(f"*Example: {example}*")

    bias_card("Confirmation Bias",
        "Seeking information that confirms existing beliefs while ignoring contradictory evidence. Over time, selective attention strengthens confidence in an incorrect view and delays corrective action.",
        "You dismiss poor earnings as \"temporary\" because you believe the company is a great long-term investment.")
    bias_card("Anchoring",
        "Over-reliance on an initial reference point — such as a purchase price or past valuation — even when new information makes it irrelevant.",
        "You refuse to sell until a stock returns to ₹1,500 — the price you paid — even as fundamentals worsen.")
    bias_card("Recency Bias",
        "Placing excessive importance on recent events while underestimating long-term trends. Leads to chasing recent winners or panicking during temporary downturns.",
        "A stock performs well for three months, so you invest heavily assuming the trend will continue.")
    bias_card("Framing Effect",
        "Investment decisions influenced by how information is presented rather than its actual content. Different wording triggers different emotional reactions even when the underlying facts are identical.",
        '"90% success rate" feels safer than "10% failure rate" — even though they describe the same outcome.')
    bias_card("Risk Sensitivity",
        "Emotional overreaction to perceived risk or uncertainty, leading to overly cautious or erratic behaviour driven by fear rather than analysis.",
        "Repeated crash news causes you to exit equities entirely, despite long-term historical resilience.")
    bias_card("Loss Aversion",
        "Losses feel more painful than equivalent gains feel rewarding. Investors focus on avoiding losses rather than maximising overall returns.",
        "You hold a falling stock to avoid \"booking\" a loss, even when exiting would improve your portfolio.")
    bias_card("Overconfidence",
        "Overestimating one's knowledge, skills, or ability to predict market movements. Leads to excessive trading and underestimation of risk.",
        "After a few wins, you double position sizes without questioning whether luck played a role.")
    bias_card("Herding",
        "Following the crowd rather than making independent, research-based decisions. Social influence and FOMO drive crowded trades and increased risk exposure.",
        "You buy a trending stock purely because everyone around you is investing in it.")
    bias_card("Disposition Effect",
        "Selling winners too early and holding losers too long. Driven by the desire to realise gains and avoid the regret associated with realised losses.",
        "You sell at a small gain but keep a losing stock for months hoping for a recovery.")
    bias_card("Status Quo Bias",
        "Preference for keeping existing investments unchanged due to inertia and familiarity, even when better alternatives exist.",
        "You haven't reviewed your portfolio in two years because changing it feels effortful.")
    bias_card("Emotional / Overtrading Bias",
        "Letting fear or excitement drive frequent trades rather than a disciplined long-term strategy. Results in poor timing, higher costs, and reactive decisions.",
        "On a volatile day, you place multiple impulsive trades instead of sticking to your plan.")
    st.divider()


# ══════════════════════════════════════════════════
# TAB 7 — ABOUT
# ══════════════════════════════════════════════════
with tab_about:
    st.header("About This Project")
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h3>Overview</h3>
        <p style="color:#6b6860;font-size:14px;line-height:1.7;margin-top:10px;">
        The Behavioural Robo-Advisor is an academic project analysing how psychological biases
        and demographic patterns influence investment decisions. Unlike traditional financial tools
        that focus only on returns and risk, this system integrates behavioural finance principles
        for deeper investor insights.
        </p>
    </div>
    <div class="card">
        <h3>Objectives</h3>
        <ul style="color:#6b6860;font-size:14px;line-height:1.8;margin-top:10px;padding-left:18px;">
            <li>Identify behavioural biases in investment decisions among Indian investors</li>
            <li>Develop a Behavioural Finance Scoring System (BFS)</li>
            <li>Analyse patterns across age and gender groups</li>
            <li>Provide data-driven and self-assessment insights through a functional prototype</li>
        </ul>
    </div>
    <div class="card">
        <h3>Data</h3>
        <ul style="color:#6b6860;font-size:14px;line-height:1.8;margin-top:10px;padding-left:18px;">
            <li><strong style="color:#1a1a18;">Primary:</strong> ~135 survey responses from Indian investors</li>
            <li><strong style="color:#1a1a18;">Secondary:</strong> Sector-wise allocation across 220 investor profiles and 10 market sectors</li>
        </ul>
    </div>
    <div class="card">
        <h3>Research Basis</h3>
        <ul style="color:#6b6860;font-size:14px;line-height:1.8;margin-top:10px;padding-left:18px;">
            <li>Barber &amp; Odean (2001) &mdash; Gender, Overconfidence and Stock Investment</li>
            <li>Shefrin &amp; Statman (2000) &mdash; Behavioural Portfolio Theory</li>
            <li>Pompian (2012) &mdash; Behavioural Finance and Investor Types</li>
            <li>NISM and SEBI Investor Reports (2022&ndash;2024)</li>
        </ul>
    </div>
    <div class="card">
        <h3>Disclaimer</h3>
        <p style="color:#6b6860;font-size:14px;line-height:1.7;margin-top:10px;">
        This tool is developed for academic and research purposes only.
        It does not constitute financial advice or investment recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)
