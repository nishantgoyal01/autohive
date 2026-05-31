import sqlite3
import pandas as pd


DB_PATH = "database/cars.db"


def create_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        brand TEXT,
        year INTEGER,
        price INTEGER,
        km_driven INTEGER,
        fuel_type TEXT,
        transmission TEXT,
        location TEXT,
        url TEXT,
        scraped_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_data(csv_file):
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_csv(csv_file)

    df_to_insert = pd.DataFrame({
        "name": df.get("name"),
        "brand": df.get("brand"),
        "year": df.get("year"),
        "price": df.get("clean_price"),
        "km_driven": df.get("clean_km_driven"),
        "fuel_type": df.get("fuel_type"),
        "transmission": df.get("transmission"),
        "location": df.get("location"),
        "url": df.get("url"),
        "scraped_at": df.get("scraped_at")
    })

    df_to_insert.to_sql(
        "cars",
        conn,
        if_exists="append",
        index=False
    )

    conn.close()

    print("Data inserted into SQLite database successfully.")


if __name__ == "__main__":
    create_table()
    insert_data("data/processed/cars_cleaned.csv")