# 🛍️ Oda Product Scraper & Web App  

A **Flask-based web application** that scrapes product details dynamically from **Oda.com** and displays them using a **JavaScript-powered frontend** with pagination & search functionality.

![Oda Product Scraper]()  

---

## 🚀 Features  
- ✅ **Dynamic Scraping** – Fetches product details in real-time.  
- ✅ **REST API** – Get product lists & single product details as JSON.  
- ✅ **Pagination** – Browse products in pages of 10.  
- ✅ **Search by ID** – Find any product instantly.  
- ✅ **Interactive UI** – Built with HTML, CSS & JavaScript.  

---

## 📂 Folder Structure  
```
📂 Web_Crawler_and_Product_Scraper/
│── 📂 static/             # Stores CSS & JS files
│   │── 📜 styles.css      # Frontend styles
│   │── 📜 script.js       # Handles API calls & pagination
│
│── 📂 templates/          # Stores HTML files (Flask default)
│   │── 📜 index.html      # Main frontend page
│
│── 📜 server.py           # Flask backend for API & scraping
│── 📜 requirements.txt    # Dependencies list
│── 📜 README.md           # Documentation
```

---

## 🛠️ Installation & Setup  

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/amarnathjamale/Web_Crawler_and_Product_Scraper.git
cd Web_Crawler_and_Product_Scraper
```

### **2️⃣ Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **3️⃣ Run the Flask Server**  
```bash
python server.py
```

### **4️⃣ Open in Browser**  
🔗 [http://127.0.0.1:5000/](http://127.0.0.1:5000/)  

---

## 🔥 API Endpoints  

### **1️⃣ Fetch Multiple Products (with pagination)**  
📌 **GET** `/products?start=1&end=10`  
🔗 Example:  
```
http://127.0.0.1:5000/products?start=1&end=10
```
📤 **Response:**  
```json
{
    "products": [
        {
            "product_id": 1,
            "name": "Sprett Yoghurt Skogsbær",
            "price": "25.90 NOK",
            "image_url": "https://image-url.com",
            "brand": "Tine",
            "categories": ["Beverages", "Dairy"]
        },
        {
            "product_id": 2,
            "name": "Pepsi Max 1.5L",
            "price": "19.90 NOK",
            "image_url": "https://image-url.com",
            "brand": "Pepsi",
            "categories": ["Beverages", "Soft Drinks"]
        }
    ]
}
```

---

### **2️⃣ Fetch a Single Product by ID**  
📌 **GET** `/product/<product_id>`  
🔗 Example:  
```
http://127.0.0.1:5000/product/1
```
📤 **Response:**  
```json
{
    "product_id": 1,
    "name": "Sprett Yoghurt Skogsbær",
    "price": "25.90 NOK",
    "image_url": "https://image-url.com",
    "brand": "Tine",
    "categories": ["Beverages", "Dairy"]
}
```

---

## 🎨 Frontend Features  

- **Pagination**: Automatically loads products in pages of 10.  
- **Search**: Enter a **Product ID** to fetch its details instantly.  
- **Dynamic Loading**: Data is fetched from Flask API using **AJAX**.

---

## 💻 Tech Stack  

| Technology   | Description |
|-------------|------------|
| **Python**  | Flask API & Web Scraper |
| **HTML/CSS** | Frontend Structure & Styling |
| **JavaScript** | Handles API calls & pagination |
| **BeautifulSoup** | Extracts product data from Oda.com |

---

## 📝 License  
This project is **open-source**. Feel free to modify & improve it! 🚀  

👨‍💻 **Developed by:** *Amarnath Jamale*  

📧 **Contact:** [amar@jamale.org](mailto:amar@jamale.org)  

🌟 **If you found this useful, give it a star on GitHub!** ⭐

