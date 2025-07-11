# scraper.py
import requests
import json
from pathlib import Path
from bs4 import BeautifulSoup
import pydantic

class Product(pydantic.BaseModel):
    title: str
    price: str
    url: str
    description: str = ""
    rating: str | None = None

BASE = "http://books.toscrape.com/catalogue/"
PAGE = "page-1.html"

def scrape_books():
    resp = requests.get(f"{BASE}{PAGE}")
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    articles = soup.select("article.product_pod")[:10]
    results = []
    for art in articles:
        title = art.h3.a["title"]
        raw_price = art.select_one("p.price_color").text
        price = raw_price.replace("Â", "")   # remove stray Â
        rel = art.h3.a["href"]
        url = BASE + rel
        classes = art.select_one("p.star-rating")["class"]
        rating = next((c for c in classes if c != "star-rating"), None)
        results.append(Product(
            title=title,
            price=price,
            url=url,
            rating=rating
        ))
    return results

def main():
    books = scrape_books()
    Path("products_raw.json").write_text(
        json.dumps([b.dict() for b in books], indent=2),
        encoding="utf-8"
    )

if __name__ == "__main__":
    main()
