document.addEventListener('DOMContentLoaded', () => {
    const cartCount = document.getElementById('cart-total');
    const searchBar = document.getElementById('search-bar');
    const searchButton = document.getElementById('search-button');
    const menuIcon = document.getElementById('menu-btn');
    const nav = document.querySelector('header nav');

    function updateCartCount() {
        const cart = JSON.parse(localStorage.getItem('cart')) || [];
        cartCount.textContent = cart.reduce((acc, item) => acc + item.quantity, 0);
    }

    searchButton.addEventListener('click', () => {
        const query = searchBar.value.toLowerCase();
        window.location.href = `products.html?search=${query}`;
    });

    menuIcon.addEventListener('click', () => {
        nav.classList.toggle('active');
    });
    let searchForm = document.querySelector('.search-form');

    document.querySelector('#search-btn').onclick = () => {
        searchForm.classList.toggle('active');
    }


    updateCartCount();
});
