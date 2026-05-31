import requests
from bs4 import BeautifulSoup


def fetch_static_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    return response.text


def parse_title(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.title.text.strip() if soup.title else "No title found"


if __name__ == "__main__":
    url = "https://example.com"

    html = fetch_static_page(url)
    title = parse_title(html)

    print("Page title:", title)