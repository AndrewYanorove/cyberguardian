// Основные функции сайта с кибер-эффектами
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 CyberGuardian загружен!');
    
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
    
    // Случайные кибер-эффекты в фоне
    createCyberEffects();
});

// Создание случайных кибер-эффектов в фоне
function createCyberEffects() {
    const effectsContainer = document.createElement('div');
    effectsContainer.style.position = 'fixed';
    effectsContainer.style.top = '0';
    effectsContainer.style.left = '0';
    effectsContainer.style.width = '100%';
    effectsContainer.style.height = '100%';
    effectsContainer.style.pointerEvents = 'none';
    effectsContainer.style.zIndex = '-1';
    effectsContainer.style.overflow = 'hidden';
    document.body.appendChild(effectsContainer);
    
    // Создаем случайные линии и точки
    for (let i = 0; i < 20; i++) {
        createCyberLine(effectsContainer);
        createCyberDot(effectsContainer);
    }
}

function createCyberLine(container) {
    const line = document.createElement('div');
    line.style.position = 'absolute';
    line.style.width = Math.random() * 100 + 50 + 'px';
    line.style.height = '1px';
    line.style.background = `linear-gradient(90deg, transparent, ${getRandomCyberColor()}, transparent)`;
    line.style.top = Math.random() * 100 + 'vh';
    line.style.left = Math.random() * 100 + 'vw';
    line.style.opacity = Math.random() * 0.3;
    line.style.animation = `moveLine ${Math.random() * 10 + 5}s linear infinite`;
    
    container.appendChild(line);
}

function createCyberDot(container) {
    const dot = document.createElement('div');
    dot.style.position = 'absolute';
    dot.style.width = '2px';
    dot.style.height = '2px';
    dot.style.background = getRandomCyberColor();
    dot.style.borderRadius = '50%';
    dot.style.top = Math.random() * 100 + 'vh';
    dot.style.left = Math.random() * 100 + 'vw';
    dot.style.boxShadow = `0 0 ${Math.random() * 10 + 5}px currentColor`;
    dot.style.animation = `pulse ${Math.random() * 3 + 2}s ease-in-out infinite`;
    
    container.appendChild(dot);
}

function getRandomCyberColor() {
    const colors = ['#00ff88', '#0088ff', '#ff0088', '#8800ff', '#ff8800'];
    return colors[Math.floor(Math.random() * colors.length)];
}

// Добавляем CSS анимации
const style = document.createElement('style');
style.textContent = `
    @keyframes moveLine {
        0% { transform: translateX(-100px) rotate(${Math.random() * 360}deg); }
        100% { transform: translateX(100px) rotate(${Math.random() * 360}deg); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.3; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.5); }
    }
`;
document.head.appendChild(style);

// Утилиты
function showCyberNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} cyber-border position-fixed`;
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '9999';
    notification.style.minWidth = '300px';
    notification.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="bi bi-info-circle me-2"></i>
            <span>${message}</span>
            <button type="button" class="btn-close ms-auto" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Автоматическое скрытие через 5 секунд
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Экспорт функций для использования в других модулях
window.CyberGuardian = {
    showNotification: showCyberNotification,
    effects: {
        createCyberLine,
        createCyberDot
    }
};