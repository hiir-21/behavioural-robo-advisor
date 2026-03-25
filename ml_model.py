import pandas as pd
import streamlit as st
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

# --------------------------------------------------
# AGE LABEL MAPPING
# App selectbox uses "18-25 years" format
# Sector Excel uses "18-25" format (no "years")
# --------------------------------------------------
AGE_MAP = {
    "18-25 years": "18-25",
    "26-40 years": "26-40",
    "41-55 years": "41-55",
    "56-70 years": "56-70",
    "70+ years":   "70+",
}

# --------------------------------------------------
# LOAD, TRAIN & CACHE MODEL
# --------------------------------------------------
@st.cache_resource
def _load_model():
    df = pd.read_excel("Stock_Sector_Allocation.xlsx", header=2)

    df.columns = df.columns.str.replace(" (%)", "", regex=False)
    df.columns = df.columns.str.strip()

    df = df.rename(columns={
        df.columns[1]: "Gender",
        df.columns[2]: "Age"
    })

    non_sector_cols = ["Gender", "Age"]
    sector_columns = [
        col for col in df.columns
        if col not in non_sector_cols and col != df.columns[0]
    ]

    df["Preferred Sector"] = df[sector_columns].idxmax(axis=1)

    le_age    = LabelEncoder()
    le_gender = LabelEncoder()
    le_sector = LabelEncoder()

    df["Age_encoded"]    = le_age.fit_transform(df["Age"])
    df["Gender_encoded"] = le_gender.fit_transform(df["Gender"])
    df["Sector_encoded"] = le_sector.fit_transform(df["Preferred Sector"])

    X = df[["Age_encoded", "Gender_encoded"]]
    y = df["Sector_encoded"]

    model = DecisionTreeClassifier(random_state=42)
    model.fit(X, y)

    return model, le_age, le_gender, le_sector

# --------------------------------------------------
# PREDICTION FUNCTION
# --------------------------------------------------
def predict_sector(age, gender):
    model, le_age, le_gender, le_sector = _load_model()

    # Convert "18-25 years" → "18-25" to match training data
    age_key = AGE_MAP.get(age, age)

    try:
        age_enc    = le_age.transform([age_key])[0]
        gender_enc = le_gender.transform([gender])[0]
        pred       = model.predict([[age_enc, gender_enc]])[0]
        return le_sector.inverse_transform([pred])[0]
    except ValueError:
        return "No prediction available"
