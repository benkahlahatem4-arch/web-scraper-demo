# Web Scraper Demo

A beginner-friendly Python portfolio project that collects publicly visible
book data from [Books to Scrape](https://books.toscrape.com/), a safe website
created for scraping practice, and exports the results to CSV.

This is a personal learning and portfolio demo for GitHub and Upwork. It is
not client work.

## What it extracts

- Book title
- Price
- Optional category
- Book link

## Installation

From this project folder, install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## How to run

Run the default scrape:

```bash
python scraper.py
```

The results are saved to `sample_output.csv`. You can choose a different
allowed public URL and output file:

```bash
python scraper.py --url https://books.toscrape.com/ --output books.csv
```

## Error handling

The script reports clear errors for invalid URLs, connection or HTTP failures,
missing fields, empty result pages, and empty CSV exports. Missing fields are
written as empty values so one incomplete result does not stop the export.

Only scrape websites you are allowed to access, and respect their terms and
robots.txt guidance.
