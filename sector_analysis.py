import pandas as pd

# Load dataset
df = pd.read_excel("Stock_Sector_Allocation.xlsx", header=2)

# CLEAN COLUMN NAMES
df.columns = df.columns.str.replace(" (%)", "", regex=False)
df.columns = df.columns.str.strip()

# Rename columns
df = df.rename(columns={
    df.columns[1]: "Gender",
    df.columns[2]: "Age"
})

# Define non-sector columns
non_sector_cols = ["Gender", "Age"]

# Automatically detect sector columns
sector_columns = [col for col in df.columns if col not in non_sector_cols and col != df.columns[0]]


def sector_analysis(age, gender):

    filtered = df[(df["Age"] == age) & (df["Gender"] == gender)]

    if filtered.empty:
        return None, None, None

    # Average allocation for that demographic
    sector_avg = filtered[sector_columns].mean()

    # Highest and lowest sectors
    most_sector = sector_avg.idxmax()
    least_sector = sector_avg.idxmin()

    return most_sector, least_sector, sector_avg
