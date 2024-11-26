import requests
from bs4 import BeautifulSoup

def get_product_details(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return f"Error: Unable to fetch the webpage (Status code: {response.status_code})"
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Product title
    product_title = soup.find(id='productTitle')
    if product_title:
        product_name = product_title.text.strip()
    else:
        product_name = "Error: Product title not found"
    
    # Product price
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
            price = "Error: Fraction part not found"
    else:
        price = "Error: Price not found"

    return f"Product: {product_name}\nPrice: {price}"

# Prompt user for URL input
url = input("Please enter the product URL: ")
product_details = get_product_details(url)
print(product_details)
