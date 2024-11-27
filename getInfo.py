import sqlite3

def add_user():
    email = input("Please enter your email: ")
    product_url = input("Please enter the product URL: ")
    
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    
    # Add user to the Users table
    cursor.execute("INSERT INTO Users (email, product_url) VALUES (?, ?)", (email, product_url))
    
    # If the product doesn't exist in the Products table, add it
    cursor.execute("SELECT product_id FROM Products WHERE product_url = ?", (product_url,))
    if not cursor.fetchone():
        product_id = product_url.split("/dp/")[-1].split("/")[0]
        cursor.execute("INSERT OR IGNORE INTO Products (product_id, product_name, product_url) VALUES (?, ?, ?)", 
                       (product_id, "Unknown Product", product_url))
    
    conn.commit()
    conn.close()
    print(f"User with email {email} and product URL {product_url} has been added.")

# Add user to the database
add_user()
