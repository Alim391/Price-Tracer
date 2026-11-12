import requests
from bs4 import BeautifulSoup

URL = "https://wise.com/ru/currency-converter/usd-to-tjs-rate"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def get_usd_tjs_rate():
    print("Запрашиваем курс доллара к сомони...")
    response = requests.get(URL, headers=HEADERS)

    if response.status_code != 200:
        print(f"Ошибка соединения: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    print("Данные успешно получены! Ищем актуальный курс...")
    
    prices = soup.find_all(string=lambda text: text and "TJS" in text)

    for item in prices:
        clean_text = item.strip()
        if len(clean_text) < 25:
            print(" ->", clean_text)

if __name__ == "__main__":
    get_usd_tjs_rate()