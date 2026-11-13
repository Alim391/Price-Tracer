from datetime import datetime
import sqlite3
from bs4 import BeautifulSoup
import requests

URL = "https://wise.com/ru/currency-converter/usd-to-tjs-rate"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}
DB_NAME = "currency_tracker.db"


def init_db():
  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rate TEXT,
            date_time TEXT
        )
    """)
  conn.commit()
  conn.close()


def save_rate(rate_text):
  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()
  now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  cursor.execute(
      "INSERT INTO rates (rate, date_time) VALUES (?, ?)", (rate_text, now)
  )
  conn.commit()
  conn.close()
  print(f"[DB] Saved: {rate_text} at {now}")


def parse_rate():
  resp = requests.get(URL, headers=HEADERS)
  if resp.status_code != 200:
    print(f"Error: {resp.status_code}")
    return

  soup = BeautifulSoup(resp.text, "html.parser")
  prices = soup.find_all(string=lambda t: t and "TJS" in t)

  for item in prices:
    text = item.strip()
    if len(text) < 25:
      print(f"Found rate: {text}")
      save_rate(text)
      break


if __name__ == "__main__":
  init_db()
  parse_rate()