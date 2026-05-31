import pandas as pd
import sqlite3
import os
import re


RAW_DATA_PATH = "data/raw_cardekho_cars.csv"
DB_PATH = "database/cars.db"
PROCESSED_CSV_PATH = "data/processed/cleaned_cars.csv"
PROCESSED_EXCEL_PATH = "data/processed/cleaned_cars.xlsx"


def clean_price(price):
    if pd.isna(price):
        return None

    price = str(price).replace("₹", "").replace(",", "").strip()

    value = re.findall(r"[\d.]+", price)

    if not value:
        return None

    value = float(value[0])

    if "Lakh" in price:
        return value * 100000

    if "Crore" in price:
        return value * 10000000

    return value


def clean_km(km):
    if pd.isna(km):
        return None

    km = str(km).replace(",", "").replace("kms", "").replace("km", "").strip()

    value = re.findall(r"[\d.]+", km)

    if not value:
        return None

    return float(value[0])


def extract_year(name):
    if pd.isna(name):
        return None

    match = re.search(r"\b(19|20)\d{2}\b", str(name))

    if match:
        return int(match.group())

    return None


def extract_brand(name):
    if pd.isna(name):
        return "Unknown"

    name = str(name).strip()

    # Remove year from car name
    name = re.sub(r"\b(19|20)\d{2}\b", "", name).strip()

    if not name:
        return "Unknown"

    # Handle multi-word brands first
    multi_word_brands = [
        "Mercedes-Benz",
        "Land Rover",
        "Maruti Suzuki"
    ]

    for brand in multi_word_brands:
        if name.lower().startswith(brand.lower()):
            return brand

    # Otherwise return first word as brand
    parts = name.split()

    if len(parts) == 0:
        return "Unknown"

    return parts[0]


def clean_car_data():
    # Check raw data file
    if not os.path.exists(RAW_DATA_PATH):
        print("Raw data file not found. Run scraper first.")
        return

    # Read raw CSV
    df = pd.read_csv(RAW_DATA_PATH)

    # Clean columns
    df["price"] = df["price"].apply(clean_price)
    df["km_driven"] = df["km_driven"].apply(clean_km)
    df["year"] = df["name"].apply(extract_year)
    df["brand"] = df["name"].apply(extract_brand)

    # Fill missing values
    df["location"] = df["location"].fillna("Unknown")
    df["fuel_type"] = df["fuel_type"].fillna("Unknown")
    df["transmission"] = df["transmission"].fillna("Unknown")
    df["url"] = df["url"].fillna("")

    # Remove rows where important cleaned values are missing
    df = df.dropna(subset=["price", "km_driven"])

    df = df.drop_duplicates(
        subset=["name", "price", "km_driven", "location", "url"],
        keep="first"
    )

    # Create required folders
    os.makedirs("database", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    # Save cleaned data to CSV and Excel
    df.to_csv(PROCESSED_CSV_PATH, index=False)
    df.to_excel(PROCESSED_EXCEL_PATH, index=False)

    # Save cleaned data to SQLite database
    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql(
            "cars",
            conn,
            if_exists="replace",
            index=False
        )

    print("Data cleaned and saved successfully.")
    print(f"SQLite database saved to: {DB_PATH}")
    print(f"Cleaned CSV saved to: {PROCESSED_CSV_PATH}")
    print(f"Cleaned Excel saved to: {PROCESSED_EXCEL_PATH}")
    print(f"Total records saved: {len(df)}")


if __name__ == "__main__":
    clean_car_data()