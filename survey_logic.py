# Survey scoring logic will go here
"""
survey_logic.py

Purpose
-------
1. Analyze Behavioral Bias Questions (Q3–Q14)
   - Compute Bias-wise scores
   - Compute Behavioral Finance Score (BFS)
2. Analyze Risk Appetite Questions (Q15–Q22)
   - Compute Risk Appetite Score
   - Classify Risk Profile

This module:
- Does NOT handle UI
- Does NOT give portfolio advice
- Is fully rule-based & explainable
"""

from collections import defaultdict

# ==================================================
# SECTION 1 — BEHAVIORAL BIAS LOGIC (Q3–Q14)
# ==================================================

QUESTION_BIAS_MAP = {
    "Q3": "Confirmation Bias",
    "Q4": "Anchoring",
    "Q5": "Anchoring",
    "Q6": "Recency Bias",
    "Q7": "Framing Effect",
    "Q8": "Risk Sensitivity",
    "Q9": "Loss Aversion",
    "Q10": "Overconfidence",
    "Q11": "Herding",
    "Q12": "Disposition Effect",
    "Q13": "Status Quo Bias",
    "Q14": "Emotional / Overtrading Bias"
}

def normalize_score(score: int) -> float:
    if score < 1 or score > 5:
        raise ValueError("Scores must be between 1 and 5")
    return (score - 1) / 4


def compute_bias_scores(responses: dict) -> dict:
    """
    Computes normalized bias-wise scores for Q3–Q14
    """
    bias_accumulator = defaultdict(list)

    for q, score in responses.items():
        if q not in QUESTION_BIAS_MAP:
            continue
        bias = QUESTION_BIAS_MAP[q]
        bias_accumulator[bias].append(normalize_score(score))

    return {
        bias: round(sum(values) / len(values), 3)
        for bias, values in bias_accumulator.items()
    }


def classify_bias_intensity(score: float) -> str:
    if score <= 0.33:
        return "Low"
    elif score <= 0.66:
        return "Moderate"
    else:
        return "High"


def generate_bias_profile(responses: dict) -> dict:
    bias_scores = compute_bias_scores(responses)

    return {
        bias: {
            "score": score,
            "level": classify_bias_intensity(score)
        }
        for bias, score in bias_scores.items()
    }


def compute_bfs_score(responses: dict) -> dict:
    """
    Behavioral Finance Score (BFS) for Q3–Q14
    """
    bfs_questions = [q for q in responses if q.startswith("Q") and 3 <= int(q[1:]) <= 14]

    bfs_score = sum(responses[q] for q in bfs_questions)
    max_score = len(bfs_questions) * 5
    bfs_percentage = round((bfs_score / max_score) * 100, 2)

    if bfs_score <= 28:
        category = "Low Bias-Prone"
    elif bfs_score <= 44:
        category = "Moderately Bias-Prone"
    else:
        category = "Highly Bias-Prone"

    return {
        "bfs_score": bfs_score,
        "max_score": max_score,
        "bfs_percentage": bfs_percentage,
        "category": category
    }

# ==================================================
# SECTION 2 — RISK APPETITE LOGIC (Q15–Q22)
# ==================================================

def compute_risk_appetite_score(responses: dict) -> dict:
    """
    Risk Appetite Score based on Q15–Q22
    """

    risk_questions = [q for q in responses if q.startswith("Q") and 15 <= int(q[1:]) <= 22]

    scores = [responses[q] for q in risk_questions]

    if not scores:
        raise ValueError("No risk appetite responses provided")

    average_score = round(sum(scores) / len(scores), 2)

    if average_score <= 2.0:
        category = "Low Risk Appetite"
        interpretation = (
            "Prefers stability and capital protection, "
            "with limited tolerance for volatility."
        )
    elif average_score <= 3.5:
        category = "Moderate Risk Appetite"
        interpretation = (
            "Willing to accept moderate volatility for balanced growth, "
            "with some focus on long-term appreciation."
        )
    else:
        category = "Moderate to High Risk Appetite"
        interpretation = (
            "Comfortable with volatility for long-term growth and "
            "prioritizes capital appreciation over short-term income."
        )

    return {
        "average_score": average_score,
        "category": category,
        "interpretation": interpretation
    }

# ==================================================
# SECTION 3 — FULL SURVEY ANALYSIS (ONE CALL)
# ==================================================

def generate_full_survey_analysis(responses: dict) -> dict:
    """
    Combines:
    - Bias profile
    - BFS summary
    - Risk appetite analysis
    """

    return {
        "behavioral_bias_analysis": {
            "bias_profile": generate_bias_profile(responses),
            "bfs_summary": compute_bfs_score(responses)
        },
        "risk_appetite_analysis": compute_risk_appetite_score(responses)
    }
