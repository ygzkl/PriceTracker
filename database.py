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

    # Create Users table to store email and product association
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT,
                        product_url TEXT,
                        FOREIGN KEY (product_url) REFERENCES Products(product_url) ON DELETE CASCADE)''')
    
    conn.commit()
    conn.close()

create_db()
