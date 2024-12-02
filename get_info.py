import sqlite3
import tkinter as tk
from tkinter import messagebox

def add_user():
    email = email_entry.get()
    product_url = product_url_entry.get()

    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    # Add user to Users table
    cursor.execute("INSERT INTO Users (email, product_url) VALUES (?, ?)", (email, product_url))

    # If the product doesn't exist, add it to Products table
    cursor.execute("SELECT product_id FROM Products WHERE product_url = ?", (product_url,))
    if not cursor.fetchone():
        product_id = product_url.split("/dp/")[-1].split("/")[0]
        cursor.execute("INSERT OR IGNORE INTO Products (product_id, product_name, product_url) VALUES (?, ?, ?)",
                       (product_id, "Unknown Product", product_url))

    conn.commit()
    conn.close()

    messagebox.showinfo("Success", f"User with email {email} has been added.")

    # Clear the input fields after successful submission
    email_entry.delete(0, tk.END)
    product_url_entry.delete(0, tk.END)

def show_products():
    # Create a new window
    product_window = tk.Toplevel(root)
    product_window.title("Product List")

    # Create a listbox to display products
    product_listbox = tk.Listbox(product_window, width=50, height=10)
    product_listbox.pack(padx=10, pady=10)

    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    # SQL query to get the latest price for each product
    cursor.execute('''SELECT p.product_name, pr.price 
                      FROM Products p
                      LEFT JOIN Prices pr ON p.product_id = pr.product_id
                      WHERE pr.date = (SELECT MAX(date) FROM Prices WHERE product_id = p.product_id)''')
    products = cursor.fetchall()
    
    # Insert product names and the latest price into the listbox
    for product in products:
        product_listbox.insert(tk.END, f"Product: {product[0]} | Price: {product[1]}")

    conn.close()

# Create main GUI
root = tk.Tk()
root.title("Add User")

# Email input
tk.Label(root, text="Email:").grid(row=0, column=0, padx=10, pady=10)
email_entry = tk.Entry(root, width=30)
email_entry.grid(row=0, column=1, padx=10, pady=10)

# Product URL input
tk.Label(root, text="Product URL:").grid(row=1, column=0, padx=10, pady=10)
product_url_entry = tk.Entry(root, width=30)
product_url_entry.grid(row=1, column=1, padx=10, pady=10)

# Add User button
tk.Button(root, text="Add User", command=add_user).grid(row=2, column=0, columnspan=2, pady=20)

# Show Products button
tk.Button(root, text="Show Products", command=show_products).grid(row=3, column=0, columnspan=2, pady=20)

root.mainloop()
