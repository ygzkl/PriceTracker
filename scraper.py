import requests
from bs4 import BeautifulSoup
import sqlite3
import re

# Function that adds or updates product and price in the database
def add_or_update_product_and_price(product_id, product_name, price):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    # Add product to the Products table if it doesn't exist
    cursor.execute("SELECT product_id FROM Products WHERE product_id = ?", (product_id,))
    result = cursor.fetchone()

    if result:
        product_id_in_db = result[0]
    else:
        # If the product doesn't exist, add it to the Products table
        cursor.execute("INSERT INTO Products (product_id, product_name, product_url) VALUES (?, ?, ?)", 
                       (product_id, product_name, url))
        conn.commit()
        product_id_in_db = product_id  # Use the URL's product_id as the primary key

    # Add the price to the Prices table
    cursor.execute("INSERT INTO Prices (product_id, price) VALUES (?, ?)", 
                   (product_id_in_db, price))
    conn.commit()

    print(f"Product '{product_name}' with price {price} has been added/updated.")

    conn.close()

# Function that fetches product details from the URL
def get_product_details(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return f"Error: Unable to fetch the webpage (Status code: {response.status_code})"
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Name of the product
    product_title = soup.find(id='productTitle')
    if product_title:
        product_name = product_title.text.strip()
    else:
        product_name = "Error: Product title not found"
    
    # Price of the product
    price_element = soup.find('span', class_='a-price-whole')
    if price_element:
        whole_price = price_element.text.strip()
        fraction_element = soup.find('span', class_='a-price-fraction')
        if fraction_element:
            fraction_price = fraction_element.text.strip()
            currency_element = soup.find('span', class_='a-price-symbol')
            currency = currency_element.text.strip() if currency_element else ''
            price = f"{whole_price}{fraction_price} {currency}"
        else:
            price = None 
    else:
        price = None 

    # Get product ID from the URL
    match = re.search(r'/dp/([A-Za-z0-9]+)', url)
    if match:
        product_id = match.group(1) 
    else:
        return "Error: Unable to extract product ID from the URL."

    # Save the product and price to the database if the price is found
    if price:
        add_or_update_product_and_price(product_id, product_name, price)
        return f"Product: {product_name}\nPrice: {price}\nProduct ID: {product_id}"
    else:
        return "Error: Price not found, not saved to the database."

# Get the product URL from the user
url = input("Please enter the product URL: ")
product_details = get_product_details(url)
print(product_details)
