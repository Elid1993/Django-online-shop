// ------------------ CSRF Helper ------------------
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie("csrftoken");

// ------------------ Detect Base URL ------------------
let BASE_URL = window.location.origin;  
// یعنی اگر روی لوکال باشی میشه http://127.0.0.1:8000
// و اگر روی pythonanywhere باشی میشه https://a1368e.pythonanywhere.com

const API_CART = BASE_URL + "/api/cart/";
const API_ORDER = BASE_URL + "/api/orders/";

// ------------------ Add Item ------------------
function addToCart(productId) {
    console.log(" ارسال درخوایت به", API_CART + "add_item/");
    fetch(API_CART + "add_item/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: 1
        }),
    })
    .then(res => {
        if (!res.ok) {
            return res.json().then(err => { throw err; });
        }
        return res.json();
    })
    .then(data => {
        alert("✅ محصول اضافه شد به سبد!");
        loadCart();
    })
    .catch(err => {
        console.error("❌ خطا در افزودن:", err);
        alert("❌ خطا در افزودن: " + (err.detail || "مشکل ناشناخته"));
    });
}

// ------------------ Remove Item ------------------
function removeFromCart(productId) {
    fetch(API_CART + "remove_item/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ product_id: productId }),
    })
    .then(res => res.json())
    .then(data => {
        alert("🗑️ محصول حذف شد!");
        loadCart();
    })
    .catch(err => {
        console.error("❌ خطا در حذف:", err);
        alert("❌ خطا در حذف محصول!");
    });
}

// ------------------ Clear Cart ------------------
function clearCart() {
    fetch(API_CART + "clear_cart/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
    })
    .then(res => res.json())
    .then(data => {
        alert("🛒 سبد خرید خالی شد!");
        loadCart();
    })
    .catch(err => {
        console.error("❌ خطا در خالی کردن:", err);
        alert("❌ خطا در خالی کردن سبد!");
    });
}

// ------------------ Checkout ------------------
function checkout() {
    fetch(API_ORDER, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
    })
    .then(res => {
        if (!res.ok) {
            return res.json().then(err => { throw err; });
        }
        return res.json();
    })
    .then(data => {
        alert("✅ سفارش شما ثبت شد! شماره سفارش: " + data.id);
        loadCart();
    })
    .catch(err => {
        console.error("❌ خطا در تسویه حساب:", err);
        alert("❌ خطا در ثبت سفارش: " + (err.detail || "مشکل ناشناخته"));
    });
}

// ------------------ Load Cart ------------------
function loadCart() {
    fetch(API_CART, {
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
    })
    .then(res => res.json())
    .then(data => {
        const container = document.getElementById("cart-items");
        container.innerHTML = "";
        if (data.items && data.items.length > 0) {
            data.items.forEach(item => {
                container.innerHTML += `
                    <div class="col-md-4">
                        <div class="card p-3 shadow-sm">
                            <h5>${item.product.name}</h5>
                            <p>تعداد: ${item.quantity}</p>
                            <p>قیمت: ${item.product.price} تومان</p>
                            <button class="btn btn-sm btn-danger" onclick="removeFromCart(${item.product.id})">حذف</button>
                        </div>
                    </div>
                `;
            });
        } else {
            container.innerHTML = "<p class='text-center'>🛍️ سبد خرید شما خالی است.</p>";
        }
    });
}

// ------------------ Init ------------------
document.addEventListener("DOMContentLoaded", loadCart);
