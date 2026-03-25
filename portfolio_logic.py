"""
portfolio_logic.py

Portfolio Analysis Module
--------------------------
Accepts a user-uploaded DataFrame with columns:
    Stock | Sector | Quantity | Buy Price (INR) | Current Price (INR)

Computes:
    1. Per-holding return, gain/loss
    2. Portfolio-level metrics (total value, total return %, weighted return)
    3. Sector allocation (%)
    4. Diversification score & concentration risk flags
    5. Bias-portfolio connections based on detected dominant bias

Fully rule-based — no external API or price feed needed.
"""

import pandas as pd

# ── Expected columns ──────────────────────────────────────────────────────────
REQUIRED_COLS = ["Stock", "Sector", "Quantity", "Buy Price (INR)", "Current Price (INR)"]

# ── Bias → portfolio behaviour mapping ───────────────────────────────────────
# For each bias, describes what pattern in the portfolio it may explain,
# and what corrective action to take.
BIAS_PORTFOLIO_INSIGHTS = {
    "Confirmation Bias": {
        "pattern": "concentrated in sectors you follow closely",
        "flag": lambda df: df["Sector"].value_counts().iloc[0] / len(df) > 0.5,
        "insight": (
            "Your portfolio is heavily concentrated in one or two sectors. "
            "Confirmation bias may be causing you to over-invest in sectors you follow "
            "closely while ignoring contradicting signals from others."
        ),
        "action": "Consider reviewing underrepresented sectors using objective data rather than only familiar sources."
    },
    "Anchoring": {
        "pattern": "holdings still held near buy price despite changed fundamentals",
        "flag": lambda df: ((df["Return (%)"].abs() < 5)).sum() / len(df) > 0.4,
        "insight": (
            "A significant portion of your holdings show near-zero returns. "
            "Anchoring bias may be causing you to hold positions simply because "
            "they haven't moved far from your purchase price."
        ),
        "action": "Evaluate each holding on current fundamentals, not the price you paid."
    },
    "Recency Bias": {
        "pattern": "overweight in recently trending sectors",
        "flag": lambda df: df["Sector"].value_counts().iloc[0] / len(df) > 0.45,
        "insight": (
            "Your portfolio may be overweight in sectors that have performed well recently. "
            "Recency bias leads investors to extrapolate short-term trends into long-term expectations."
        ),
        "action": "Check whether your top sector allocation reflects long-term conviction or recent performance chasing."
    },
    "Loss Aversion": {
        "pattern": "holding losing positions while selling winners",
        "flag": lambda df: (df["Return (%)"] < -10).sum() >= 1,
        "insight": (
            "You have holdings with significant unrealised losses. "
            "Loss aversion often causes investors to hold losers too long to avoid "
            "the psychological pain of booking a loss."
        ),
        "action": "Assess whether each loss-making holding still has a fundamental case, or if it is being held solely to avoid realising a loss."
    },
    "Overconfidence": {
        "pattern": "under-diversified portfolio with high concentration",
        "flag": lambda df: len(df["Sector"].unique()) < 4,
        "insight": (
            "Your portfolio spans few sectors, suggesting high conviction bets. "
            "Overconfidence bias leads investors to under-diversify, believing their "
            "stock-picking ability is better than it is."
        ),
        "action": "Ensure diversification is based on analysis, not certainty. Consider adding uncorrelated sectors."
    },
    "Herding": {
        "pattern": "holdings concentrated in widely discussed stocks",
        "flag": lambda df: df["Sector"].value_counts().iloc[0] / len(df) > 0.4,
        "insight": (
            "Your portfolio shows sector concentration that may reflect following popular market trends. "
            "Herding bias leads investors to buy what everyone else is buying rather than "
            "based on independent analysis."
        ),
        "action": "Review whether your top holdings were chosen through independent research or following market sentiment."
    },
    "Disposition Effect": {
        "pattern": "selling winners early, holding losers",
        "flag": lambda df: (df["Return (%)"] < 0).sum() > (df["Return (%)"] > 15).sum(),
        "insight": (
            "Your portfolio has more losing positions than strong gainers, which can indicate "
            "the disposition effect — the tendency to sell winners too quickly to lock in gains "
            "while holding losers hoping for a recovery."
        ),
        "action": "Let your winners run based on fundamentals, and cut losses when the investment thesis has broken down."
    },
    "Status Quo Bias": {
        "pattern": "portfolio unchanged, dominated by old holdings",
        "flag": lambda df: len(df) < 5,
        "insight": (
            "A small, potentially unchanged portfolio may reflect status quo bias — "
            "the tendency to keep existing investments simply because changing them feels uncomfortable."
        ),
        "action": "Schedule a periodic portfolio review to reassess each holding objectively rather than by default."
    },
    "Framing Effect": {
        "pattern": "allocation decisions influenced by how returns are presented",
        "flag": lambda df: df["Return (%)"].std() > 30,
        "insight": (
            "High return variability across your holdings suggests decision-making may be "
            "influenced by how performance is framed — focusing on percentage gains on winners "
            "while mentally framing losses differently."
        ),
        "action": "Evaluate all holdings on the same consistent metric (e.g. absolute return vs benchmark) rather than in isolation."
    },
    "Risk Sensitivity": {
        "pattern": "overly conservative allocation despite long time horizon",
        "flag": lambda df: (df["Return (%)"].between(-5, 5)).sum() / len(df) > 0.5,
        "insight": (
            "A large proportion of your holdings are near flat, suggesting a very conservative "
            "approach. High risk sensitivity may be causing you to avoid positions with "
            "growth potential due to perceived volatility."
        ),
        "action": "Reassess your risk tolerance in the context of your investment horizon and financial goals."
    },
    "Emotional / Overtrading Bias": {
        "pattern": "fragmented portfolio with many small positions",
        "flag": lambda df: len(df) > 15,
        "insight": (
            "A very large number of holdings may indicate frequent buying driven by "
            "emotional reactions to market movements rather than a deliberate strategy."
        ),
        "action": "Consolidate your portfolio around your highest-conviction, well-researched positions."
    },
}

# ── Diversification thresholds ────────────────────────────────────────────────
def _diversification_score(n_sectors: int, n_holdings: int) -> dict:
    if n_sectors >= 5 and n_holdings >= 8:
        level = "Well diversified"
        color = "good"
    elif n_sectors >= 3 and n_holdings >= 5:
        level = "Moderately diversified"
        color = "moderate"
    else:
        level = "Concentrated — diversification risk"
        color = "poor"
    return {"level": level, "color": color, "n_sectors": n_sectors, "n_holdings": n_holdings}


# ── Main analysis function ────────────────────────────────────────────────────
def analyse_portfolio(df: pd.DataFrame, dominant_bias: str = None) -> dict:
    """
    Parameters
    ----------
    df : pd.DataFrame
        Must contain REQUIRED_COLS exactly.
    dominant_bias : str, optional
        The investor's dominant behavioural bias from BFS / Quick Analysis.
        If provided, generates a personalised bias-portfolio insight.

    Returns
    -------
    dict with keys:
        holdings        — enriched DataFrame with per-row metrics
        summary         — portfolio-level aggregates
        sector_alloc    — sector allocation Series (%)
        diversification — diversification assessment dict
        bias_insight    — personalised bias-portfolio connection (or None)
        flags           — list of risk flag strings
    """

    df = df.copy()

    # ── Clean numeric columns ─────────────────────────────────────────────────
    for col in ["Quantity", "Buy Price (INR)", "Current Price (INR)"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["Quantity", "Buy Price (INR)", "Current Price (INR)"])

    # ── Per-holding calculations ──────────────────────────────────────────────
    df["Invested Value (INR)"]  = df["Quantity"] * df["Buy Price (INR)"]
    df["Current Value (INR)"]   = df["Quantity"] * df["Current Price (INR)"]
    df["Gain / Loss (INR)"]     = df["Current Value (INR)"] - df["Invested Value (INR)"]
    df["Return (%)"]            = ((df["Current Price (INR)"] - df["Buy Price (INR)"]) /
                                    df["Buy Price (INR)"]) * 100

    # ── Portfolio-level summary ───────────────────────────────────────────────
    total_invested = df["Invested Value (INR)"].sum()
    total_current  = df["Current Value (INR)"].sum()
    total_gain     = total_current - total_invested
    total_return   = ((total_current - total_invested) / total_invested * 100) if total_invested > 0 else 0

    # Weighted average return
    df["Weight"]          = df["Current Value (INR)"] / total_current
    weighted_return       = (df["Return (%)"] * df["Weight"]).sum()

    best_holding  = df.loc[df["Return (%)"].idxmax(), "Stock"]
    worst_holding = df.loc[df["Return (%)"].idxmin(), "Stock"]
    best_return   = df["Return (%)"].max()
    worst_return  = df["Return (%)"].min()

    summary = {
        "total_invested":  round(total_invested, 2),
        "total_current":   round(total_current, 2),
        "total_gain":      round(total_gain, 2),
        "total_return":    round(total_return, 2),
        "weighted_return": round(weighted_return, 2),
        "n_holdings":      len(df),
        "best_holding":    best_holding,
        "best_return":     round(best_return, 2),
        "worst_holding":   worst_holding,
        "worst_return":    round(worst_return, 2),
    }

    # ── Sector allocation ─────────────────────────────────────────────────────
    sector_alloc = (
        df.groupby("Sector")["Current Value (INR)"].sum() / total_current * 100
    ).round(2).sort_values(ascending=False)

    # ── Diversification ───────────────────────────────────────────────────────
    diversification = _diversification_score(
        n_sectors=df["Sector"].nunique(),
        n_holdings=len(df)
    )

    # ── Risk flags ────────────────────────────────────────────────────────────
    flags = []
    top_sector_pct = sector_alloc.iloc[0] if len(sector_alloc) > 0 else 0
    if top_sector_pct > 50:
        flags.append(f"High concentration: {sector_alloc.index[0]} accounts for {top_sector_pct:.1f}% of portfolio.")
    if (df["Return (%)"] < -20).any():
        bad = df[df["Return (%)"] < -20]["Stock"].tolist()
        flags.append(f"Significant losses (>20% down): {', '.join(bad)}.")
    if df["Sector"].nunique() < 3:
        flags.append("Portfolio spans fewer than 3 sectors — consider broader diversification.")
    if len(df) == 1:
        flags.append("Single holding — extremely concentrated portfolio.")

    # ── Bias-portfolio insight ────────────────────────────────────────────────
    bias_insight = None
    if dominant_bias and dominant_bias in BIAS_PORTFOLIO_INSIGHTS:
        entry = BIAS_PORTFOLIO_INSIGHTS[dominant_bias]
        triggered = False
        try:
            triggered = entry["flag"](df)
        except Exception:
            triggered = True  # default to showing insight if flag check fails
        bias_insight = {
            "bias":      dominant_bias,
            "pattern":   entry["pattern"],
            "triggered": triggered,
            "insight":   entry["insight"],
            "action":    entry["action"],
        }

    # ── Round display columns ─────────────────────────────────────────────────
    df["Return (%)"]           = df["Return (%)"].round(2)
    df["Invested Value (INR)"] = df["Invested Value (INR)"].round(2)
    df["Current Value (INR)"]  = df["Current Value (INR)"].round(2)
    df["Gain / Loss (INR)"]    = df["Gain / Loss (INR)"].round(2)
    df["Weight"]               = (df["Weight"] * 100).round(2)
    df = df.rename(columns={"Weight": "Portfolio Weight (%)"})

    return {
        "holdings":        df,
        "summary":         summary,
        "sector_alloc":    sector_alloc,
        "diversification": diversification,
        "bias_insight":    bias_insight,
        "flags":           flags,
    }


def validate_upload(df: pd.DataFrame) -> tuple[bool, str]:
    """
    Returns (True, "") if valid, (False, error_message) if not.
    """
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        return False, f"Missing columns: {', '.join(missing)}. Expected: {', '.join(REQUIRED_COLS)}"
    if len(df) == 0:
        return False, "Uploaded file has no data rows."
    if len(df) > 100:
        return False, "Maximum 100 holdings supported."
    return True, ""
