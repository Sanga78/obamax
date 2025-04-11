// Add subtle hover effects to value cards

document.addEventListener('DOMContentLoaded', function() {
    // FAQ Accordion Functionality
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        const answer = item.querySelector('.faq-answer');
        const icon = question.querySelector('i');
        question.addEventListener('click', () => {
            // Close all other items
            faqItems.forEach(otherItem => {
                if (otherItem !== item) {
                    otherItem.querySelector('.faq-question').classList.remove('active');
                    otherItem.querySelector('.faq-answer').classList.remove('show');
                    otherItem.querySelector('i').style.transform = 'rotate(0deg)';
                }
            });
            
            // Toggle current item
            
            
            
            // Rotate icon
            if (question.classList.contains('active')) {
                answer.style.maxHeight = '500px';
                answer.style.padding = '1.25rem';
                icon.style.transform = 'rotate(180deg)';
                question.style.background = 'var(--primary)';
                question.style.color = 'white';
                question.style.outline = '3px solid lime';          
            } else {
                icon.style.transform = 'rotate(0deg)';
                answer.style.maxHeight = '0px';
                answer.style.padding = '0 1.5rem';
                question.style.background = 'white';
                question.style.color = 'black';
                question.style.outline = 'none';
            }
            question.classList.toggle('active');
            answer.classList.toggle('show');
            
        });
        
    });

    // Stats Counter Animation (if you want animated numbers)
    const statNumbers = document.querySelectorAll('.stat-number');
    const animationDuration = 2000; // 2 seconds
    const frameDuration = 1000 / 60; // 60fps
    
    statNumbers.forEach(stat => {
        const target = parseInt(stat.textContent.replace(/,/g, ''));
        const suffix = stat.textContent.match(/\D+$/)?.[0] || '';
        const startTime = Date.now();
        
        // Only animate if element is in viewport
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const animate = () => {
                        const now = Date.now();
                        const progress = Math.min((now - startTime) / animationDuration, 1);
                        const currentValue = Math.floor(progress * target);
                        
                        stat.textContent = currentValue.toLocaleString() + suffix;
                        
                        if (progress < 1) {
                            requestAnimationFrame(animate);
                        }
                    };
                    
                    animate();
                    observer.unobserve(stat);
                }
            });
        });
        
        observer.observe(stat);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        });
    });
    document.querySelectorAll('.value-card').forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);
        });
    });
    // Parallax effect for hero section (optional)
    const hero = document.querySelector('.about-hero');
    if (hero) {
        window.addEventListener('scroll', function() {
            const scrollPosition = window.pageYOffset;
            hero.style.backgroundPositionY = scrollPosition * 0.5 + 'px';
        });
    }
    // Add to the DOMContentLoaded event
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.onload = () => {
                    img.classList.add('loaded');
                };
                imageObserver.unobserve(img);
            }
        });
    }, { rootMargin: '200px' });

    images.forEach(img => imageObserver.observe(img));
});
