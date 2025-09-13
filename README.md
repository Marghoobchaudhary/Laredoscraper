# Laredo Scraper (JSON)


Scrapes LaredoAnywhere with Selenium, intercepts API responses, enriches with doc details, and writes JSON.


## Setup
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate


pip install -r requirements.txt
cp .env.example .env # then edit with your creds
