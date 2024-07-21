document.addEventListener('DOMContentLoaded', () => {
    const menuIcon = document.getElementById('menu-btn');
    const nav = document.querySelector('header nav');

    menuIcon.addEventListener('click', () => {
        nav.classList.toggle('active');
    });
    let searchForm = document.querySelector('.search-form');

    document.querySelector('#search-btn').onclick = () => {
        searchForm.classList.toggle('active');
    }
});
