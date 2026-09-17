import pandas as pd

# Read the scraped data
df = pd.read_csv("data_pipeline/books.csv")

# Remove duplicate rows
df = df.drop_duplicates()

# Remove missing values
df = df.dropna()

# Clean the price column
df["price"] = df["price"].str.replace("£", "", regex=False)
df["price"] = pd.to_numeric(df["price"], errors="coerce")

# Save cleaned data
df.to_csv("data_pipeline/books_cleaned.csv", index=False)

print("Cleaned data saved successfully!")
print(df.head())