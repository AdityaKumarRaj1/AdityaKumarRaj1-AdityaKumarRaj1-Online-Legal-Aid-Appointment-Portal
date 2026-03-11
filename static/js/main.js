/* ============================================
   Main JavaScript for Legal Aid Portal
   ============================================ */

document.addEventListener('DOMContentLoaded', function () {

    // === Auto-dismiss alerts after 5 seconds ===
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 5000);
    });

    // === Animate elements on scroll ===
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.feature-card, .stat-card, .lawyer-card, .card-custom').forEach(function (el) {
        el.style.opacity = '0';
        observer.observe(el);
    });

    // === Navbar shrink on scroll ===
    const navbar = document.querySelector('.navbar-custom');
    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                navbar.style.padding = '0.3rem 0';
                navbar.style.boxShadow = '0 4px 20px rgba(0,0,0,0.15)';
            } else {
                navbar.style.padding = '0.6rem 0';
                navbar.style.boxShadow = '';
            }
        });
    }

    // === Confirm before critical actions ===
    document.querySelectorAll('[data-confirm]').forEach(function (el) {
        el.addEventListener('click', function (e) {
            if (!confirm(this.dataset.confirm)) {
                e.preventDefault();
            }
        });
    });

    // === File upload preview ===
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(function (input) {
        input.addEventListener('change', function () {
            const fileName = this.files[0] ? this.files[0].name : 'No file chosen';
            const label = this.closest('.mb-3')?.querySelector('.file-name');
            if (label) {
                label.textContent = fileName;
            }
        });
    });

    // === Tooltip initialization ===
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // === Set active nav link ===
    const currentPath = window.location.pathname;
    document.querySelectorAll('.navbar-custom .nav-link').forEach(function (link) {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // === Counter animation for stat cards ===
    document.querySelectorAll('.stat-number').forEach(function (counter) {
        const target = parseInt(counter.textContent);
        if (isNaN(target)) return;

        let current = 0;
        const increment = Math.ceil(target / 40);
        const timer = setInterval(function () {
            current += increment;
            if (current >= target) {
                counter.textContent = target;
                clearInterval(timer);
            } else {
                counter.textContent = current;
            }
        }, 30);
    });
});
