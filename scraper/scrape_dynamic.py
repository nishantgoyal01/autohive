from playwright.sync_api import sync_playwright
import pandas as pd
import time


URL = "https://www.cardekho.com/used-cars+in+ambikapur"


def scrape_cardekho():
    cars = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(URL, timeout=60000)
        time.sleep(5)

        # Scroll to load more cars
        for _ in range(5):
            page.mouse.wheel(0, 3000)
            time.sleep(2)

        car_cards = page.locator("div.bottom_container")
        count = car_cards.count()

        print(f"Total cars found: {count}")

        for i in range(count):
            card = car_cards.nth(i)

            try:
                name = card.locator("h3.title a").inner_text()
            except:
                name = None

            try:
                relative_url = card.locator("h3.title a").get_attribute("href")
                car_url = "https://www.cardekho.com" + relative_url
            except:
                car_url = None

            try:
                details = card.locator("div.dotsDetails").inner_text()
                parts = [x.strip() for x in details.split("•")]

                km_driven = parts[0] if len(parts) > 0 else None
                fuel_type = parts[1] if len(parts) > 1 else None
                transmission = parts[2] if len(parts) > 2 else None
            except:
                km_driven = None
                fuel_type = None
                transmission = None

            try:
                price = card.locator("div.priceAssured p").inner_text()
            except:
                price = None

            try:
                location = card.locator("div.distanceText").inner_text()
            except:
                location = None

            cars.append({
                "name": name,
                "price": price,
                "km_driven": km_driven,
                "fuel_type": fuel_type,
                "transmission": transmission,
                "location": location,
                "url": car_url
            })

        browser.close()

    return cars


if __name__ == "__main__":
    data = scrape_cardekho()

    df = pd.DataFrame(data)

    print(df.head())

    df.to_csv("data/raw_cardekho_cars.csv", index=False)

    print("Scraping completed. Data saved to data/raw_cardekho_cars.csv")