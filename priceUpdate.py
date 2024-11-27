import sqlite3
import time
from scraper import get_product_details

def update_all_products():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    # Get all product URLs from the database
    cursor.execute("SELECT product_url FROM Products")
    products = cursor.fetchall()

    for product in products:
        product_url = product[0]
        print(f"Updating product: {product_url}")
        try:
            product_details = get_product_details(product_url)
            print(product_details)
        except Exception as e:
            print(f"Error updating product {product_url}: {e}")
    
    conn.close()

while True:
    update_all_products()
    print("All products updated. Waiting for the next update...")
    time.sleep(10)
