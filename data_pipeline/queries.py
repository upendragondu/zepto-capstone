import sqlite3
import pandas as pd

DB_PATH = "zepto.db"

conn = sqlite3.connect(DB_PATH)

# Enable foreign keys
conn.execute("PRAGMA foreign_keys = ON")


# =========================
# QUERY 1
# SELECT + ORDER BY + LIMIT
# =========================

query1 = """
SELECT title, price_inr
FROM books
ORDER BY price_inr DESC
LIMIT 5;
"""

result1 = pd.read_sql_query(query1, conn)

print("\n===== QUERY 1 =====")
print(result1)


# =========================
# QUERY 2
# WHERE + BETWEEN
# =========================

query2 = """
SELECT title, price_inr, rating
FROM books
WHERE price_inr BETWEEN 3000 AND 5000
ORDER BY price_inr;
"""

result2 = pd.read_sql_query(query2, conn)

print("\n===== QUERY 2 =====")
print(result2.head(10))


# =========================
# QUERY 3
# DISTINCT
# =========================

query3 = """
SELECT DISTINCT rating
FROM books
ORDER BY rating;
"""

result3 = pd.read_sql_query(query3, conn)

print("\n===== QUERY 3 =====")
print(result3)


# =========================
# QUERY 4
# IN
# =========================

query4 = """
SELECT title, category_id, price_inr
FROM books
WHERE category_id IN (1, 2, 3)
ORDER BY price_inr DESC;
"""

result4 = pd.read_sql_query(query4, conn)

print("\n===== QUERY 4 =====")
print(result4.head(10))


# =========================
# QUERY 5
# JOIN
# =========================

query5 = """
SELECT
    b.title,
    b.price_inr,
    b.rating,
    c.category_name
FROM books b
JOIN categories c
    ON b.category_id = c.category_id
ORDER BY b.price_inr DESC
LIMIT 10;
"""

result5 = pd.read_sql_query(query5, conn)

print("\n===== QUERY 5 =====")
print(result5)


# =========================
# SAVE QUERY OUTPUTS
# =========================

result1.to_csv(
    "data_pipeline/query1_output.csv",
    index=False
)

result2.to_csv(
    "data_pipeline/query2_output.csv",
    index=False
)

result3.to_csv(
    "data_pipeline/query3_output.csv",
    index=False
)

result4.to_csv(
    "data_pipeline/query4_output.csv",
    index=False
)

result5.to_csv(
    "data_pipeline/query5_output.csv",
    index=False
)


# =========================
# PANDAS MERGE
# Reproduce JOIN
# =========================

books_df = pd.read_sql_query(
    "SELECT * FROM books",
    conn
)

categories_df = pd.read_sql_query(
    "SELECT * FROM categories",
    conn
)

merged_df = pd.merge(
    books_df,
    categories_df,
    on="category_id",
    how="inner"
)

print("\n===== PANDAS MERGE =====")
print(
    merged_df[
        ["title", "price_inr", "category_name"]
    ].head(10)
)


conn.close()

print("\nAll SQL queries completed successfully!")