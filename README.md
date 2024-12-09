# PriceTracker

**PriceTracker** is a tool designed to monitor and track price changes for Amazon products. By scraping product details such as name, price, and product ID from Amazon.com.tr URLs, it helps users stay informed of price fluctuations. The tool stores this data in a local SQLite database and sends email notifications when the price of a tracked product drops, ensuring users never miss a price change.


## Features

- Scrapes product data (name, price, product ID) from Amazon.com.tr URLs.
- Stores product data locally in an SQLite database and tracks price changes.
- Email notifications with SMTP when the price of a tracked product drops.
- User-friendly interface built with Tkinter, allowing users to easily input product links, view existing products, and check the status of price tracking. The interface provides fields for entering a product URL and user email, as well as buttons for adding new products and viewing product data with price history.


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

4. Run the price_update.py to start tracking Amazon products and update existing ones
```bash
python price_update.py
```

5. Run the get_info.py script to collect user email and product URL. This script allows adding new products and showing existing products along with their last 10 prices.
```bash
python get_info.py
```

![add_user-2](https://github.com/user-attachments/assets/d5015f55-f3e4-4e8c-b90d-d551a8f16d64)
*This step allows you to add new products by entering the user email and product URL.*

![graph](https://github.com/user-attachments/assets/47414be3-e82c-499d-837a-595ff34c79dc)
*Here, you can view existing products along with their last 10 prices, displayed in a graph.*


## Additional Notes
* The get_info.py script can be run at any time to collect a new product URL and user email, but it does not need to run continuously.
* The price_update.py script must be running continuously in the background to track and update product prices. Without it running, the application will not be able to fetch updated product prices.
* The email notifications feature will notify you when a price change is detected for the products you are tracking.
* If you need further customization or run into any issues, feel free to open an issue in the GitHub repository.