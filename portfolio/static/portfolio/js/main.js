document.addEventListener('DOMContentLoaded', () => {
    // Initialiser les icônes
    lucide.createIcons();

    // Gestion du Menu Mobile
    const btnMenuMobile = document.getElementById('mobile-menu-btn');
    const menuMobile = document.getElementById('mobile-menu');
    const iconMenu = document.getElementById('icon-menu');
    const iconX = document.getElementById('icon-x');

    if (btnMenuMobile && menuMobile) {
        btnMenuMobile.addEventListener('click', () => {
            menuMobile.classList.toggle('hidden');
            iconMenu.classList.toggle('hidden');
            iconX.classList.toggle('hidden');
        });
    }

    // Protection de l'email contre les robots (obfuscation)
    const emailSpan = document.getElementById('contact-email-text');
    const emailLink = document.getElementById('contact-email');

    if (emailSpan && emailLink) {
        // Reconstitution dynamique de l'email
        const user = 'abdelemfossa';
        const domain = 'gmail.com';
        const secureEmail = user + '@' + domain;

        emailSpan.textContent = secureEmail;
        emailLink.href = 'mailto:' + secureEmail;
    }

    // Gestion Dark Mode
    const themeToggleBtn = document.getElementById('theme-toggle');
    const themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
    const themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');

    if (themeToggleBtn && themeToggleDarkIcon && themeToggleLightIcon) {
        // Change les icônes en fonction de l'état actuel
        if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            themeToggleLightIcon.classList.remove('hidden');
        } else {
            themeToggleDarkIcon.classList.remove('hidden');
        }

        // Bascule lors du clic
        themeToggleBtn.addEventListener('click', function () {
            themeToggleDarkIcon.classList.toggle('hidden');
            themeToggleLightIcon.classList.toggle('hidden');

            if (localStorage.getItem('color-theme')) {
                if (localStorage.getItem('color-theme') === 'light') {
                    document.documentElement.classList.add('dark');
                    localStorage.setItem('color-theme', 'dark');
                } else {
                    document.documentElement.classList.remove('dark');
                    localStorage.setItem('color-theme', 'light');
                }
            } else {
                if (document.documentElement.classList.contains('dark')) {
                    document.documentElement.classList.remove('dark');
                    localStorage.setItem('color-theme', 'light');
                } else {
                    document.documentElement.classList.add('dark');
                    localStorage.setItem('color-theme', 'dark');
                }
            }
        });
    }

    // Gestion du bouton Retour en Haut
    const backToTopBtn = document.getElementById('back-to-top');
    if (backToTopBtn) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 400) {
                backToTopBtn.classList.remove('opacity-0', 'translate-y-10', 'invisible');
                backToTopBtn.classList.add('opacity-100', 'translate-y-0', 'visible');
            } else {
                backToTopBtn.classList.add('opacity-0', 'translate-y-10', 'invisible');
                backToTopBtn.classList.remove('opacity-100', 'translate-y-0', 'visible');
            }
        });

        backToTopBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
});

// Disparition du Loader une fois la page chargée
window.addEventListener('load', () => {
    const loader = document.getElementById('page-loader');
    const body = document.getElementById('body-content');

    if (loader) {
        setTimeout(() => {
            loader.classList.add('opacity-0', 'invisible');
            if (body) body.classList.remove('overflow-hidden');
            setTimeout(() => {
                loader.style.display = 'none';
            }, 700);
        }, 500);
    }
});
