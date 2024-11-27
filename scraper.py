import requests
from bs4 import BeautifulSoup
import sqlite3
import re

# Function to add or update product and price in the database
def add_or_update_product_and_price(product_id, product_name, price, url):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    # Add product to the Products table if it doesn't exist
    cursor.execute("SELECT product_id FROM Products WHERE product_id = ?", (product_id,))
    result = cursor.fetchone()

    if not result:
        # If the product doesn't exist, add it to the Products table
        cursor.execute("INSERT INTO Products (product_id, product_name, product_url) VALUES (?, ?, ?)",
                       (product_id, product_name, url))
        conn.commit()

    # Add the price to the Prices table
    cursor.execute("INSERT INTO Prices (product_id, price) VALUES (?, ?)",
                   (product_id, price))
    conn.commit()

    conn.close()

# Function to fetch product details from the URL
def get_product_details(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return {"Error": f"Unable to fetch the webpage (Status code: {response.status_code})"}
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract product title
    product_title = soup.find(id='productTitle')
    product_name = product_title.text.strip() if product_title else "Error: Product title not found"
    
    # Extract product price
    price_element = soup.find('span', class_='a-price-whole')
    if price_element:
        whole_price = price_element.text.strip()
        fraction_element = soup.find('span', class_='a-price-fraction')
        fraction_price = fraction_element.text.strip() if fraction_element else "00"
        price = float(f"{whole_price}.{fraction_price}")
    else:
        price = None

    # Extract product ID from the URL
    match = re.search(r'/dp/([A-Za-z0-9]+)', url)
    product_id = match.group(1) if match else None

    if not product_id:
        return {"Error": "Unable to extract product ID from the URL."}

    if price is not None:
        add_or_update_product_and_price(product_id, product_name, price, url)
        return {"product_name": product_name, "price": price, "product_id": product_id}
    else:
        return {"Error": "Price not found"}
