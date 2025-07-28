let cart = JSON.parse(localStorage.getItem('cart')) || [];

function formatPrice(price) {
  return price.toLocaleString('uz-UZ') + " so'm";
}

function saveCart() {
  localStorage.setItem('cart', JSON.stringify(cart));
}

function addToCart(name, price) {
  const existing = cart.find(item => item.name === name);
  if (existing) {
    existing.count += 1;
  } else {
    cart.push({ name, price, count: 1 });
  }
  saveCart();
  alert(`✅ ${name} savatga qo‘shildi!`);
}
