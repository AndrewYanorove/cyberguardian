// Основные функции сайта с кибер-эффектами
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 CyberGuardian загружен!');
    
    // Инициализация всех компонентов
    initCyberEffects();
    initAnimations();
    initNavigation();
    initForms();
    initNotifications();
});

// Инициализация кибер-эффектов
function initCyberEffects() {
    // Добавляем кибер-эффекты для текста
    const cyberTexts = document.querySelectorAll('.cyber-text');
    cyberTexts.forEach(text => {
        text.addEventListener('mouseenter', function() {
            this.classList.add('cyber-glitch');
        });
        
        text.addEventListener('mouseleave', function() {
            this.classList.remove('cyber-glitch');
        });
    });
    
    // Создаем сетку в фоне
    createCyberGrid();
    
    // Создаем эффект матрицы
    createMatrixEffect();
    
    // Случайные кибер-эффекты в фоне
    createCyberParticles();
}

// Инициализация анимаций
function initAnimations() {
    // Анимация появления элементов
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);
    
    // Анимируем карточки
    document.querySelectorAll('.cyber-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(50px)';
        card.style.transition = 'all 0.8s ease';
        observer.observe(card);
    });
    
    // Анимируем другие элементы
    document.querySelectorAll('.fade-in').forEach(item => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(30px)';
        observer.observe(item);
    });
}

// Инициализация навигации
function initNavigation() {
    // Плавная прокрутка
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Активное состояние навигации
    const currentPage = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
    });
}

// Инициализация форм
function initForms() {
    // Валидация форм
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
    
    // Интерактивные элементы форм
    document.querySelectorAll('.cyber-input').forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });
}

// Создание кибер-сетки
function createCyberGrid() {
    const grid = document.createElement('div');
    grid.className = 'cyber-grid';
    document.body.appendChild(grid);
}

// Создание эффекта матрицы
function createMatrixEffect() {
    const matrix = document.createElement('div');
    matrix.className = 'matrix-effect';
    document.body.appendChild(matrix);
}

// Создание кибер-частиц
function createCyberParticles() {
    const particlesContainer = document.createElement('div');
    particlesContainer.style.position = 'fixed';
    particlesContainer.style.top = '0';
    particlesContainer.style.left = '0';
    particlesContainer.style.width = '100%';
    particlesContainer.style.height = '100%';
    particlesContainer.style.pointerEvents = 'none';
    particlesContainer.style.zIndex = '-1';
    particlesContainer.style.overflow = 'hidden';
    document.body.appendChild(particlesContainer);
    
    // Создаем случайные частицы
    for (let i = 0; i < 30; i++) {
        createCyberParticle(particlesContainer);
    }
}

function createCyberParticle(container) {
    const particle = document.createElement('div');
    const size = Math.random() * 3 + 1;
    const colors = ['#00ff88', '#0088ff', '#ff0088', '#8800ff'];
    
    particle.style.position = 'absolute';
    particle.style.width = size + 'px';
    particle.style.height = size + 'px';
    particle.style.background = colors[Math.floor(Math.random() * colors.length)];
    particle.style.borderRadius = '50%';
    particle.style.top = Math.random() * 100 + 'vh';
    particle.style.left = Math.random() * 100 + 'vw';
    particle.style.opacity = Math.random() * 0.3;
    particle.style.boxShadow = '0 0 ' + (size * 2) + 'px currentColor';
    
    // Анимация движения
    particle.style.animation = `
        moveParticle ${Math.random() * 10 + 5}s linear infinite,
        pulseParticle ${Math.random() * 3 + 2}s ease-in-out infinite
    `;
    
    container.appendChild(particle);
}

// Анимации для частиц
const style = document.createElement('style');
style.textContent = `
    @keyframes moveParticle {
        0% { 
            transform: translate(0, 0) rotate(0deg); 
        }
        25% { 
            transform: translate(${Math.random() * 100 - 50}px, ${Math.random() * 100 - 50}px) rotate(90deg); 
        }
        50% { 
            transform: translate(${Math.random() * 100 - 50}px, ${Math.random() * 100 - 50}px) rotate(180deg); 
        }
        75% { 
            transform: translate(${Math.random() * 100 - 50}px, ${Math.random() * 100 - 50}px) rotate(270deg); 
        }
        100% { 
            transform: translate(0, 0) rotate(360deg); 
        }
    }
    
    @keyframes pulseParticle {
        0%, 100% { 
            opacity: 0.2; 
            transform: scale(1); 
        }
        50% { 
            opacity: 0.8; 
            transform: scale(1.5); 
        }
    }
`;
document.head.appendChild(style);

// Система уведомлений
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
    
    // Стили для уведомления
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '9999';
    notification.style.minWidth = '300px';
    notification.style.maxWidth = '400px';
    notification.style.backdropFilter = 'blur(10px)';
    
    document.body.appendChild(notification);
    
    // Автоматическое скрытие через 5 секунд
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
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

// Утилиты
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Глобальные функции
window.CyberGuardian = {
    showNotification: showCyberNotification,
    utils: {
        formatFileSize,
        debounce
    },
    effects: {
        createCyberParticle,
        createMatrixEffect
    }
};

// Обработчики событий
window.addEventListener('resize', debounce(() => {
    // Пересоздаем эффекты при изменении размера окна
    document.querySelectorAll('.cyber-grid, .matrix-effect').forEach(el => el.remove());
    createCyberGrid();
    createMatrixEffect();
}, 250));

// Service Worker для оффлайн-работы (если нужно)
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').catch(console.error);
}

// Функции для бокового меню (уже добавлены в base.html, но для полноты)
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    sidebar.classList.toggle('active');
    overlay.classList.toggle('active');
}

function closeSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    sidebar.classList.remove('active');
    overlay.classList.remove('active');
}

// Закрытие меню при клике на ссылку (мобильные)
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.sidebar-item').forEach(item => {
        item.addEventListener('click', () => {
            if (window.innerWidth < 992) {
                closeSidebar();
            }
        });
    });

    // Закрытие меню при изменении размера окна
    window.addEventListener('resize', () => {
        if (window.innerWidth >= 992) {
            closeSidebar();
        }
    });
});