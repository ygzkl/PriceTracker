import requests
from bs4 import BeautifulSoup
import sqlite3
import re

# Function that adds or updates product and price in the database
def add_or_update_product_and_price(product_id, product_name, price, url):
    conn = sqlite3.connect('products.db', timeout=10)
    cursor = conn.cursor()

    try:
        # Check if product already exists in the Products table
        cursor.execute("SELECT product_id FROM Products WHERE product_id = ?", (product_id,))
        result = cursor.fetchone()

        if not result:
            cursor.execute("INSERT INTO Products (product_id, product_name, product_url) VALUES (?, ?, ?)", 
                           (product_id, product_name, url))
            print(f"Added new product: {product_name} (ID: {product_id})")
            cursor.execute("INSERT INTO Prices (product_id, price) VALUES (?, ?)", 
                       (product_id, price))
                   
        else:
            cursor.execute("UPDATE Products SET product_name = ? WHERE product_id = ?", (product_name, product_id))
            cursor.execute("INSERT INTO Prices (product_id, price) VALUES (?, ?)", (product_id, price))
        conn.commit()
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
    finally:
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
    
    # Extract product name
    product_title = soup.find(id='productTitle')
    if product_title:
        product_name = product_title.text.strip()
    else:
        product_name = "Error: Product title not found"
    
    # Extract product price
    price_element = soup.find('span', class_='a-price-whole')
    if price_element:
        whole_price = price_element.text.strip().replace('.', '').replace(',', '')
        fraction_element = soup.find('span', class_='a-price-fraction')
        fraction_price = fraction_element.text.strip() if fraction_element else '00'
        
        price = float(f"{whole_price}.{fraction_price}")
    else:
        price = None

    # Extract product ID from the URL
    match = re.search(r'/dp/([A-Za-z0-9]+)', url)
    if match:
        product_id = match.group(1)
    else:
        return "Error: Unable to extract product ID from the URL."

    # Save the product and price to the database if the price is found
    if price:
        add_or_update_product_and_price(product_id, product_name, price, url)
        return f"Product: {product_name}\nPrice: {price}\nProduct ID: {product_id}"
    else:
        return "Error: Price not found, not saved to the database."

