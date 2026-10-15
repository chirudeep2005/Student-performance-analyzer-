from pathlib import Path
import csv
import requests
from bs4 import BeautifulSoup
HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs" / "quotes.csv"
URL = "https://quotes.toscrape.com/"
HEADERS = {"User-Agent": "StudentPortfolioDemo/1.0 (educational example)"}

def scrape_quotes(url=URL):
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    rows = []
    for card in soup.select("div.quote"):
        quote, author = card.select_one("span.text"), card.select_one("small.author")
        tags = [tag.get_text(strip=True) for tag in card.select("a.tag")]
        if quote and author:
            rows.append({"quote": quote.get_text(strip=True), "author": author.get_text(strip=True), "tags": "; ".join(tags)})
    return rows

def main():
    try: rows = scrape_quotes()
    except requests.RequestException as exc: raise SystemExit(f"Could not fetch practice site; check connection. Details: {exc}") from exc
    if not rows: raise SystemExit("No quote cards found; site structure may have changed.")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["quote", "author", "tags"]); writer.writeheader(); writer.writerows(rows)
    print(f"Collected {len(rows)} quotes from first page. Saved to {OUT}")
    for row in rows[:3]: print(f"- {row['quote']} — {row['author']} [{row['tags']}]")

if __name__ == "__main__": main()
