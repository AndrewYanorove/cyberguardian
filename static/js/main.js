// Оптимизированные функции сайта с кибер-эффектами
document.addEventListener('DOMContentLoaded', function() {
    // Инициализация только критически важных компонентов
    initNavigation();
    initForms();
    
    // Отложенная загрузка тяжелых эффектов
    setTimeout(initCyberEffects, 1000);
    setTimeout(initAnimations, 500);
});

// Оптимизированная инициализация кибер-эффектов
function initCyberEffects() {
    // Упрощенные кибер-эффекты для текста
    const cyberTexts = document.querySelectorAll('.cyber-text');
    cyberTexts.forEach(text => {
        text.addEventListener('mouseenter', function() {
            this.style.textShadow = '0 0 10px currentColor';
        });
        
        text.addEventListener('mouseleave', function() {
            this.style.textShadow = 'none';
        });
    });
    
    // Упрощенная сетка в фоне (вместо создания DOM элементов)
    createOptimizedCyberGrid();
}

// Оптимизированная инициализация анимаций
function initAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.cyber-card, .fade-in').forEach(item => {
        observer.observe(item);
    });
}

// Упрощенная навигация
function initNavigation() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}

// Упрощенные формы
function initForms() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = this.querySelectorAll('input[required]');
            let isValid = true;
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    input.classList.add('is-invalid');
                    isValid = false;
                } else {
                    input.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showCyberNotification('Пожалуйста, заполните все обязательные поля', 'danger');
            }
        });
    });
}

// Оптимизированная кибер-сетка (CSS-based вместо DOM)
function createOptimizedCyberGrid() {
    if (!document.querySelector('.cyber-grid')) {
        const grid = document.createElement('div');
        grid.className = 'cyber-grid';
        document.body.appendChild(grid);
    }
}

// Упрощенная система уведомлений
function showCyberNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} cyber-notification`;
    notification.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="bi ${getNotificationIcon(type)} me-2"></i>
            <span>${message}</span>
            <button type="button" class="btn-close ms-auto" onclick="this.parentElement.parentElement.remove()"></button>
        </div>
    `;
    
    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        zIndex: '9999',
        minWidth: '300px',
        backdropFilter: 'blur(10px)'
    });
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        if (notification.parentNode) notification.remove();
    }, 5000);
}

function getNotificationIcon(type) {
    const icons = {
        'success': 'bi-check-circle',
        'danger': 'bi-exclamation-circle',
        'warning': 'bi-exclamation-triangle',
        'info': 'bi-info-circle'
    };
    return icons[type] || 'bi-info-circle';
}

// Убраны тяжелые функции: createCyberParticles, createMatrixEffect
// Убраны сложные анимации частиц

// Убрана регистрация ServiceWorker (из-за 404 ошибки)
// if ('serviceWorker' in navigator) {
//     navigator.serviceWorker.register('/sw.js').catch(console.error);
// }

// Функции для бокового меню (оставлены как есть)
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    sidebar.classList.toggle('active');
    overlay.classList.toggle('active');
    
    if (sidebar.classList.contains('active')) {
        document.body.style.overflow = 'hidden';
    } else {
        document.body.style.overflow = '';
    }
}

function closeSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    sidebar.classList.remove('active');
    overlay.classList.remove('active');
    document.body.style.overflow = '';
}

// Закрытие меню при клике на ссылку
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.sidebar-item').forEach(item => {
        item.addEventListener('click', () => {
            if (window.innerWidth < 992) closeSidebar();
        });
    });
});