import pandas as pd

# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------
df = pd.read_excel("Stock_Sector_Allocation.xlsx", header=2)

# --------------------------------------------------
# CLEAN COLUMN NAMES
# --------------------------------------------------
# Remove " (%)" from sector names and trim spaces
df.columns = df.columns.str.replace("%", "", regex=False)
df.columns = df.columns.str.replace("()", "", regex=False)
df.columns = df.columns.str.strip()

# --------------------------------------------------
# STANDARDIZE COLUMN NAMES
# --------------------------------------------------
df = df.rename(columns={
    "Age Group": "Age",
    "Gender": "Gender"
})

# --------------------------------------------------
# IDENTIFY SECTOR COLUMNS
# --------------------------------------------------
# First column = Client ID
# Next two = Gender, Age
# Remaining = sectors
sector_columns = df.columns[3:]

# --------------------------------------------------
# SECTOR ANALYSIS FUNCTION
# --------------------------------------------------
def sector_analysis(age, gender):

    # Filter by demographic
    filtered = df[(df["Age"] == age) & (df["Gender"] == gender)]

    if filtered.empty:
        return None, None, None

    # Calculate average allocation for that demographic
    sector_avg = filtered[sector_columns].mean()

    # Determine most and least preferred sectors
    most_sector = sector_avg.idxmax()
    least_sector = sector_avg.idxmin()

    return most_sector, least_sector, sector_avg
