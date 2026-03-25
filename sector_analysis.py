import pandas as pd
import streamlit as st

# --------------------------------------------------
# AGE LABEL MAPPING
# App selectbox uses "18-25 years" format
# Sector Excel uses "18-25" format (no "years")
# This map converts between the two
# --------------------------------------------------
AGE_MAP = {
    "18-25 years": "18-25",
    "26-40 years": "26-40",
    "41-55 years": "41-55",
    "56-70 years": "56-70",
    "70+ years":   "70+",
}

# --------------------------------------------------
# LOAD & CACHE DATASET
# --------------------------------------------------
@st.cache_data
def _load_sector_data():
    df = pd.read_excel("Stock_Sector_Allocation.xlsx", header=2)
    df.columns = df.columns.str.replace("%", "", regex=False)
    df.columns = df.columns.str.replace("()", "", regex=False)
    df.columns = df.columns.str.strip()
    df = df.rename(columns={"Age Group": "Age"})
    return df

# --------------------------------------------------
# SECTOR ANALYSIS FUNCTION
# --------------------------------------------------
def sector_analysis(age, gender):
    df = _load_sector_data()

    # Convert "18-25 years" → "18-25" to match the Excel values
    age_key = AGE_MAP.get(age, age)

    sector_columns = df.columns[3:]

    filtered = df[(df["Age"] == age_key) & (df["Gender"] == gender)]

    if filtered.empty:
        return None, None, None

    sector_avg = filtered[sector_columns].mean()
    most_sector = sector_avg.idxmax()
    least_sector = sector_avg.idxmin()

    return most_sector, least_sector, sector_avg
