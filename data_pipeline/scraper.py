import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

all_books = []

for page in range(1, 6):

    url = BASE_URL.format(page)

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.select("article.product_pod")

    print(f"Page {page}: {len(books)} books found")

    for book in books:

        title = book.h3.a["title"]

        price = book.select_one(".price_color").get_text(strip=True)

        rating = book.select_one("p.star-rating")["class"][1]

        availability = book.select_one(".availability").get_text(
            strip=True
        )

        # Get individual book page
        book_link = book.h3.a["href"]
        book_url = urljoin(url, book_link)

        book_response = requests.get(book_url, timeout=10)
        book_response.raise_for_status()

        book_soup = BeautifulSoup(
            book_response.text,
            "html.parser"
        )

        # Category from book detail page
        breadcrumb = book_soup.select("ul.breadcrumb li")

        if len(breadcrumb) >= 3:
            category = breadcrumb[-2].get_text(strip=True)
        else:
            category = "Unknown"

        all_books.append({
            "title": title,
            "price": price,
            "rating": rating,
            "availability": availability,
            "category": category
        })


print()
print("Total books scraped:", len(all_books))


# Convert to DataFrame
df = pd.DataFrame(all_books)


# Clean price
df["price_gbp"] = (
    df["price"]
    .str.replace("£", "", regex=False)
    .str.replace("Â", "", regex=False)
    .astype(float)
)


# Convert rating words to numbers
rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

df["rating"] = df["rating"].map(rating_map)


# Clean availability
df["in_stock"] = df["availability"].str.contains(
    "In stock",
    case=False,
    na=False
)


# Fixed exchange rate
GBP_TO_INR = 105.50

df["price_inr"] = df["price_gbp"] * GBP_TO_INR


# Show category count
print("Categories found:", df["category"].nunique())

print()
print("Categories:")
print(df["category"].value_counts())


# Show first 5 rows
print()
print(df.head())


# Show data types
print()
print(df.dtypes)


# Save cleaned data
df.to_csv(
    "data_pipeline/books.csv",
    index=False
)

print()
print("Books saved to books.csv successfully!")