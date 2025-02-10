from flask import Flask, jsonify, request, render_template
import json
import requests
from bs4 import BeautifulSoup
from flask_caching import Cache

app = Flask(__name__, static_folder="static", template_folder="templates")

# Enable caching for improved speed
cache = Cache(app, config={"CACHE_TYPE": "simple"})

BASE_URL = "https://oda.com/no/products/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# Create a session for requests
session = requests.Session()

# Scrape a product
def scrape_product(product_id):
    url = f"{BASE_URL}{product_id}/"

    # Check cache first
    cached_data = cache.get(url)
    if cached_data:
        return cached_data

    # If not nil
    response = session.get(url, headers=HEADERS)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract name of the product

    product_name = soup.find("title").text.strip() if soup.find("title") else "Unknown Product"
    
    # Set default values for product properties
    price, image_url, brand = "N/A", "N/A", "Unknown"
    
    # Scrape Product properties
    script_tag = soup.find("script", type="application/ld+json")
    if script_tag:
        try:
            product_data = json.loads(script_tag.string)
            price = product_data.get("offers", {}).get("price", "N/A")
            image_url = product_data.get("image", [])[0] if "image" in product_data else "N/A"
            brand = product_data.get("brand", "Unknown")
        except json.JSONDecodeError:
            pass

    # Extract categories from breadcrumbs
    categories = []
    breadcrumb_scripts = soup.find_all("script", type="application/ld+json")
    for script in breadcrumb_scripts:
        try:
            data = json.loads(script.string)
            if data.get("@type") == "BreadcrumbList":
                categories = [item["name"] for item in data["itemListElement"][:-1]]
                break
        except json.JSONDecodeError:
            pass

    # Set product data
    product_data = {
        "product_id": product_id,
        "name": product_name,
        "price": price,
        "image_url": image_url,
        "brand": brand,
        "categories": categories
    }

    # Cache the result to speed up future requests
    cache.set(url, product_data, timeout=3600)

    return product_data


# Serve HTML via Flask
@app.route("/")
def home():
    return render_template("index.html")

# Serve API to search products
@app.route("/products", methods=["GET"])
def get_products():
    start_id = int(request.args.get("start", 1))
    end_id = int(request.args.get("end", 10))

    products = []
    for product_id in range(start_id, end_id + 1):
        product = scrape_product(product_id)
        if product:
            products.append(product)

    return jsonify(products)

# Serve API to get individual product via product ID
@app.route("/product/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = scrape_product(product_id)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

# TODO: Add API to search via product name

if __name__ == "__main__":
    app.run(debug=True)
