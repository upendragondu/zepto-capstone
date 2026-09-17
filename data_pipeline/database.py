import sqlite3
import pandas as pd

DB_PATH = "zepto.db"
CSV_PATH = "data_pipeline/books.csv"

# Connect to database
conn = sqlite3.connect(DB_PATH)

# Enable foreign keys
conn.execute("PRAGMA foreign_keys = ON")

# Read cleaned CSV
df = pd.read_csv(CSV_PATH)

# Create categories table
conn.execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE NOT NULL
)
""")

# Create books table
conn.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price_gbp REAL,
    price_inr REAL,
    rating INTEGER,
    availability TEXT,
    in_stock INTEGER,
    category_id INTEGER,
    FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
)
""")

# Start fresh
conn.execute("DELETE FROM books")
conn.execute("DELETE FROM categories")
conn.commit()

# Insert categories
for category in df["category"].dropna().unique():

    conn.execute(
        """
        INSERT INTO categories (category_name)
        VALUES (?)
        """,
        (category,)
    )

conn.commit()

# Insert books
for _, row in df.iterrows():

    category_result = conn.execute(
        """
        SELECT category_id
        FROM categories
        WHERE category_name = ?
        """,
        (row["category"],)
    ).fetchone()

    category_id = category_result[0]

    conn.execute(
        """
        INSERT INTO books
        (
            title,
            price_gbp,
            price_inr,
            rating,
            availability,
            in_stock,
            category_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            row["title"],
            row["price_gbp"],
            row["price_inr"],
            row["rating"],
            row["availability"],
            int(row["in_stock"]),
            category_id
        )
    )

conn.commit()

# Check counts
book_count = conn.execute(
    "SELECT COUNT(*) FROM books"
).fetchone()[0]

category_count = conn.execute(
    "SELECT COUNT(*) FROM categories"
).fetchone()[0]

print("Books inserted:", book_count)
print("Categories inserted:", category_count)

# Check JOIN
join_df = pd.read_sql_query(
    """
    SELECT
        b.book_id,
        b.title,
        b.price_inr,
        c.category_name
    FROM books b
    JOIN categories c
        ON b.category_id = c.category_id
    LIMIT 5
    """,
    conn
)

print("\nJOIN result:")
print(join_df)

conn.close()

print("\nDatabase created successfully!")