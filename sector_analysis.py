import pandas as pd

# Load dataset
df = pd.read_excel("Stock_Sector_Allocation.xlsx", header=1)

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

    # Filter by demographic
    filtered = df[(df["Age"] == age) & (df["Gender"] == gender)]

    if filtered.empty:
        return None, None

    # Calculate mean allocation
    sector_avg = filtered[sector_columns].mean()

    # Most preferred sector
    most_sector = sector_avg.idxmax()

    # Least preferred sector
    least_sector = sector_avg.idxmin()

    return most_sector, least_sector
