import requests
from bs4 import BeautifulSoup
import os
import urllib.request
from tqdm import tqdm
import csv


# URL of the category page
url = 'https://www.coupang.com/np/categories/186764'

# Send a request to the URL and get the response
response = requests.get(url)

# Parse the response using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Extract the category name
category_name = soup.find('h2', {'class': 'search-category-filter-title'}).text.strip()

# Create a directory with the category name
if not os.path.exists(category_name):
    os.makedirs(category_name)

#Saving in CSV
def create_csv(data):
    with open('products.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['post_title', 'post_content', 'post_status', 'post_type', 'sku', 'regular_price', 'sale_price', 'category'])
        for product in data:
            title = product['title']
            description = product['description']
            price = product['price']
            sale_price = product['sale_price']
            category = product['category']
            image_url = product['image_url']
            sku = product['sku']
            writer.writerow([title, description, 'publish', 'product', sku, price, sale_price, category])

# Find all the product links on the page
product_links = soup.find_all('a', {'class': 'search-product-link'})

# Create a progress bar with the total number of products to download
progress_bar = tqdm(total=len(product_links), desc="Downloading Products")

# Download each product and save it in the category directory
for index, product_link in enumerate(product_links):
    # Create a progress bar with the total number of images to download
    image_progress_bar = tqdm(total=len(images), desc=f"Parsing... {product_name}")
    # Get the product URL
    product_url = 'https://www.coupang.com' + product_link['href']

    # Send a request to the product URL and get the response
    product_response = requests.get(product_url)

    # Parse the response using BeautifulSoup
    product_soup = BeautifulSoup(product_response.text, 'html.parser')

    # Extract the product details
    product_name = product_soup.find('h2', {'class': 'prod-buy-header__title'}).text.strip()
    product_price = product_soup.find('span', {'class': 'total-price'}).text.strip()

    # Create a directory with the product name
    product_directory = f"{category_name}/{product_name}"
    if not os.path.exists(product_directory):
        os.makedirs(product_directory)

    # Find all the images on the product page
    images = product_soup.find_all('img')

    

    # Download each image and save it in the product directory
    for image_index, image in enumerate(images):
        # Get the image URL
        image_url = image['src']

        # Get the image extension (jpg, png, etc.)
        image_extension = image_url.split('.')[-1]

        # Save the image with a unique name
        image_filename = f"{product_directory}/image_{image_index+1}.{image_extension}"

        # Download the image and update the progress bar
        urllib.request.urlretrieve(image_url, image_filename, reporthook=lambda *args: image_progress_bar.update())

    # Close the image progress bar
    image_progress_bar.close()

    # Save the product details in a file
    with open(f"{product_directory}/details.txt", 'w') as file:
        file.write(f"Name: {product_name}\n")
        file.write(f"Price: {product_price}\n")
        file.write(f"URL: {product_url}\n")

    # Update the progress bar
    progress_bar.update()

# Close the progress bar
progress_bar.close()

