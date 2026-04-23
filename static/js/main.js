// 🚀 СОВРЕМЕННЫЙ JavaScript ДЛЯ УЛЬТРА-СТИЛЬНОГО САЙТА

const YM_COUNTER_ID = 108701111;
function ymReachGoal(goalName) {
    if (typeof ym !== 'function') return;
    try {
        ym(YM_COUNTER_ID, 'reachGoal', goalName);
    } catch (err) {
        console.warn('ym reachGoal', err);
    }
}
window.ymReachGoal = ymReachGoal;

const PHONE_INCOMPLETE_TEXT =
    'Введите полный номер: +7 (___) ___-__-__ (только цифры, 10 цифр после 7)';

/**
 * 11 цифр, начиная с 7 (РФ), или null.
 */
function getRuPhone11Digits(value) {
    let d = String(value || '').replace(/\D/g, '');
    if (d.length === 0) {
        return null;
    }
    if (d[0] === '8') {
        d = '7' + d.slice(1);
    }
    if (d.length === 10 && d[0] === '9') {
        d = '7' + d;
    }
    if (d.length > 11) {
        d = d.slice(0, 11);
    }
    if (d.length === 11 && d[0] === '7') {
        return d;
    }
    return null;
}

function isValidRuMobilePhone(value) {
    return getRuPhone11Digits(value) !== null;
}

function formatRuPhoneForStorage(value) {
    const d = getRuPhone11Digits(value);
    if (!d) {
        return '';
    }
    return `+7 (${d.slice(1, 4)}) ${d.slice(4, 7)}-${d.slice(7, 9)}-${d.slice(9, 11)}`;
}
window.formatRuPhoneForStorage = formatRuPhoneForStorage;

/**
 * @returns {boolean} false, если в форме есть phone и он неполный/некорректный
 */
function validateFormPhone(form) {
    const el = form.querySelector('input[name="phone"]');
    if (!el) {
        return true;
    }
    if (!isValidRuMobilePhone(el.value)) {
        if (typeof window.showNotification === 'function') {
            window.showNotification(PHONE_INCOMPLETE_TEXT, 'error');
        }
        el.focus();
        return false;
    }
    return true;
}

window.isValidRuMobilePhone = isValidRuMobilePhone;
window.getRuPhone11Digits = getRuPhone11Digits;
window.validateFormPhone = validateFormPhone;

document.addEventListener('DOMContentLoaded', function () {
    // ПРИНУДИТЕЛЬНО УСТАНАВЛИВАЕМ БЕЛЫЙ ЦВЕТ ДЛЯ СТАТИСТИКИ
    setTimeout(() => {
        const statNumbers = document.querySelectorAll('.hero-stats div:first-child');
        const statLabels = document.querySelectorAll('.hero-stats div:last-child');

        statNumbers.forEach(el => {
            el.style.color = '#ffffff !important';
            el.style.fontWeight = '900 !important';
        });

        statLabels.forEach(el => {
            el.style.color = '#ffffff !important';
            el.style.fontWeight = '500 !important';
        });
    }, 100);

    // Инициализация всех компонентов
    initPreloader();
    initScrollAnimations();
    initHeader();
    initServicesDropdown();
    initMobileMenu();
    initModals();
    initForms();
    initSmoothScroll();
    initPhoneFormatting();

    // Initialize progress bar for heating preparation page
    const progressFill = document.querySelector('.progress-fill');
    if (progressFill) {
        // Set initial progress to 25% (first button)
        progressFill.style.width = '25%';
        console.log('Progress bar initialized to 25%');
    }
    initParallax();
    initModernFeatures();
    initAnimatedBorders();
    initModernInteractions();
    initPerformanceOptimizations();
    initScrollTopFab();

    // Обработка якорей при загрузке страницы
    handlePageAnchor();

    // Плавная загрузка страницы с улучшенными эффектами
    setTimeout(() => {
        document.body.classList.add('loaded');
        initPageLoadAnimations();
    }, 150);

    adjustBodyPadding();
    window.addEventListener('load', adjustBodyPadding);

    // Современная оптимизация производительности
    initIntersectionObserver();

    console.log('🎨 Современный дизайн загружен успешно!');

    setTimeout(function () {
        if (typeof refreshPhoneFieldMeta === 'function') {
            refreshPhoneFieldMeta();
        }
    }, 400);
    setTimeout(function () {
        if (typeof refreshPhoneFieldMeta === 'function') {
            refreshPhoneFieldMeta();
        }
    }, 2000);
});

// Обработка якорей при загрузке страницы
function handlePageAnchor() {
    const hash = window.location.hash;
    if (hash) {
        setTimeout(() => {
            const targetElement = document.querySelector(hash);
            if (targetElement) {
                const headerHeight = document.getElementById('header').offsetHeight;
                const targetPosition = targetElement.offsetTop - headerHeight - 20;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        }, 500); // Небольшая задержка для загрузки контента
    }
}

function initScrollTopFab() {
    const btn = document.getElementById('scrollTopFab');
    if (!btn) return;

    const threshold = 200;
    let ticking = false;

    function updateVisibility() {
        if (window.scrollY > threshold) {
            btn.classList.add('scroll-top-fab--visible');
        } else {
            btn.classList.remove('scroll-top-fab--visible');
        }
        ticking = false;
    }

    function onScroll() {
        if (!ticking) {
            ticking = true;
            window.requestAnimationFrame(updateVisibility);
        }
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll, { passive: true });
    window.addEventListener('load', updateVisibility);
    updateVisibility();

    btn.addEventListener('click', () => {
        const instant = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        window.scrollTo({ top: 0, behavior: instant ? 'auto' : 'smooth' });
    });
}

// Прелоадер
function initPreloader() {
    const preloader = document.getElementById('preloader');
    if (preloader) {
        // Скрываем прелоадер сразу, если страница уже загружена
        if (document.readyState === 'complete') {
            preloader.style.display = 'none';
            return;
        }

        // Показываем прелоадер только при первой загрузке
        window.addEventListener('load', function () {
            setTimeout(() => {
                preloader.style.opacity = '0';
                setTimeout(() => {
                    preloader.style.display = 'none';
                }, 300);
            }, 500); // Уменьшили время показа
        });
    }
}

// Анимации при скролле
function initScrollAnimations() {
    // Проверяем поддержку Intersection Observer
    if ('IntersectionObserver' in window) {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target._scrollAnimationStarted) {
                    entry.target._scrollAnimationStarted = true;
                    entry.target.classList.add('animate');

                    // Добавляем задержку для каскадной анимации
                    const delay = entry.target.dataset.delay || 0;
                    entry.target.style.animationDelay = delay + 'ms';
                }
            });
        }, observerOptions);

        // Наблюдаем за элементами для анимации
        document.querySelectorAll('.animate-on-scroll').forEach(el => {
            observer.observe(el);
        });

        // Наблюдаем за карточками услуг
        document.querySelectorAll('.service-card').forEach((card, index) => {
            card.classList.add('animate-on-scroll');
            card.dataset.delay = index * 200;
            observer.observe(card);
        });

        // Наблюдаем за фотографиями
        document.querySelectorAll('.photo-item').forEach((photo, index) => {
            photo.classList.add('animate-on-scroll');
            photo.dataset.delay = index * 150;
            observer.observe(photo);
        });

        // Наблюдаем за карточками услуг современного дизайна
        document.querySelectorAll('.service-card-modern').forEach((card, index) => {
            if (!card.classList.contains('animate-on-scroll')) {
                card.classList.add('animate-on-scroll');
                card.dataset.delay = index * 100;
                observer.observe(card);
            }
        });
    }
}

function updateHeaderOffset() {
    const header = document.getElementById('header');
    if (header) {
        document.documentElement.style.setProperty('--header-offset', `${header.offsetHeight}px`);
    }
}

// Фиксированная шапка: body только под бар шапки; слот под панель «Услуги» — в padding героя (--services-panel-slot)
function initHeader() {
    const header = document.getElementById('header');
    if (!header) return;

    adjustBodyPadding();
}

function closeServicesDropdown() {
    const panel = document.getElementById('servicesDropdownPanel');
    const toggle = document.getElementById('servicesDropdownToggle');
    if (panel) {
        panel.classList.remove('is-open');
        panel.setAttribute('aria-hidden', 'true');
    }
    if (toggle) {
        toggle.setAttribute('aria-expanded', 'false');
    }
}

function initServicesDropdown() {
    const toggle = document.getElementById('servicesDropdownToggle');
    const panel = document.getElementById('servicesDropdownPanel');
    const dropdown = document.getElementById('servicesDropdown');
    if (!toggle || !panel || !dropdown) return;

    function openMenu() {
        toggle.setAttribute('aria-expanded', 'true');
        panel.classList.add('is-open');
        panel.setAttribute('aria-hidden', 'false');
    }

    const isHoverEnabled = () => {
        if (window.innerWidth <= 768) return false;
        return window.matchMedia && window.matchMedia('(hover: hover) and (pointer: fine)').matches;
    };

    let closeTimer = null;
    const scheduleClose = () => {
        if (closeTimer) clearTimeout(closeTimer);
        closeTimer = setTimeout(() => closeServicesDropdown(), 140);
    };
    const cancelScheduledClose = () => {
        if (closeTimer) clearTimeout(closeTimer);
        closeTimer = null;
    };

    toggle.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (panel.classList.contains('is-open')) {
            closeServicesDropdown();
        } else {
            openMenu();
        }
    });

    // Desktop hover open (click still works for accessibility/touch).
    dropdown.addEventListener('mouseenter', () => {
        if (!isHoverEnabled()) return;
        cancelScheduledClose();
        openMenu();
    });
    dropdown.addEventListener('mouseleave', () => {
        if (!isHoverEnabled()) return;
        scheduleClose();
    });
    panel.addEventListener('mouseenter', () => {
        if (!isHoverEnabled()) return;
        cancelScheduledClose();
        openMenu();
    });
    panel.addEventListener('mouseleave', () => {
        if (!isHoverEnabled()) return;
        scheduleClose();
    });

    panel.querySelectorAll('a[href]').forEach((a) => {
        a.addEventListener('click', () => closeServicesDropdown());
    });

    document.addEventListener('click', (e) => {
        if (!panel.classList.contains('is-open')) return;
        if (dropdown.contains(e.target) || panel.contains(e.target)) return;
        closeServicesDropdown();
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeServicesDropdown();
    });

    window.addEventListener(
        'resize',
        debounce(() => {
            if (window.innerWidth <= 768) closeServicesDropdown();
            adjustBodyPadding();
        }, 200)
    );
}

/** Закрыть выезжающее меню и снять блокировку скролла (для модалок и ссылок из меню). */
function closeMobileMenuFromOutside() {
    const mobileMenu = document.getElementById('mobileMenu');
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    if (!mobileMenu || !mobileMenu.classList.contains('active')) return;
    mobileMenu.classList.remove('active');
    document.body.style.overflow = '';
    if (mobileMenuToggle) {
        mobileMenuToggle.setAttribute('aria-expanded', 'false');
        mobileMenuToggle.setAttribute('aria-hidden', 'false');
        mobileMenuToggle.setAttribute('aria-label', 'Открыть меню');
    }
}

// Мобильное меню
function initMobileMenu() {
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const mobileMenu = document.getElementById('mobileMenu');

    if (!mobileMenuToggle || !mobileMenu) return;

    // Открытие/закрытие мобильного меню
    mobileMenuToggle.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();

        if (mobileMenu.classList.contains('active')) {
            closeMobileMenu();
        } else {
            openMobileMenu();
        }
    });

    const mobileMenuClose = document.getElementById('mobileMenuClose');
    if (mobileMenuClose) {
        mobileMenuClose.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            closeMobileMenu();
        });
    }

    // Закрытие меню при клике на фон
    mobileMenu.addEventListener('click', function (e) {
        if (e.target === mobileMenu) {
            closeMobileMenu();
        }
    });

    // Закрытие меню при клике на ссылку
    const mobileNavItems = mobileMenu.querySelectorAll('.mobile-nav-item');
    mobileNavItems.forEach(item => {
        item.addEventListener('click', function () {
            closeMobileMenu();
        });
    });

    mobileMenu.querySelectorAll('.mobile-menu-quick__item[href]').forEach(link => {
        link.addEventListener('click', function () {
            closeMobileMenu();
        });
    });

    // Закрытие меню при нажатии Escape
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && mobileMenu.classList.contains('active')) {
            closeMobileMenu();
        }
    });

    function openMobileMenu() {
        closeServicesDropdown();
        mobileMenu.classList.add('active');
        document.body.style.overflow = 'hidden';
        mobileMenuToggle.setAttribute('aria-expanded', 'true');
        mobileMenuToggle.setAttribute('aria-hidden', 'true');
    }

    function closeMobileMenu() {
        closeMobileMenuFromOutside();
    }
}


// Модальные окна
function initModals() {
    // Приглашение в тендер
    const tenderModal = document.getElementById('tenderModal');
    const tenderModalClose = document.getElementById('tenderModalClose');

    document.querySelectorAll('.js-tender-open').forEach(btn => {
        if (!tenderModal) return;
        btn.addEventListener('click', e => {
            e.preventDefault();
            closeMobileMenuFromOutside();
            openModal(tenderModal);
        });
    });
    if (tenderModalClose) {
        tenderModalClose.addEventListener('click', () => closeModal(tenderModal));
    }

    // Заявка на услугу
    const serviceModal = document.getElementById('serviceModal');
    const serviceModalClose = document.getElementById('serviceModalClose');

    document.addEventListener('click', function (e) {
        if (e.target.classList.contains('btn-service-application') ||
            e.target.classList.contains('btn-call-specialist')) {
            const serviceType = e.target.dataset.service;
            if (serviceType) {
                document.getElementById('serviceType').value = serviceType;
                openModal(serviceModal);
            }
        }
    });

    if (serviceModalClose) {
        serviceModalClose.addEventListener('click', () => closeModal(serviceModal));
    }

    // Звонок
    const callModal = document.getElementById('callModal');
    const callModalClose = document.getElementById('callModalClose');

    document.querySelectorAll('.js-callback-open').forEach(btn => {
        if (!callModal) return;
        btn.addEventListener('click', e => {
            e.preventDefault();
            closeMobileMenuFromOutside();
            openModal(callModal);
        });
    });

    document.addEventListener('click', function (e) {
        if (e.target.classList.contains('btn-call') || e.target.classList.contains('btn-call-specialist')) {
            openModal(callModal);
        }
    });

    if (callModalClose) {
        callModalClose.addEventListener('click', () => closeModal(callModal));
    }

    document.addEventListener('click', onModalBackdropClick, false);
    document.addEventListener('keydown', onModalEscapeKey, false);
}

// Функции для работы с модалами
function isModalVisible(modal) {
    if (!modal) return false;
    if (modal.classList.contains('show')) return true;
    const inline = modal.style.display;
    if (inline === 'block' || inline === 'flex') return true;
    return window.getComputedStyle(modal).display !== 'none';
}

function closeAnyModal(modal) {
    if (!modal) return;
    const id = modal.id;
    const w = window;
    if (id === 'callbackModal' && typeof w.closeCallbackModal === 'function') {
        w.closeCallbackModal();
        return;
    }
    if (id === 'applicationModal' && typeof w.closeApplicationModal === 'function') {
        w.closeApplicationModal();
        return;
    }
    if (id === 'quoteModal' && typeof w.closeQuoteModal === 'function') {
        w.closeQuoteModal();
        return;
    }
    closeModal(modal);
}

function onModalBackdropClick(e) {
    document.querySelectorAll('.modal').forEach(modal => {
        if (!isModalVisible(modal)) return;
        if (!modal.contains(e.target)) return;
        const panel = modal.querySelector('.modal-content');
        if (panel && panel.contains(e.target)) return;
        closeAnyModal(modal);
    });
}

function onModalEscapeKey(e) {
    if (e.key !== 'Escape') return;
    document.querySelectorAll('.modal').forEach(modal => {
        if (isModalVisible(modal)) closeAnyModal(modal);
    });
}

function openModal(modal) {
    modal.classList.add('show');
    document.body.style.overflow = 'hidden';

    // Фокус на первое поле ввода
    const firstInput = modal.querySelector('input:not([type="hidden"])');
    if (firstInput) {
        setTimeout(() => firstInput.focus(), 300);
    }
}

function closeModal(modal) {
    modal.classList.remove('show');
    document.body.style.overflow = '';

    // Очищаем формы
    const form = modal.querySelector('form');
    if (form) {
        form.reset();
        // Убираем состояние загрузки с кнопок
        const submitBtn = form.querySelector('.btn-submit');
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.textContent = submitBtn.dataset.originalText || submitBtn.textContent;
        }
    }
}

// Обработка форм
function initForms() {
    // Форма приглашения в тендер
    const tenderForm = document.getElementById('tenderForm');
    if (tenderForm) {
        tenderForm.addEventListener('submit', handleTenderSubmit);
    }

    // Форма заявки на услугу
    const serviceForm = document.getElementById('serviceForm');
    if (serviceForm) {
        serviceForm.addEventListener('submit', handleServiceSubmit);
    }

    // Обработка загрузки файлов
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function () {
            const caption = this.parentElement.querySelector('.file-upload__caption');
            if (caption && this.files.length > 0) {
                caption.textContent = this.files[0].name;
            }
        });
    });
}

// Обработка формы приглашения в тендер
async function handleTenderSubmit(e) {
    e.preventDefault();

    const form = e.target;
    if (!validateFormPhone(form)) {
        return;
    }

    const submitBtn = form.querySelector('.btn-submit');
    const originalText = submitBtn.textContent;

    // Показываем состояние загрузки
    submitBtn.disabled = true;
    submitBtn.textContent = 'Отправка...';
    submitBtn.dataset.originalText = originalText;

    try {
        const formData = new FormData(form);
        const phoneField = form.querySelector('input[name="phone"]');
        if (phoneField) {
            formData.set('phone', formatRuPhoneForStorage(phoneField.value));
        }

        const response = await fetch('/ajax/tender-invitation/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCSRFToken()
            }
        });

        const data = await response.json();

        if (data.success) {
            ymReachGoal('tender_form');
            showNotification(data.message, 'success');
            closeModal(document.getElementById('tenderModal'));
        } else {
            showNotification(data.message, 'error');
        }
    } catch (error) {
        showNotification('Произошла ошибка при отправке. Попробуйте еще раз.', 'error');
        console.error('Error:', error);
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
    }
}

// Обработка формы заявки на услугу
async function handleServiceSubmit(e) {
    e.preventDefault();

    const form = e.target;
    if (!validateFormPhone(form)) {
        return;
    }

    const submitBtn = form.querySelector('.btn-submit');
    const originalText = submitBtn.textContent;

    submitBtn.disabled = true;
    submitBtn.textContent = 'Отправка...';
    submitBtn.dataset.originalText = originalText;

    try {
        const formData = new FormData(form);
        const phoneEl = form.querySelector('input[name="phone"]');
        const data = {
            full_name: (formData.get('full_name') || '').trim(),
            phone: formatRuPhoneForStorage(phoneEl ? phoneEl.value : ''),
            service_type: formData.get('service_type'),
            agreed_to_processing: form.querySelector('input[name="agreed_to_processing"]')?.checked === true,
        };

        const response = await fetch('/ajax/service-application/', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            }
        });

        const result = await response.json();

        if (result.success) {
            ymReachGoal('service_form');
            showNotification(result.message, 'success');
            closeModal(document.getElementById('serviceModal'));
        } else {
            showNotification(result.message, 'error');
        }
    } catch (error) {
        showNotification('Произошла ошибка при отправке. Попробуйте еще раз.', 'error');
        console.error('Error:', error);
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
    }
}

// Получение CSRF токена
function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return value;
        }
    }

    // Fallback: попробуем найти токен в мета-теге
    const metaTag = document.querySelector('meta[name="csrf-token"]');
    return metaTag ? metaTag.getAttribute('content') : '';
}

// Тосты 1-в-1 в духе /services/ventilation/ (зелёный success справа сверху, z-index выше модалок)
function showNotification(message, type = 'info') {
    const el = document.createElement('div');
    el.setAttribute('role', 'status');
    el.setAttribute('aria-live', 'polite');
    const esc = String(message)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
    el.innerHTML = `<span class="site-toast__text">${esc}</span>`;
    const bg = {
        success: 'linear-gradient(135deg, #10b981, #059669)',
        error: 'linear-gradient(135deg, #ef4444, #dc2626)',
        info: 'linear-gradient(135deg, #1e88e5, #0d47a1)',
        warning: 'linear-gradient(135deg, #f59e0b, #d97706)',
    }[type] || 'linear-gradient(135deg, #1e88e5, #0d47a1)';
    const narrow = window.matchMedia('(max-width: 768px)').matches;
    const z = 2147482000;
    if (narrow) {
        el.className = 'site-toast site-toast--mob';
        el.style.cssText = [
            'position:fixed',
            'top:max(88px,calc(env(safe-area-inset-top,0px)+72px))',
            'left:50%',
            'right:auto',
            'transform:translateX(-50%)',
            'width:min(420px,calc(100vw - 24px))',
            'max-width:calc(100vw - 24px)',
            'box-sizing:border-box',
            'z-index:' + z,
            'padding:14px 18px',
            'border-radius:12px',
            'box-shadow:0 10px 30px rgba(0,0,0,.2)',
            'color:#fff',
            'font-weight:600',
            'text-align:center',
            'font-size:15px',
            'line-height:1.35',
            'background:' + bg,
            'animation:fadeInUp 0.3s ease-out',
        ].join(';');
    } else {
        el.className = 'site-toast';
        el.style.cssText = [
            'position:fixed',
            'top:20px',
            'right:20px',
            'z-index:' + z,
            'min-width:250px',
            'max-width:min(400px,92vw)',
            'padding:16px 24px',
            'border-radius:12px',
            'box-shadow:0 10px 30px rgba(0,0,0,.2)',
            'color:#fff',
            'font-weight:600',
            'text-align:center',
            'background:' + bg,
            'animation:slideInRight 0.3s ease-out',
        ].join(';');
    }
    document.body.appendChild(el);
    const ms = type === 'error' ? 5000 : 4000;
    setTimeout(function () {
        if (!el.parentNode) {
            return;
        }
        el.style.transition = 'opacity 0.28s ease, transform 0.28s ease';
        el.style.opacity = '0';
        if (narrow) {
            el.style.transform = 'translateX(-50%) translateY(-12px)';
        } else {
            el.style.transform = 'translateX(32px)';
        }
        setTimeout(function () {
            el.remove();
        }, 280);
    }, ms);
}
window.showNotification = showNotification;

// Update progress bar for heating preparation page
function updateHeatingPreparationProgress(targetId) {
    // Check if we're on the heating preparation page
    const progressFill = document.querySelector('.progress-fill');
    const pills = document.querySelectorAll('.pill-btn');

    if (progressFill && pills.length > 0) {
        // Find the index of the clicked pill
        let activeIndex = -1;
        pills.forEach((pill, index) => {
            if (pill.getAttribute('href') === '#' + targetId) {
                activeIndex = index;
                // Update active state
                pills.forEach(p => p.classList.remove('active'));
                pill.classList.add('active');
            }
        });

        if (activeIndex >= 0) {
            const progress = ((activeIndex + 1) / pills.length) * 100;
            progressFill.style.width = `${progress}%`;
            console.log('Progress updated to:', progress + '%');
        }
    }
}

// Плавный скролл для якорных ссылок
function initSmoothScroll() {
    // Обрабатываем все ссылки с якорями
    document.querySelectorAll('a[href*="#"]').forEach(link => {
        link.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            console.log('Clicked link with href:', href);

            // Если это ссылка на главную страницу с якорем
            if (href.includes('#contacts')) {
                console.log('Redirecting to contacts section');
                // Не предотвращаем стандартное поведение для ссылки на контакты
                return;
            }

            // Если это якорь на текущей странице
            if (href.startsWith('#')) {
                e.preventDefault();
                const targetId = href.substring(1);
                const targetElement = document.getElementById(targetId);
                console.log('Looking for element with ID:', targetId, 'Found:', targetElement);

                if (targetElement) {
                    const headerHeight = document.getElementById('header').offsetHeight;
                    const targetPosition = targetElement.offsetTop - headerHeight - 20;

                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });

                    // Update progress bar for heating preparation page
                    updateHeatingPreparationProgress(targetId);
                }
            }
        });
    });
}

function isPhoneMaskTarget(el) {
    if (!el || el.nodeName !== 'INPUT') {
        return false;
    }
    if (el.getAttribute('data-phone-skip') === '1') {
        return false;
    }
    if (el.type === 'tel') {
        return true;
    }
    return el.getAttribute('name') === 'phone' && (el.type === 'text' || el.type === '');
}

// Маска +7 (___) ___-__-__, не более 11 цифр
function formatPhoneInputValue(raw) {
    let d = String(raw).replace(/\D/g, '');
    if (d.startsWith('8')) {
        d = '7' + d.substring(1);
    }
    if (d.length && d[0] === '9' && d.length <= 10) {
        d = '7' + d;
    }
    if (d.length > 11) {
        d = d.substring(0, 11);
    }
    if (d.length === 0) {
        return '';
    }
    if (d[0] !== '7') {
        return d[0] === '9' ? formatPhoneInputValue('7' + d) : '+7';
    }

    let formatted = '+7';
    if (d.length > 1) {
        formatted += ' (' + d.substring(1, 4);
    }
    if (d.length > 4) {
        formatted += ') ' + d.substring(4, 7);
    }
    if (d.length > 7) {
        formatted += '-' + d.substring(7, 9);
    }
    if (d.length > 9) {
        formatted += '-' + d.substring(9, 11);
    }
    return formatted;
}

let _phoneMaskDelegationInit = false;

function ensurePhoneInputMeta(t) {
    if (!isPhoneMaskTarget(t)) {
        return;
    }
    if (!t.placeholder) {
        t.placeholder = '+7 (999) 123-45-67';
    }
    t.setAttribute('inputmode', 'tel');
    t.setAttribute('autocomplete', 'tel');
    if (t.type !== 'tel' && t.getAttribute('name') === 'phone') {
        t.setAttribute('type', 'tel');
    }
}

/**
 * Делегирование на document — маска не слетает после cloneNode() (вентиляция и др.).
 */
function initPhoneFormatting() {
    document.querySelectorAll('input[type="tel"], input[name="phone"]').forEach(ensurePhoneInputMeta);

    if (_phoneMaskDelegationInit) {
        return;
    }
    _phoneMaskDelegationInit = true;

    document.addEventListener(
        'input',
        (e) => {
            const t = e.target;
            if (!isPhoneMaskTarget(t)) {
                return;
            }
            ensurePhoneInputMeta(t);
            t.value = formatPhoneInputValue(t.value);
            try {
                t.setSelectionRange(t.value.length, t.value.length);
            } catch (err) {
                /* ignore */
            }
        },
        true
    );

    document.addEventListener(
        'paste',
        (e) => {
            const t = e.target;
            if (!isPhoneMaskTarget(t)) {
                return;
            }
            e.preventDefault();
            const paste = (e.clipboardData || window.clipboardData).getData('text');
            ensurePhoneInputMeta(t);
            t.value = formatPhoneInputValue(paste);
        },
        true
    );

    document.addEventListener(
        'keydown',
        (e) => {
            const t = e.target;
            if (!isPhoneMaskTarget(t)) {
                return;
            }
            if (
                [8, 9, 27, 13, 46].indexOf(e.keyCode) !== -1 ||
                (e.keyCode === 65 && e.ctrlKey) ||
                (e.keyCode === 67 && e.ctrlKey) ||
                (e.keyCode === 86 && e.ctrlKey) ||
                (e.keyCode === 88 && e.ctrlKey) ||
                (e.keyCode >= 35 && e.keyCode <= 40)
            ) {
                return;
            }
            if ((e.keyCode < 48 || e.keyCode > 57) && (e.keyCode < 96 || e.keyCode > 105)) {
                e.preventDefault();
            }
        },
        true
    );
}

/** После динамической подмены форм (clone) — проставить meta на новых input */
function refreshPhoneFieldMeta() {
    document.querySelectorAll('input[type="tel"], input[name="phone"]').forEach(ensurePhoneInputMeta);
}
window.refreshPhoneFieldMeta = refreshPhoneFieldMeta;

// Параллакс эффекты
function initParallax() {
    const parallaxElements = document.querySelectorAll('[data-parallax]');

    if (parallaxElements.length === 0) return;

    function updateParallax() {
        const scrollTop = window.pageYOffset;

        parallaxElements.forEach(element => {
            const speed = element.dataset.parallax || 0.5;
            const yPos = -(scrollTop * speed);
            element.style.transform = `translateY(${yPos}px)`;
        });
    }

    // Используем requestAnimationFrame для плавности
    let ticking = false;

    window.addEventListener('scroll', () => {
        if (!ticking) {
            requestAnimationFrame(() => {
                updateParallax();
                ticking = false;
            });
            ticking = true;
        }
    });
}

// Дополнительные утилиты

// Дебаунс функция
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction() {
        const context = this;
        const args = arguments;

        const later = function () {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };

        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

// Проверка видимости элемента
function isElementInViewport(el) {
    const rect = el.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

// Анимация чисел (счетчики)
function animateNumber(element, start, end, duration) {
    const startTime = performance.now();
    const range = end - start;

    // ПРИНУДИТЕЛЬНО УСТАНАВЛИВАЕМ БЕЛЫЙ ЦВЕТ
    element.style.color = '#ffffff !important';
    element.style.fontWeight = '900 !important';

    function updateNumber(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);

        const current = Math.floor(start + (range * progress));
        element.textContent = current.toLocaleString();

        // ПРИНУДИТЕЛЬНО УСТАНАВЛИВАЕМ БЕЛЫЙ ЦВЕТ НА КАЖДОМ КАДРЕ
        element.style.color = '#ffffff !important';
        element.style.fontWeight = '900 !important';

        if (progress < 1) {
            requestAnimationFrame(updateNumber);
        }
    }

    requestAnimationFrame(updateNumber);
}

// Ленивая загрузка изображений
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');

    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    observer.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback для старых браузеров
        images.forEach(img => {
            img.src = img.dataset.src;
        });
    }
}

// Инициализация ленивой загрузки
document.addEventListener('DOMContentLoaded', initLazyLoading);

// Современные функции для нового дизайна
function initModernFeatures() {

    // Кнопка "Заказать звонок" в hero
    const heroCallBtn = document.getElementById('heroCallBtn');
    console.log('Hero call button:', heroCallBtn);
    if (heroCallBtn) {
        heroCallBtn.addEventListener('click', function () {
            console.log('Hero call button clicked!');
            const callModal = document.getElementById('callModal');
            console.log('Call modal:', callModal);
            openModal(callModal);
        });
    }

    // Кнопка "Заказать звонок" под картой
    const mapCallBtn = document.querySelector('.btn-call-modern[data-service="call"]');
    console.log('Map call button:', mapCallBtn);
    if (mapCallBtn) {
        mapCallBtn.addEventListener('click', function () {
            console.log('Map call button clicked!');
            const callModal = document.getElementById('callModal');
            console.log('Call modal:', callModal);
            openModal(callModal);
        });
    }

    // Форма заказа звонка
    const callForm = document.getElementById('callForm');
    if (callForm) {
        callForm.addEventListener('submit', function (e) {
            e.preventDefault();

            if (!validateFormPhone(this)) {
                return;
            }

            const formData = new FormData(this);
            const phoneEl = this.querySelector('input[name="phone"]');
            const data = {
                full_name: (formData.get('full_name') || '').trim(),
                phone: formatRuPhoneForStorage(phoneEl ? phoneEl.value : ''),
                service_type: 'main_page',
                request_type: 'callback',
                agreed_to_processing: this.querySelector('input[name="agreed_to_processing"]')?.checked === true,
            };

            fetch('/ajax/service-application/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                },
                body: JSON.stringify(data)
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        ymReachGoal('call_form');
                        showNotification('Заявка отправлена! Мы свяжемся с вами в ближайшее время.', 'success');
                        closeModal(document.getElementById('callModal'));
                        callForm.reset();
                    } else {
                        showNotification(data.message || 'Произошла ошибка', 'error');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showNotification('Произошла ошибка при отправке', 'error');
                });
        });
    }

    // Кнопка отмены в форме звонка
    const callModalCancel = document.getElementById('callModalCancel');
    if (callModalCancel) {
        callModalCancel.addEventListener('click', function () {
            closeModal(document.getElementById('callModal'));
        });
    }

    // Анимация счетчиков в hero
    animateCounters();

    // Инициализация выпадающего меню
    initDropdownMenu();

    // Инициализация кнопок услуг
    initServiceButtons();
}

// Обработка кнопок услуг
function initServiceButtons() {
    const serviceButtons = document.querySelectorAll('.service-button[data-service]');
    serviceButtons.forEach(button => {
        button.addEventListener('click', function () {
            const service = this.dataset.service;
            const action = this.dataset.action;

            if (action.includes('звонок')) {
                openModal(document.getElementById('callModal'));
            } else {
                showNotification('Функция в разработке. Используйте кнопку "Заказать звонок".', 'info');
            }
        });
    });

    // Универсальный обработчик для всех кнопок "Заказать звонок"
    document.addEventListener('click', function (e) {
        // Обработка кнопок с data-service="call"
        if (e.target.closest('[data-service="call"]')) {
            e.preventDefault();
            const callModal = document.getElementById('callModal');
            if (callModal) {
                openModal(callModal);
            }
        }
    });
}

// Анимация счетчиков
function animateCounters() {
    const counters = document.querySelectorAll('.stat-number[data-count]');

    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.dataset.count);
                animateNumber(counter, 0, target, 2000);
                observer.unobserve(counter);
            }
        });
    }, observerOptions);

    counters.forEach(counter => {
        observer.observe(counter);
    });
}

// Выпадающее меню в навигации
function initDropdownMenu() {
    const dropdown = document.querySelector('.nav-dropdown');
    if (dropdown) {
        const btn = dropdown.querySelector('.nav-dropdown-btn');
        const menu = dropdown.querySelector('.nav-dropdown-menu');

        let timeout;

        dropdown.addEventListener('mouseenter', function () {
            clearTimeout(timeout);
            menu.style.opacity = '1';
            menu.style.visibility = 'visible';
            menu.style.transform = 'translateX(-50%) translateY(0)';
        });

        dropdown.addEventListener('mouseleave', function () {
            timeout = setTimeout(() => {
                menu.style.opacity = '0';
                menu.style.visibility = 'hidden';
                menu.style.transform = 'translateX(-50%) translateY(-10px)';
            }, 150);
        });
    }
}

// Обработка ошибок JavaScript
window.addEventListener('error', function (e) {
    console.error('JavaScript Error:', e.error);
    // Здесь можно отправить ошибку на сервер для логирования
});

// Проверка поддержки современных функций браузера
function checkBrowserSupport() {
    const features = {
        flexbox: CSS.supports('display', 'flex'),
        grid: CSS.supports('display', 'grid'),
        intersectionObserver: 'IntersectionObserver' in window,
        fetch: 'fetch' in window
    };

    // Добавляем классы для условного CSS
    Object.keys(features).forEach(feature => {
        if (features[feature]) {
            document.documentElement.classList.add('supports-' + feature);
        } else {
            document.documentElement.classList.add('no-' + feature);
        }
    });
}

// Инициализация проверки браузера
checkBrowserSupport();

// Постоянный зазор между низом панели «Услуги» и началом контента (панель fixed, место резервируем всегда)
const SERVICES_PANEL_CONTENT_GAP_PX = 8;

/** Высота панели в развёрнутом виде без показа пользователю (чтобы контент не прыгал при open/close) */
function measureServicesDropdownPanelHeight() {
    const panel = document.getElementById('servicesDropdownPanel');
    const wrap = document.querySelector('.header-services-wrap');
    if (!panel) return 0;
    if (wrap && window.getComputedStyle(wrap).display === 'none') {
        return 0;
    }

    const wasOpen = panel.classList.contains('is-open');
    panel.classList.add('is-open');
    panel.style.visibility = 'hidden';
    panel.style.opacity = '0';
    panel.style.pointerEvents = 'none';

    const h = panel.offsetHeight;

    panel.style.visibility = '';
    panel.style.opacity = '';
    panel.style.pointerEvents = '';
    if (!wasOpen) {
        panel.classList.remove('is-open');
    }

    return h;
}

function adjustBodyPadding() {
    const header = document.getElementById('header');
    if (!header) return;
    updateHeaderOffset();
    const bar = header.offsetHeight;
    const panelReserve = measureServicesDropdownPanelHeight();
    const slot = panelReserve + SERVICES_PANEL_CONTENT_GAP_PX;
    document.documentElement.style.setProperty('--services-panel-slot', `${slot}px`);
    document.body.style.paddingTop = `${bar}px`;
}

// Пересчитываем отступ при изменении размера окна
window.addEventListener('resize', debounce(adjustBodyPadding, 250));

// Функция для создания анимированных рамок с Intersection Observer
function initAnimatedBorders() {
    const serviceCards = document.querySelectorAll('.service-card-modern');
    const featureCards = document.querySelectorAll('.feature-card-animated');


    // Современные цвета для анимации
    const colors = ['#3d5ba5', '#6366f1', '#8b5cf6', '#1e1a6b'];

    function animateBorder(element) {
        let colorIndex = 0;
        let direction = 1;

        const animationInterval = setInterval(() => {
            const currentColor = colors[colorIndex];
            element.style.borderColor = currentColor;
            element.style.boxShadow = `0 0 25px ${currentColor}40`;

            colorIndex += direction;
            if (colorIndex >= colors.length - 1) {
                direction = -1;
            } else if (colorIndex <= 0) {
                direction = 1;
            }
        }, 1000);

        // Сохраняем ссылку на интервал для очистки
        element._animationInterval = animationInterval;

        // Очистка при уходе элемента из видимости
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (!entry.isIntersecting && element._animationInterval) {
                    clearInterval(element._animationInterval);
                    element._animationInterval = null;
                }
            });
        });

        observer.observe(element);
    }

    // Intersection Observer для карточек услуг
    const serviceObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target._animationStarted) {
                entry.target._animationStarted = true;
                // Небольшая задержка для плавного появления
                setTimeout(() => {
                    animateBorder(entry.target);
                }, 200);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '50px'
    });

    // Наблюдаем за карточками услуг
    serviceCards.forEach(card => {
        serviceObserver.observe(card);
    });

    // Intersection Observer для блоков преимуществ
    const featureObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target._animationStarted) {
                entry.target._animationStarted = true;
                setTimeout(() => {
                    animateBorder(entry.target);
                }, 300);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '50px'
    });

    // Наблюдаем за блоками преимуществ
    featureCards.forEach(card => {
        featureObserver.observe(card);
    });

    // ПРИНУДИТЕЛЬНЫЙ ЗАПУСК АНИМАЦИИ НА ВСЕХ КАРТОЧКАХ ЧЕРЕЗ 2 СЕКУНДЫ
    setTimeout(() => {
        serviceCards.forEach((card, index) => {
            if (!card._animationStarted) {
                card._animationStarted = true;
                setTimeout(() => {
                    animateBorder(card);
                }, index * 200);
            }
        });
    }, 2000);

    // ДОПОЛНИТЕЛЬНАЯ ПРОВЕРКА ПРИ ПРОКРУТКЕ
    let scrollTimeout;
    window.addEventListener('scroll', () => {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(() => {
            serviceCards.forEach((card, index) => {
                if (!card._animationStarted && isElementInViewport(card)) {
                    card._animationStarted = true;
                    setTimeout(() => {
                        animateBorder(card);
                    }, index * 100);
                }
            });
        }, 100);
    });
}

// 🎨 СОВРЕМЕННЫЕ ИНТЕРАКТИВНЫЕ ЭФФЕКТЫ
function initModernInteractions() {
    // Параллакс мыши для карточек - ОТКЛЮЧЕНО
    // initMouseParallax();

    // Магнитные эффекты для кнопок
    initMagneticButtons();

    // Плавные переходы при загрузке
    initStaggeredAnimations();

    // Интерактивные частицы
    initInteractiveParticles();
}

// Параллакс мыши для карточек - ОТКЛЮЧЕНО
function initMouseParallax() {
    // УБРАНО: ебанутый параллакс который двигает карточки за курсором
}

// Магнитные эффекты для кнопок
function initMagneticButtons() {
    const magneticElements = document.querySelectorAll('.btn-cta-primary, .btn-cta-secondary, .btn-tender');

    magneticElements.forEach(el => {
        el.addEventListener('mousemove', (e) => {
            const rect = el.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;

            el.style.transform = `translate(${x * 0.1}px, ${y * 0.1}px)`;
        });

        el.addEventListener('mouseleave', () => {
            el.style.transform = 'translate(0, 0)';
        });
    });
}

// Поэтапные анимации с Intersection Observer
function initStaggeredAnimations() {
    const elements = document.querySelectorAll('.service-card-modern');

    // Intersection Observer для поэтапных анимаций
    const staggerObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target._staggerAnimationStarted) {
                entry.target._staggerAnimationStarted = true;
                entry.target.classList.add('animate');

                // Добавляем задержку для каскадного эффекта
                const index = Array.from(elements).indexOf(entry.target);
                entry.target.style.animationDelay = `${index * 0.1}s`;
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '50px'
    });

    elements.forEach(el => {
        el.classList.add('animate-on-scroll');
        staggerObserver.observe(el);
    });
}

// Интерактивные частицы
function initInteractiveParticles() {
    const hero = document.querySelector('.hero-simple');
    if (!hero) return;

    // Создаем canvas для частиц
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');

    canvas.style.position = 'absolute';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.pointerEvents = 'none';
    canvas.style.zIndex = '1';

    hero.appendChild(canvas);

    function resizeCanvas() {
        canvas.width = hero.offsetWidth;
        canvas.height = hero.offsetHeight;
    }

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    const particles = [];

    // Создаем частицы
    for (let i = 0; i < 50; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * 2 + 1,
            speedX: (Math.random() - 0.5) * 0.5,
            speedY: (Math.random() - 0.5) * 0.5,
            opacity: Math.random() * 0.5 + 0.2
        });
    }

    function animateParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        particles.forEach(particle => {
            particle.x += particle.speedX;
            particle.y += particle.speedY;

            if (particle.x < 0 || particle.x > canvas.width) particle.speedX *= -1;
            if (particle.y < 0 || particle.y > canvas.height) particle.speedY *= -1;

            ctx.beginPath();
            ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(255, 255, 255, ${particle.opacity})`;
            ctx.fill();
        });

        requestAnimationFrame(animateParticles);
    }

    animateParticles();
}

// Анимации при загрузке страницы
function initPageLoadAnimations() {
    // Анимация счетчиков
    animateCounters();

    // Анимация появления элементов
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    animatedElements.forEach((el, index) => {
        setTimeout(() => {
            el.classList.add('animate');
        }, index * 100);
    });
}

// Оптимизация производительности
function initPerformanceOptimizations() {
    // Throttle для ресайза
    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            // Пересчет позиций элементов
            adjustBodyPadding();
        }, 250);
    });

    // Preload критичных изображений
    const criticalImages = document.querySelectorAll('.logo-img, .hero-simple img');
    criticalImages.forEach(img => {
        if (img.dataset.src) {
            img.src = img.dataset.src;
        }
    });
}

// Современный Intersection Observer
function initIntersectionObserver() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target._intersectionAnimationStarted) {
                entry.target._intersectionAnimationStarted = true;
                entry.target.classList.add('animate');

                // Дополнительные эффекты для разных типов элементов
                if (entry.target.classList.contains('service-card-modern')) {
                    // УБРАНО: принудительное назначение transform чтобы CSS hover работал
                    entry.target.style.transform = '';
                }

                if (entry.target.classList.contains('stat-number')) {
                    // ПРИНУДИТЕЛЬНО УСТАНАВЛИВАЕМ БЕЛЫЙ ЦВЕТ И ЗАПУСКАЕМ АНИМАЦИЮ
                    entry.target.style.color = '#ffffff !important';
                    entry.target.style.fontWeight = '900 !important';

                    const target = parseInt(entry.target.dataset.count);
                    animateNumber(entry.target, 0, target, 2000);
                }
            }
        });
    }, observerOptions);

    // Наблюдаем за всеми анимируемыми элементами
    document.querySelectorAll('.animate-on-scroll, .service-card-modern, .stat-number').forEach(el => {
        observer.observe(el);
    });

    // Дополнительная проверка для карточек услуг - принудительный запуск анимации
    setTimeout(() => {
        const serviceCards = document.querySelectorAll('.service-card-modern');
        serviceCards.forEach(card => {
            if (!card._intersectionAnimationStarted && isElementInViewport(card)) {
                card._intersectionAnimationStarted = true;
                card.classList.add('animate');
            }
        });
    }, 1000);
}
