from flask import Flask, jsonify, request, render_template
import json
import requests
from bs4 import BeautifulSoup
from flask_caching import Cache

app = Flask(__name__, static_folder="static", template_folder="templates")

cache = Cache(app, config={"CACHE_TYPE": "simple"})

BASE_URL = "https://oda.com/no/products/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

session = requests.Session()

def scrape_product(product_id):
    url = f"{BASE_URL}{product_id}/"

    cached_data = cache.get(url)
    if cached_data:
        return cached_data

    response = session.get(url, headers=HEADERS)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    
    product_name = soup.find("title").text.strip() if soup.find("title") else "Unknown Product"
    price, image_url, brand = "N/A", "N/A", "Unknown"
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

    product_data = {
        "product_id": product_id,
        "name": product_name,
        "price": price,
        "image_url": image_url,
        "brand": brand,
        "categories": categories
    }

    cache.set(url, product_data, timeout=3600)

    return product_data


# Serve HTML via Flask
@app.route("/")
def home():
    return render_template("index.html")

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

@app.route("/product/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = scrape_product(product_id)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
