from bs4 import BeautifulSoup
from datetime import datetime


def parse_car_cards(html):
    soup = BeautifulSoup(html, "html.parser")
    car_cards = soup.select(".car-card")

    cars = []

    for card in car_cards:
        name = card.select_one(".car-name")
        price = card.select_one(".car-price")
        km = card.select_one(".car-km")
        fuel = card.select_one(".car-fuel")
        transmission = card.select_one(".car-transmission")
        location = card.select_one(".car-location")
        link = card.select_one("a")

        car = {
            "name": name.text.strip() if name else None,
            "price": price.text.strip() if price else None,
            "km_driven": km.text.strip() if km else None,
            "fuel_type": fuel.text.strip() if fuel else None,
            "transmission": transmission.text.strip() if transmission else None,
            "location": location.text.strip() if location else None,
            "url": link["href"] if link and link.has_attr("href") else None,
            "scraped_at": datetime.now().isoformat()
        }

        cars.append(car)

    return cars