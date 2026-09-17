import sqlite3
import pandas as pd

connection = sqlite3.connect("data_pipeline/books.db")

books = pd.read_sql(
    "SELECT * FROM books",
    connection
)

categories = pd.read_sql(
    "SELECT * FROM categories",
    connection
)

# Reproduce SQL JOIN using pandas
merged = pd.merge(
    books,
    categories,
    on="category_id"
)

print("Pandas merge result:")
print(merged.head(10))

connection.close()