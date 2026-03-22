import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_excel("Stock_Sector_Allocation.xlsx", header=2)

# Clean column names
df.columns = df.columns.str.replace(" (%)", "", regex=False)
df.columns = df.columns.str.strip()

# Rename columns
df = df.rename(columns={
    df.columns[1]: "Gender",
    df.columns[2]: "Age"
})

# Identify sector columns
non_sector_cols = ["Gender", "Age"]
sector_columns = [col for col in df.columns if col not in non_sector_cols and col != df.columns[0]]

# Create target column (preferred sector)
df["Preferred Sector"] = df[sector_columns].idxmax(axis=1)

# Encode categorical data
le_age = LabelEncoder()
le_gender = LabelEncoder()
le_sector = LabelEncoder()

df["Age_encoded"] = le_age.fit_transform(df["Age"])
df["Gender_encoded"] = le_gender.fit_transform(df["Gender"])
df["Sector_encoded"] = le_sector.fit_transform(df["Preferred Sector"])

# Features & target
X = df[["Age_encoded", "Gender_encoded"]]
y = df["Sector_encoded"]

# Train model
model = DecisionTreeClassifier()
model.fit(X, y)

# Prediction function
def predict_sector(age, gender):
    try:
        age_enc = le_age.transform([age])[0]
        gender_enc = le_gender.transform([gender])[0]

        pred = model.predict([[age_enc, gender_enc]])[0]
        return le_sector.inverse_transform([pred])[0]

    except:
        return "No prediction available"
