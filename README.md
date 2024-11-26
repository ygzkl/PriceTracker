# PriceTracker

**PriceTracker** is a price monitoring tool specifically designed for Amazon products. It helps users track product prices by scraping product details such as names, prices, and IDs from Amazon URLs. The application stores this data in a database and monitors price changes over time. 

## Features

- Scrapes product data (name, price, product ID) from Amazon URLs.
- Stores the data in a database and tracks price changes.
- Simple user interface (coming soon) for users to input product links.
- Email notifications when the price of a tracked product drops.


1. Clone this project to your computer
```bash
git clone https://github.com/username/PriceTracker.git
cd PriceTracker
```

2. Install the required dependencies
```bash
pip install -r requirements.txt
```

3. Run the database setup script to create a local database
```bash
python database.py
```

4. Run the scraper and start tracking Amazon products:
```bash
python scraper.py
```