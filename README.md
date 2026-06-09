# Behavioural Robo-Advisor

A capstone project built for our BSc/BBA final year at Ahmedabad University. The idea came from a simple observation — most investing tools tell you what to do with your money but say nothing about *why* you make the decisions you do. This tries to fix that.

The app identifies psychological biases that influence investment behaviour, scores them, and connects them to patterns in your actual portfolio. It's built on behavioural finance research and about 135 survey responses we collected from Indian investors.

---

## What it does

There are two ways to use it:

**Quick Analysis** — select your age group and gender, get instant results. Uses a Decision Tree trained on 220 investor profiles to predict sector preferences, and looks up average bias scores for your demographic from our primary survey data. Takes about 5 seconds.

**Manual Assessment** — 22 questions about how you'd actually react in different investment situations (not how you think you should react). Your answers get scored across 11 behavioural biases, producing a Behavioural Finance Score (BFS) out of 60 and a Risk Appetite classification.

**Portfolio tab** — upload a CSV of your holdings and the app calculates your returns, sector allocation, and diversification. It then checks whether your dominant bias is actually showing up in your portfolio data — things like holding positions with large losses (Loss Aversion), or having fewer than 4 sectors (Overconfidence).

Results from both paths are shown together on the Results tab and stay there as long as you don't refresh the page.

---

## Files

```
app.py                        main app — all tabs, UI, session state
survey_logic.py               BFS and risk appetite scoring
sector_analysis.py            statistical sector lookup from Excel
ml_model.py                   Decision Tree sector predictor
bias_rules.py                 pre-computed demographic bias averages
portfolio_logic.py            portfolio analysis + bias-portfolio mapping
Stock_Sector_Allocation.xlsx  220 investor profiles across 10 sectors
Sectorwise Return Data.xlsx   11-year index return data for 10 sectors
requirements.txt              dependencies
```

---

## Running it locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Both Excel files need to be in the same folder as `app.py`.

---

## Portfolio upload format

The portfolio tab expects a CSV or Excel file with exactly these columns:

| Column | Example |
|--------|---------|
| Stock | Reliance Industries |
| Sector | Energy |
| Quantity | 10 |
| Buy Price (INR) | 2400 |
| Current Price (INR) | 2800 |

A sample template is available to download directly in the app.

Sectors should be one of: Technology, Finance, Healthcare, Energy, Consumer Goods, Real Estate, Utilities, Industrials, Materials, Telecom.

---

## Tech stack

- Python, Streamlit
- pandas, scikit-learn, Plotly, openpyxl

---

## Research basis

- Barber & Odean (2001) — Boys Will Be Boys: Gender, Overconfidence, and Common Stock Investment
- Shefrin & Statman (2000) — Behavioural Portfolio Theory
- Kahneman & Tversky (1979) — Prospect Theory
- Pompian (2012) — Behavioural Finance and Investor Types
- NISM and SEBI Investor Reports (2022–2024)

---


*Built for academic purposes only. Not financial advice.*
