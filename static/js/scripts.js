/*!
* Start Bootstrap - Shop Homepage v5.0.6 (https://startbootstrap.com/template/shop-homepage)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project
// alert("hello java");

// آدرس‌های API
const API_CART = "http://localhost:8000/api/orders/cart/";
const API_ORDER = "http://localhost:8000/api/orders/checkout/";

// 🟢 افزودن محصول به سبد
function addToCart(productId) {
    fetch(API_CART + "add_item/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: 1
        })
    })
    .then(res => {
        if (!res.ok) throw new Error("خطا در افزودن محصول");
        return res.json();
    })
    .then(data => {
        alert("✅ محصول اضافه شد!");
        loadCart();
    })
    .catch(err => alert("❌ خطا در افزودن محصول!"));
}

// 🔴 حذف یک محصول خاص
function removeFromCart(productId) {
    fetch(API_CART + "remove_item/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({ product_id: productId })
    })
    .then(res => res.json())
    .then(data => {
        alert("🗑️ محصول حذف شد!");
        loadCart();
    })
    .catch(err => alert("❌ خطا در حذف محصول!"));
}

// 🟡 خالی کردن کل سبد
function clearCart() {
    fetch(API_CART + "clear_cart/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        }
    })
    .then(res => res.json())
    .then(data => {
        alert("🛒 سبد خرید خالی شد!");
        loadCart();
    })
    .catch(err => alert("❌ خطا در خالی کردن سبد!"));
}

// 💳 تسویه حساب (ثبت سفارش)
function checkout() {
    fetch(API_ORDER, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        }
    })
    .then(res => {
        if (!res.ok) throw new Error("خطا در تسویه حساب");
        return res.json();
    })
    .then(data => {
        alert("✅ سفارش شما با موفقیت ثبت شد! شماره سفارش: " + data.id);
        loadCart();
    })
    .catch(err => alert("❌ خطا در ثبت سفارش!"));
}

// 📦 نمایش آیتم‌های سبد خرید
function loadCart() {
    fetch(API_CART, {
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        }
    })
    .then(res => res.json())
    .then(data => {
        const container = document.getElementById("cart-items");
        if (!container) return; // اگر توی اون صفحه نبودیم
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

// 🛡 گرفتن CSRF Token از کوکی
function getCSRFToken() {
    let cookieValue = null;
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith("csrftoken=")) {
            cookieValue = cookie.substring("csrftoken=".length, cookie.length);
            break;
        }
    }
    return cookieValue;
}

// وقتی صفحه لود شد
document.addEventListener("DOMContentLoaded", loadCart);
