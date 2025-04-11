document.addEventListener('DOMContentLoaded', function() {
    // Mobile Menu Toggle
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const navbarLinks = document.getElementById('navbarLinks');
    
    if (mobileMenuBtn && navbarLinks) {
        mobileMenuBtn.addEventListener('click', function() {
            navbarLinks.classList.toggle('active');
            this.classList.toggle('active');
        });
    }

    // Dropdown Toggle for Mobile
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            if (window.innerWidth <= 992) {
                e.preventDefault();
                const dropdown = this.closest('.dropdown');
                dropdown.classList.toggle('active');
                
                // Close other dropdowns
                document.querySelectorAll('.dropdown').forEach(otherDropdown => {
                    if (otherDropdown !== dropdown) {
                        otherDropdown.classList.remove('active');
                    }
                });
            }
        });
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown') && !e.target.closest('.mobile-menu-btn')) {
            document.querySelectorAll('.dropdown').forEach(dropdown => {
                dropdown.classList.remove('active');
            });
            
            if (window.innerWidth <= 992 && navbarLinks && !e.target.closest('#navbarLinks')) {
                navbarLinks.classList.remove('active');
                if (mobileMenuBtn) mobileMenuBtn.classList.remove('active');
            }
        }
    });

    // Cart button animation
    const cartBtn = document.querySelector('.cart-btn');
    if (cartBtn) {
        cartBtn.addEventListener('click', function() {
            this.classList.add('animate');
            setTimeout(() => {
                this.classList.remove('animate');
            }, 500);
        });
    }

    // Search toggle functionality
    const searchBtn = document.getElementById('search-btn');
    const searchForm = document.querySelector('.search-form');
    
    if (searchBtn && searchForm) {
        searchBtn.addEventListener('click', function(e) {
            e.preventDefault();
            searchForm.classList.toggle('active');
        });
    }

    // Close search when clicking outside
    document.addEventListener('click', function(e) {
        if (searchForm && !e.target.closest('.search-container') && !e.target.closest('#search-btn')) {
            searchForm.classList.remove('active');
        }
    });

    // User dropdown toggle
    const userBtn = document.querySelector('.user-btn');
    const userDropdown = document.querySelector('.user-menu');
    
    if (userBtn && userDropdown) {
        userBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            userDropdown.classList.toggle('show');
        });
    }

    // Close user dropdown when clicking outside
    document.addEventListener('click', function() {
        if (userDropdown) {
            userDropdown.classList.remove('show');
        }
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});