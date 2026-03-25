# Bias–portfolio mapping rules will go here
import streamlit as st

# --------------------------------------------------
# PRE-COMPUTED BIAS AVERAGES BY AGE GROUP
# Source: "BFS average for each age" sheet from
# The_Investor_Mindset__Data_Analysis_.xlsx
#
# Bias order (columns C–N in that sheet):
#   Confirmation Bias, Anchoring (Q4), Anchoring (Q5),
#   Recency Bias, Framing Effect, Availability Bias,
#   Loss Aversion, Overconfidence, Herding,
#   Disposition Effect, Status Quo Bias,
#   Emotional / Overtrading Bias
#
# Note: Q4 and Q5 both map to Anchoring — averaged together.
# "Availability Bias" in the sheet = "Risk Sensitivity" in app.
# --------------------------------------------------

BIAS_AVERAGES = {
    "18-25": {
        "Confirmation Bias":            3.447,
        "Anchoring":                    (2.585 + 2.489) / 2,
        "Recency Bias":                 2.734,
        "Framing Effect":               2.394,
        "Risk Sensitivity":             2.415,
        "Loss Aversion":                3.128,
        "Overconfidence":               2.702,
        "Herding":                      2.383,
        "Disposition Effect":           2.617,
        "Status Quo Bias":              2.426,
        "Emotional / Overtrading Bias": 2.638,
    },
    "26-40": {
        "Confirmation Bias":            3.100,
        "Anchoring":                    (2.750 + 2.400) / 2,
        "Recency Bias":                 2.750,
        "Framing Effect":               2.350,
        "Risk Sensitivity":             2.450,
        "Loss Aversion":                3.100,
        "Overconfidence":               2.700,
        "Herding":                      2.700,
        "Disposition Effect":           2.100,
        "Status Quo Bias":              2.200,
        "Emotional / Overtrading Bias": 2.550,
    },
    "41-55": {
        "Confirmation Bias":            3.533,
        "Anchoring":                    (2.200 + 2.267) / 2,
        "Recency Bias":                 2.867,
        "Framing Effect":               2.067,
        "Risk Sensitivity":             1.667,
        "Loss Aversion":                3.667,
        "Overconfidence":               2.800,
        "Herding":                      2.267,
        "Disposition Effect":           1.933,
        "Status Quo Bias":              2.533,
        "Emotional / Overtrading Bias": 1.733,
    },
    "56-70": {
        "Confirmation Bias":            3.000,
        "Anchoring":                    (2.000 + 2.500) / 2,
        "Recency Bias":                 1.500,
        "Framing Effect":               2.000,
        "Risk Sensitivity":             1.000,
        "Loss Aversion":                3.000,
        "Overconfidence":               3.000,
        "Herding":                      1.500,
        "Disposition Effect":           3.500,
        "Status Quo Bias":              1.500,
        "Emotional / Overtrading Bias": 2.000,
    },
    "70+": {
        "Confirmation Bias":            2.000,
        "Anchoring":                    (3.500 + 3.000) / 2,
        "Recency Bias":                 3.000,
        "Framing Effect":               1.500,
        "Risk Sensitivity":             1.500,
        "Loss Aversion":                2.500,
        "Overconfidence":               3.500,
        "Herding":                      3.000,
        "Disposition Effect":           2.500,
        "Status Quo Bias":              2.000,
        "Emotional / Overtrading Bias": 1.500,
    },
}

# --------------------------------------------------
# AGE LABEL MAPPING
# App selectbox uses "18-25 years" format
# BIAS_AVERAGES uses short keys "18-25"
# --------------------------------------------------
AGE_MAP = {
    "18-25 years": "18-25",
    "26-40 years": "26-40",
    "41-55 years": "41-55",
    "56-70 years": "56-70",
    "70+ years":   "70+",
}

# --------------------------------------------------
# DOMINANT BIAS FUNCTION
# gender param accepted for future use / extensibility
# but currently age-level data is used (no gender split
# in the Excel BFS average sheet)
# --------------------------------------------------
def get_dominant_bias(age: str, gender: str = None) -> dict:
    age_key = AGE_MAP.get(age, age)

    scores = BIAS_AVERAGES.get(age_key)

    if not scores:
        return {
            "dominant": "Insufficient data",
            "top3": [],
            "scores": {}
        }

    sorted_biases = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    return {
        "dominant": sorted_biases[0][0],
        "top3": [b for b, _ in sorted_biases[:3]],
        "scores": {b: round(s, 3) for b, s in sorted_biases}
    }
