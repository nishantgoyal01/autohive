import sqlite3
import pandas as pd


DB_PATH = "database/cars.db"


def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM cars", conn)
    conn.close()
    return df


def generate_insights():
    df = load_data()

    insights = []

    insights.append(f"Total cars scraped: {len(df)}")

    if "price" in df.columns:
        insights.append(f"Average car price: ₹{df['price'].mean():,.0f}")
        insights.append(f"Lowest car price: ₹{df['price'].min():,.0f}")
        insights.append(f"Highest car price: ₹{df['price'].max():,.0f}")

    if "brand" in df.columns:
        top_brand = df["brand"].value_counts().idxmax()
        insights.append(f"Most common brand: {top_brand}")

    with open("reports/insights.md", "w", encoding="utf-8") as file:
        file.write("# AutoMarket Intelligence Insights\n\n")

        for insight in insights:
            file.write(f"- {insight}\n")

    print("Insights generated successfully.")


if __name__ == "__main__":
    generate_insights()