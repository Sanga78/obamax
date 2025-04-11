document.addEventListener('DOMContentLoaded', function() {
    // Avatar upload functionality
    const avatarUploadBtn = document.querySelector('.avatar-upload-btn');
    if (avatarUploadBtn) {
        avatarUploadBtn.addEventListener('click', function(e) {
            e.preventDefault();
            // In a real implementation, this would trigger a file input
            alert('Avatar upload functionality would go here');
        });
    }

    // Order filtering
    const orderFilter = document.getElementById('order-filter');
    if (orderFilter) {
        orderFilter.addEventListener('change', function() {
            // In a real implementation, this would filter orders
            console.log('Filtering by:', this.value);
        });
    }

    // Form validation
    const profileForm = document.querySelector('.profile-form');
    if (profileForm) {
        profileForm.addEventListener('submit', function(e) {
            // Add form validation logic here
            const phoneInput = document.getElementById('phone');
            if (phoneInput && !/^[\d\s+-]+$/.test(phoneInput.value)) {
                e.preventDefault();
                alert('Please enter a valid phone number');
                phoneInput.focus();
            }
        });
    }
});