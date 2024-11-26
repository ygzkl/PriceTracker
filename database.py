import sqlite3
from datetime import datetime

def create_db():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    # Create Products table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Products (
                        product_id TEXT PRIMARY KEY,
                        product_name TEXT,
                        product_url TEXT UNIQUE)''')
    
    # Create Prices table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Prices (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        product_id TEXT,
                        price REAL,
                        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE)''')
    
    conn.commit()
    conn.close()

# Insert product details into the database
create_db()
