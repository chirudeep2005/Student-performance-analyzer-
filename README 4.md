# Web Scraping & Data Collection

A small BeautifulSoup scraper that extracts quote text, author names, and tags from `https://quotes.toscrape.com/`, a public practice website intended for scraping exercises, then saves the records as CSV.

## Run
`pip install -r requirements.txt` then `python main.py`

The script includes a request timeout, HTTP status check, and basic missing-element handling. It reads the first page only.

Responsible scraping: check terms and robots.txt, use reasonable request rates, and never bypass authentication, CAPTCHAs, or access controls. The included project does not scrape private or login-protected data.
