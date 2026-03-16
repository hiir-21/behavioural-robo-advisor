import pandas as pd

# load dataset
df = pd.read_excel("Stock_Sector_Allocation.xlsx", header=1)

# rename columns for easier use
df = df.rename(columns={
    df.columns[1]: "Gender",
    df.columns[2]: "Age"
})

sector_columns = [
    "Technology\n(%)",
    "Healthcare\n(%)",
    "Finance\n(%)",
    "Energy\n(%)",
    "Consumer Goods\n(%)",
    "Real Estate\n(%)",
    "Utilities\n(%)",
    "Industrials\n(%)",
    "Materials\n(%)",
    "Telecom\n(%)"
]

def sector_analysis(age, gender):

    filtered = df[(df["Age"] == age) & (df["Gender"] == gender)]

    if filtered.empty:
        return None, None

    sector_avg = filtered[sector_columns].mean()

    most = sector_avg.idxmax().replace("\n(%)","")
    least = sector_avg.idxmin().replace("\n(%)","")

    return most, least
