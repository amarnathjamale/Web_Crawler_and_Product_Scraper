from flask import Flask, jsonify, request
import json
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

BASE_URL = "https://oda.com/no/products/"

def scrape_product(product_id):
    url = f"{BASE_URL}{product_id}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract product name
    product_name = soup.find("title").text.strip()

    # Extract price from JSON-LD metadata
    script_tag = soup.find("script", type="application/ld+json")
    if script_tag:
        try:
            product_data = json.loads(script_tag.string) 
            price = product_data.get("offers", {}).get("price", "N/A")
        except json.JSONDecodeError:
            price = "N/A"
    else:
        price = "N/A"

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

    return {
        "product_id": product_id,
        "name": product_name,
        "price": price,
        "categories": categories
    }

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

if __name__ == "__main__":
    app.run(debug=True)
