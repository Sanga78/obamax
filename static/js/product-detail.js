document.addEventListener('DOMContentLoaded', function() {
    // Initialize star ratings display
    function initializeStarRatings() {
        document.querySelectorAll('.stars[data-rating]').forEach(starsContainer => {
            const rating = parseFloat(starsContainer.getAttribute('data-rating'));
            const fullStars = Math.floor(rating);
            const hasHalfStar = (rating % 1) >= 0.5;
            
            let starsHTML = '';
            
            // Add full stars
            for (let i = 0; i < fullStars; i++) {
                starsHTML += '<i class="fas fa-star"></i>';
            }
            
            // Add half star if needed
            if (hasHalfStar) {
                starsHTML += '<i class="fas fa-star-half-alt"></i>';
            }
            
            // Add empty stars
            const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
            for (let i = 0; i < emptyStars; i++) {
                starsHTML += '<i class="far fa-star"></i>';
            }
            
            starsContainer.innerHTML = starsHTML;
        });
    }

    // Initialize interactive star rating for forms
    function initInteractiveStarRating() {
        const starInputs = document.querySelectorAll('.star-rating input');
        const starLabels = document.querySelectorAll('.star-rating label');
        
        starLabels.forEach(label => {
            label.addEventListener('click', function() {
                const inputId = this.getAttribute('for');
                const input = document.getElementById(inputId);
                const rating = input.value;
                
                // Update visual display
                starLabels.forEach((l, index) => {
                    if (index < rating) {
                        l.style.color = 'var(--warning)';
                    } else {
                        l.style.color = 'var(--light-gray)';
                    }
                });
            });
        });

        // Initialize form stars if editing a review
        const currentRatingInput = document.querySelector('.star-rating input:checked');
        if (currentRatingInput) {
            const rating = currentRatingInput.value;
            starLabels.forEach((label, index) => {
                if (index < rating) {
                    label.style.color = 'var(--warning)';
                }
            });
        }
    }

    // Tab functionality
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));
            
            button.classList.add('active');
            const tabId = button.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });

    // Thumbnail click functionality
    const thumbnails = document.querySelectorAll('.thumbnail');
    const mainImage = document.querySelector('.main-product-image');
    
    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', () => {
            thumbnails.forEach(t => t.classList.remove('active'));
            thumbnail.classList.add('active');
            const thumbnailImg = thumbnail.querySelector('img');
            mainImage.src = thumbnailImg.src;
        });
    });

    // Quantity controls
    const quantityInput = document.querySelector('.quantity-input');
    const decreaseBtn = document.querySelector('.quantity-btn.decrease');
    const increaseBtn = document.querySelector('.quantity-btn.increase');
    
    decreaseBtn.addEventListener('click', () => {
        let value = parseInt(quantityInput.value);
        if (value > 1) {
            quantityInput.value = value - 1;
        }
    });
    
    increaseBtn.addEventListener('click', () => {
        let value = parseInt(quantityInput.value);
        quantityInput.value = value + 1;
    });

    // Initialize all components
    initializeStarRatings();
    initInteractiveStarRating();

    // Confirm review deletion
    document.querySelectorAll('.delete-review').forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete your review?')) {
                e.preventDefault();
            }
        });
    });
});