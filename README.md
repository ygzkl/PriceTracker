# PriceTracker

**PriceTracker** is a tool designed to monitor and track price changes for Amazon products. By scraping product details such as name, price, and product ID from Amazon.com.tr URLs, it helps users stay informed of price fluctuations. The tool stores this data in a local SQLite database and sends email notifications when the price of a tracked product drops, ensuring users never miss a price change.


## Features

- Scrapes product data (name, price, product ID) from Amazon.com.tr URLs.
- Stores product data locally in an SQLite database and tracks price changes.
- Email notifications when the price of a tracked product drops.
- Simple user interface (coming soon) for users to input product links.


## Installation

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

4. Runs the getInfo.py script to collect user email and product URL
```bash
python getInfo.py
```

5. Run the priceUpdate.py to start tracking Amazon products and update existing ones
```bash
python priceUpdate.py
```


## Additional Notes
* The get_info.py script can be run at any time to collect a new product URL and user email, but it does not need to run continuously.
* The price_update.py script must be running continuously in the background to track and update product prices. Without it running, the application will not be able to fetch updated product prices.
* The email notifications feature will notify you when a price change is detected for the products you are tracking.
* If you need further customization or run into any issues, feel free to open an issue in the GitHub repository.