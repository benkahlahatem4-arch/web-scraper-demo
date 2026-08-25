"""Scrape book data from a public demo website and save it as CSV."""

import argparse
import csv
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

DEFAULT_URL = "https://books.toscrape.com/"
DEFAULT_OUTPUT = "sample_output.csv"
FIELDS = ["title", "price", "category", "link"]


def validate_url(url):
    """Return a valid HTTP(S) URL or raise ValueError."""
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("URL must start with http:// or https:// and include a host")
    return url


def scrape_books(url=DEFAULT_URL, timeout=10):
    """Download and parse book cards from a public practice page."""
    validate_url(url)
    try:
        response = requests.get(url, timeout=timeout, headers={"User-Agent": "BeginnerPortfolioScraper/1.0"})
        response.raise_for_status()
    except requests.RequestException as error:
        raise ConnectionError(f"Could not download {url}: {error}") from error
    soup = BeautifulSoup(response.text, "html.parser")
    books = []
    for card in soup.select("article.product_pod"):
        title_link = card.select_one("h3 a")
        price = card.select_one(".price_color")
        category = card.select_one(".category")
        books.append({
            "title": title_link.get("title", "").strip() if title_link else "",
            "price": price.get_text(strip=True) if price else "",
            "category": category.get_text(strip=True) if category else "",
            "link": urljoin(url, title_link.get("href", "")) if title_link else "",
        })
    if not books:
        raise ValueError("The page loaded successfully, but no book results were found")
    return books


def save_to_csv(rows, output_path):
    """Write rows to a UTF-8 CSV file."""
    if not rows:
        raise ValueError("Cannot export an empty result set")
    with Path(output_path).open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in FIELDS} for row in rows)


def main():
    parser = argparse.ArgumentParser(description="Scrape books and export them to CSV")
    parser.add_argument("--url", default=DEFAULT_URL, help="Public page to scrape")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="CSV output path")
    args = parser.parse_args()
    try:
        rows = scrape_books(args.url)
        save_to_csv(rows, args.output)
    except (ConnectionError, ValueError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    print(f"Saved {len(rows)} book records to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
