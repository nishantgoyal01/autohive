# AutoHive

**AutoHive** is a Python-based web scraping and data analytics project that extracts public used-car listing data, cleans and stores it, and visualizes meaningful market insights through an interactive Streamlit dashboard.

This project is designed to demonstrate practical skills in **web scraping, browser automation, HTML parsing, data cleaning, structured storage, and dashboard development**.

---

## Project Objective

The main objective of AutoHive is to build an end-to-end data extraction and analytics pipeline for used-car marketplace data.

The system collects publicly available car listing details such as car name, year, price, kilometers driven, fuel type, transmission, location, and listing URL. The scraped data is then cleaned, stored, and analyzed to generate useful insights such as average price trends, inventory distribution, fuel-type patterns, and price comparison based on kilometers driven.

Dashboard link: https://autohive-e76gdxkfa7rhaverjqhzyx.streamlit.app/

---

## Features

* Static web scraping using **BeautifulSoup**
* Dynamic web scraping using **Playwright**
* HTML parsing and structured data extraction
* Public used-car listing data collection
* Data cleaning and preprocessing using **Pandas**
* Duplicate record removal
* Missing value handling
* Price and kilometer normalization
* Cleaned data storage in **SQLite database**
* Cleaned data export to **CSV and Excel**
* Streamlit-based interactive analytics dashboard
* JSON/CSV/Excel-compatible data pipeline
* Rate limiting and ethical scraping practices

---

## Tech Stack

| Category             | Technologies                            |
| -------------------- | --------------------------------------- |
| Programming Language | Python                                  |
| Web Scraping         | BeautifulSoup, Playwright, Requests     |
| Data Processing      | Pandas, NumPy                           |
| Data Storage         | SQLite, CSV, Excel                      |
| Dashboard            | Streamlit, Plotly                       |
| Data Format          | JSON, CSV, XLSX                         |
| Development Tools    | VS Code, Git, GitHub                    |
| Automation           | Browser Automation, Pagination Handling |

---

## Project Folder Structure

```bash
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
```

---

## Folder Description

| Folder/File                   | Purpose                                                              |
| ----------------------------- | -------------------------------------------------------------------- |
| `scraper/`                    | Contains scripts for scraping static and dynamic car listing pages   |
| `scraper/scrape_static.py`    | Scrapes static HTML pages using Requests and BeautifulSoup           |
| `scraper/scrape_dynamic.py`   | Scrapes dynamic pages using Playwright browser automation            |
| `scraper/parser.py`           | Extracts structured fields from raw HTML                             |
| `scraper/utils.py`            | Helper functions for headers, delays, formatting, and reusable logic |
| `data/raw/`                   | Stores raw scraped data before cleaning                              |
| `data/processed/`             | Stores cleaned dashboard-ready data in CSV and Excel format          |
| `analytics/clean_data.py`     | Cleans raw scraped data and stores cleaned records                   |
| `analytics/price_analysis.py` | Performs pricing and market analysis                                 |
| `database/`                   | Stores SQLite database and database helper scripts                   |
| `dashboard/app.py`            | Streamlit dashboard for visualizing insights                         |
| `reports/`                    | Contains sample outputs and project insights                         |
| `requirements.txt`            | Python dependencies required to run the project                      |
| `.gitignore`                  | Files and folders ignored by Git                                     |

---

## Data Fields Extracted

AutoHive extracts and processes the following fields:

| Field          | Description                         |
| -------------- | ----------------------------------- |
| `name`         | Car name/model                      |
| `brand`        | Car brand                           |
| `year`         | Manufacturing year                  |
| `price`        | Listed price                        |
| `price_lakh`   | Price converted into lakhs          |
| `km_driven`    | Kilometers driven                   |
| `fuel_type`    | Petrol, Diesel, CNG, Electric, etc. |
| `transmission` | Manual or Automatic                 |
| `location`     | Listing city/location               |
| `owner_type`   | First owner, second owner, etc.     |
| `url`          | Source listing URL                  |
| `scraped_at`   | Timestamp of data extraction        |

---

## Data Pipeline

```text
Public Car Listings
        ↓
Web Scraping using BeautifulSoup / Playwright
        ↓
Raw Data Storage
        ↓
Data Cleaning using Pandas
        ↓
Cleaned Data Storage
        ↓
SQLite + CSV + Excel
        ↓
Streamlit Dashboard
        ↓
Market Insights
```

---

## Sample Insights Generated

AutoHive helps generate insights such as:

* Average used-car price by brand
* City-wise inventory distribution
* Fuel-type distribution
* Transmission-type distribution
* Price vs kilometers driven analysis
* Cheapest listings by model
* Most available car brands
* High-value and low-value listings
* Used-car depreciation pattern
* Budget-wise car availability

---

## Dashboard Features

The Streamlit dashboard includes:

* Total listings count
* Average car price
* Average kilometers driven
* Brand-wise price analysis
* Fuel-type distribution chart
* Transmission-type distribution chart
* Price distribution graph
* Price vs kilometers driven scatter plot
* City/location-wise inventory analysis
* Filter options by brand, fuel type, transmission, and budget
* Cleaned data preview table

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/nishantgoyal01/autohive.git
cd autohive
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
```

### 3. Activate Virtual Environment

For macOS/Linux:

```bash
source venv/bin/activate
```

For Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Install Playwright Browsers

```bash
playwright install
```

---

## How to Run the Project

Run the project in the following order:

### Step 1: Run the Scraper

```bash
python scraper/scrape_dynamic.py
```

This extracts public used-car listing data and stores raw data in:

```bash
data/raw/raw_cars.csv
```

### Step 2: Clean and Store the Data

```bash
python analytics/clean_data.py
```

This cleans the scraped data and stores it in:

```bash
database/cars.db
data/processed/cleaned_cars.csv
data/processed/cleaned_cars.xlsx
```

### Step 3: Run the Streamlit Dashboard

```bash
streamlit run dashboard/app.py
```

The dashboard will open in your browser at:

```bash
http://localhost:8501
```

---

## Required Dependencies

The following packages are inside `requirements.txt`:

```txt
beautifulsoup4
requests
playwright
pandas
numpy
streamlit
plotly
openpyxl
```

---

## Example Output

After running the cleaning script, the expected output may look like:

```bash
Data cleaned and saved to database/cars.db
Cleaned CSV saved to data/processed/cleaned_cars.csv
Cleaned Excel saved to data/processed/cleaned_cars.xlsx
Total records saved: 120
```

---

## Why Cleaned Data Storage Matters

AutoHive stores cleaned data instead of only raw scraped data. This makes the data directly usable for analysis, reporting, and dashboarding.

The cleaned data includes:

* Standardized prices
* Normalized kilometer values
* Removed duplicates
* Cleaned text fields
* Structured car attributes
* Dashboard-ready CSV and Excel files
* SQLite database storage for querying

---

## Ethical Scraping Practices

This project follows ethical scraping principles:

* Scrapes only publicly available data
* Avoids login-protected or private user information
* Uses rate limiting between requests
* Does not overload target servers
* Respects website terms and robots.txt wherever applicable
* Stores data only for educational and portfolio purposes

---

## Future Improvements

* Add Scrapy-based large-scale scraping pipeline
* Add automated scheduled scraping
* Add proxy and retry handling
* Add API-based data extraction where available
* Add advanced price prediction model
* Add car recommendation system
* Add anomaly detection for unusually low-priced listings
* Deploy dashboard on Streamlit Cloud
* Store historical price trends over time

---

## Project Relevance

This project demonstrates hands-on experience in:

* Python programming
* Web scraping
* Browser automation
* HTML and CSS selector usage
* APIs and JSON handling
* Data cleaning
* SQLite database storage
* CSV and Excel export
* Dashboard development
* Real-world automation workflow

AutoHive is especially relevant for web scraping and data automation roles because it shows the complete process from data extraction to cleaned storage and business insight generation.

---

## Snapshots

**Home Page**

<img width="1920" height="1589" alt="image" src="https://github.com/user-attachments/assets/b57905fb-6176-498d-8c75-a4222ed5c268" /><br>

**Brand Analytics**

<img width="1920" height="1148" alt="brandanalytics" src="https://github.com/user-attachments/assets/5ed8c7eb-fcda-4274-a492-e1776c651cc8" /><br>

**Market Insights**

<img width="1920" height="1683" alt="marketinsights" src="https://github.com/user-attachments/assets/4eb37509-edc4-4275-88cf-1c684f310791" /><br>

**Listings & Exports**

<img width="1920" height="1734" alt="listingnexports" src="https://github.com/user-attachments/assets/a58a36b0-9ab7-4063-99e8-89dca2173e9e" /><br>

---

## Author

**Nishant Goyal**\
B.Tech Computer Science and Engineering\
Email: [nishantgoyal010@gmail.com](mailto:nishantgoyal010@gmail.com)
