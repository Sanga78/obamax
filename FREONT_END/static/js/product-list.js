document.addEventListener('DOMContentLoaded', () => {
    const products = [
        { id: '1', name: 'Smartphone', price: 699, description: 'High-end smartphone with a great camera', image: 'path/to/smartphone.jpg' },
        { id: '2', name: 'Tablet', price: 499, description: 'Lightweight tablet with a long battery life', image: 'path/to/tablet.jpg' },
        { id: '3', name: 'Laptop', price: 999, description: 'Powerful laptop for all your needs', image: 'path/to/laptop.jpg' },
        { id: '4', name: 'Charger', price: 29, description: 'Fast charging USB-C charger', image: 'path/to/charger.jpg' },
        { id: '5', name: 'Headphones', price: 199, description: 'Noise-cancelling over-ear headphones', image: 'path/to/headphones.jpg' },
        { id: '6', name: 'Smart Home Device', price: 149, description: 'Smart home assistant with voice control', image: 'path/to/smart-home.jpg' },
        // Add more products as needed
    ];

    const productGrid = document.getElementById('product-grid');

    products.forEach(product => {
        const productCard = document.createElement('div');
        productCard.classList.add('product-card');
        productCard.innerHTML = `
            <img src="${product.image}" alt="${product.name}">
            <h3>${product.name}</h3>
            <p>$${product.price}</p>
            <a href="product.html?id=${product.id}">View Details</a>
        `;
        productGrid.appendChild(productCard);
    });
});
