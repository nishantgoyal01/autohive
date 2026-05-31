# AutoHive 🚗📊

AutoHive is a Python-based web scraping and data analytics project that extracts public used-car listing data, cleans and stores it, and visualizes meaningful market insights through an interactive Streamlit dashboard.

This project is designed to demonstrate practical skills in web scraping, browser automation, HTML parsing, data cleaning, structured storage, and dashboard development.

---

## 🎯 Project Objective

The main objective of AutoHive is to build an end-to-end data extraction and analytics pipeline for used-car marketplace data. 

The system collects publicly available car listing details such as car name, year, price, kilometers driven, fuel type, transmission, location, and listing URL. The scraped data is then cleaned, stored, and analyzed to generate useful insights such as average price trends, inventory distribution, fuel-type patterns, and price comparison based on kilometers driven.

---

## ✨ Features

* **Static Web Scraping:** Using BeautifulSoup & Requests.
* **Dynamic Web Scraping:** Using Playwright browser automation.
* **HTML Parsing:** Structured data extraction using CSS selectors.
* **Data Pipeline:** Continuous handling of public used-car listings.
* **Data Preprocessing:** Robust cleaning, duplicate record removal, missing value handling, and normalization (prices/kilometers) via Pandas & NumPy.
* **Structured Storage:** Cleaned data storage in an SQLite database, with multi-format exports (CSV, Excel).
* **Interactive Dashboard:** Streamlit-based analytics platform featuring dynamic Plotly visualizations.
* **Ethical Practices:** Implemented rate limiting and respectful scraping logic.

---

## 🛠️ Tech Stack

| Category | Technologies |
| :--- | :--- |
| **Programming Language** | Python |
| **Web Scraping** | BeautifulSoup, Playwright, Requests |
| **Data Processing** | Pandas, NumPy |
| **Data Storage** | SQLite, CSV, Excel |
| **Dashboard** | Streamlit, Plotly |
| **Data Format** | JSON, CSV, XLSX |
| **Development Tools** | VS Code, Git, GitHub |
| **Automation** | Browser Automation, Pagination Handling |

---

## 📂 Project Folder Structure

```text
autohive/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   │   └── raw_cars.csv
│   │
│   └── processed/
│       ├── cleaned_cars.csv
│       └── cleaned_cars.xlsx
│
├── scraper/
│   ├── scrape_static.py
│   ├── scrape_dynamic.py
│   ├── parser.py
│   └── utils.py
│
├── analytics/
│   ├── clean_data.py
│   └── price_analysis.py
│
├── database/
│   ├── db.py
│   └── cars.db
│
├── dashboard/
│   └── app.py
│
└── reports/
    ├── sample_output.csv
    └── insights.md