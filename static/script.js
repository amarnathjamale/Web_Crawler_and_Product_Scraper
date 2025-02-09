let products = [];
let currentPage = 1;
const itemsPerPage = 10;
const API_URL = "http://127.0.0.1:5000";

async function fetchProducts() {
    const start = (currentPage - 1) * itemsPerPage + 1;
    const end = start + itemsPerPage - 1;

    try {
        const response = await fetch(`${API_URL}/products?start=${start}&end=${end}`);
        products = await response.json();
        displayProducts();
    } catch (error) {
        console.error("Error fetching products:", error);
    }
}

function displayProducts() {
    const productContainer = document.getElementById("product-container");
    productContainer.innerHTML = ""; // Clear previous content

    products.forEach(product => {
        const productDiv = document.createElement("div");
        productDiv.classList.add("product");
        productDiv.innerHTML = `
            <h3>${product.name}</h3>
            <p><strong>Product ID:</strong> ${product.product_id}</p>
            <p><strong>Price:</strong> ${product.price}</p>
            <p><strong>Categories:</strong> ${product.categories.join(", ")}</p>
        `;
        productContainer.appendChild(productDiv);
    });

    updatePagination();
}

async function searchProduct() {
    const searchValue = document.getElementById("search-input").value.trim();
    if (!searchValue) {
        alert("Enter a Product ID!");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/product/${searchValue}`);
        const data = await response.json();

        document.getElementById("search-result").innerHTML = data.error
            ? `<p style="color: red;">Product Not Found!</p>`
            : `<div class="product"><h3>${data.name}</h3><p><strong>Price:</strong> ${data.price}</p></div>`;
    } catch (error) {
        console.error("Error searching product:", error);
    }
}

function updatePagination() {
    document.getElementById("page-info").innerText = `Page ${currentPage}`;
    document.getElementById("prev-btn").disabled = currentPage === 1;
}


document.getElementById("prev-btn").addEventListener("click", () => {
    if (currentPage > 1) {
        currentPage--;
        fetchProducts();
    }
});

document.getElementById("next-btn").addEventListener("click", () => {
    currentPage++;
    fetchProducts();
});

document.getElementById("search-btn").addEventListener("click", searchProduct);

// Load products on page load
fetchProducts();
