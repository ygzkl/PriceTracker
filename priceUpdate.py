import os
import sqlite3
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from scraper import get_product_details

def send_email(to_email, subject, body):
    from_email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")

    # SMTP server setup
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(from_email, password)

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))
    
    # Send the email
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()
    print(f"Email sent to {to_email}")

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
            
            # Update the product name, price and product ID
            
            product_id = product_details.split("\n")[2].replace("Product ID: ", "")
            
            cursor.execute("SELECT price FROM Prices WHERE product_id = ? ORDER BY date DESC LIMIT 1", (product_id,))
            last_price = cursor.fetchone()

            product_name = product_details.split("\n")[0].replace("Product: ", "")
            price = product_details.split("\n")[1].replace("Price: ", "").replace(" TL", "")

            if last_price:
                last_price = last_price[0]
                if float(last_price) != float(price):
                    print(f"Price changed for {product_name}:\n\n")
                    
                    # Save the last price to the Prices table
                    cursor.execute("INSERT INTO Prices (product_id, price) VALUES (?, ?)", (product_id, price))
                    conn.commit()

                    # Send email to users who are tracking this product
                    cursor.execute("SELECT email FROM Users WHERE product_url = ?", (product_url,))
                    users = cursor.fetchall()
                    for user in users:
                        user_email = user[0]
                        subject = f"Price Update for {product_name}\n\n"
                        body = f"The price for '{product_name}' has changed to {price} TL.\n\nCheck the product at {product_url}."
                        send_email(user_email, subject, body)
                else:
                    print(f"No price change for {product_name} (ID: {product_id})")
            else:
                # Add first price to the Prices table
                cursor.execute("INSERT INTO Prices (product_id, price) VALUES (?, ?)", (product_id, price))
                conn.commit()
            
        except Exception as e:
            print(f"Error updating product {product_url}: {e}")
    
    conn.close()

while True:
    update_all_products()
    print("All products updated. Waiting for the next update...")
    time.sleep(40)  # Update every 40 seconds
