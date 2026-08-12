/**
 * Theme & Language Manager for majkatakata Django app
 * Supports Dark/Light Mode and Macedonian (Primary) / English bilingual switching.
 */

(function () {
  'use strict';

  const THEME_KEY = 'majkatakata-theme';
  const LANG_KEY = 'majkatakata-lang';

  // --- Theme Management ---
  function getPreferredTheme() {
    const saved = localStorage.getItem(THEME_KEY);
    if (saved === 'dark' || saved === 'light') {
      return saved;
    }
    return 'light';
  }

  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    const metaColorScheme = document.querySelector('meta[name="color-scheme"]');
    if (metaColorScheme) {
      metaColorScheme.setAttribute('content', theme);
    }
    updateThemeToggleBtn(theme);
  }

  function updateThemeToggleBtn(theme) {
    const btn = document.getElementById('theme-toggle');
    if (!btn) return;

    const isDark = theme === 'dark';
    const currentLang = getPreferredLang();
    btn.setAttribute('aria-label', isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode');

    const iconSpan = btn.querySelector('.theme-icon');
    const textSpan = btn.querySelector('.theme-text');

    if (iconSpan) {
      iconSpan.innerHTML = isDark
        ? `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>`
        : `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;
    }

    if (textSpan) {
      if (currentLang === 'mk') {
        textSpan.textContent = isDark ? 'Светла тема' : 'Темна тема';
      } else {
        textSpan.textContent = isDark ? 'Light Mode' : 'Dark Mode';
      }
    }
  }

  function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') || getPreferredTheme();
    const next = current === 'dark' ? 'light' : 'dark';
    localStorage.setItem(THEME_KEY, next);
    setTheme(next);
  }

  // --- Language Management (Primary: Macedonian / Secondary: English) ---
  function getPreferredLang() {
    const saved = localStorage.getItem(LANG_KEY);
    return saved === 'en' ? 'en' : 'mk';
  }

  function setLanguage(lang) {
    const targetLang = lang === 'en' ? 'en' : 'mk';
    localStorage.setItem(LANG_KEY, targetLang);
    document.documentElement.setAttribute('lang', targetLang);

    // Swap text for all elements with data-lang-mk / data-lang-en
    document.querySelectorAll('[data-lang-mk][data-lang-en]').forEach((el) => {
      const text = el.getAttribute(`data-lang-${targetLang}`);
      if (text) {
        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
          el.setAttribute('placeholder', text);
        } else {
          el.textContent = text;
        }
      }
    });

    // Toggle visibility of language block containers
    document.querySelectorAll('.lang-block-mk').forEach((el) => {
      el.style.display = targetLang === 'mk' ? 'block' : 'none';
    });
    document.querySelectorAll('.lang-block-en').forEach((el) => {
      el.style.display = targetLang === 'en' ? 'block' : 'none';
    });

    // Update language switcher button UI
    const langBtn = document.getElementById('lang-toggle');
    if (langBtn) {
      langBtn.textContent = targetLang === 'mk' ? '🇲🇰 MK | EN' : '🇬🇧 EN | MK';
    }

    updateThemeToggleBtn(getPreferredTheme());
  }

  function toggleLanguage() {
    const current = getPreferredLang();
    const next = current === 'mk' ? 'en' : 'mk';
    setLanguage(next);
  }

  // --- AJAX Registration Form Handler ---
  function initAjaxRegistrationForm() {
    const form = document.getElementById('registration-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const btn = document.getElementById('btn-registration-submit');
      const feedback = document.getElementById('registration-feedback');
      const currentLang = getPreferredLang();

      const originalBtnText = btn ? btn.textContent : '';

      if (btn) {
        btn.disabled = true;
        btn.textContent = currentLang === 'mk' ? 'Се испраќа...' : 'Submitting...';
      }

      if (feedback) {
        feedback.style.display = 'none';
        feedback.className = 'form-feedback-banner';
      }

      try {
        const formData = new FormData(form);
        const response = await fetch(window.location.href, {
          method: 'POST',
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json'
          },
          body: formData
        });

        const data = await response.json();

        if (response.ok && data.success) {
          if (feedback) {
            feedback.className = 'form-feedback-banner success';
            feedback.textContent = currentLang === 'mk' 
              ? (data.message_mk || 'Благодариме! Вашата пријава е успешно испратена.')
              : (data.message_en || 'Thank you! Your registration has been submitted successfully.');
            feedback.style.display = 'block';
          }
          form.reset();
        } else {
          if (feedback) {
            feedback.className = 'form-feedback-banner error';
            feedback.textContent = currentLang === 'mk' 
              ? 'Ве молиме проверете ги внесените податоци и обидете се повторно.'
              : 'Please check your inputs and try again.';
            feedback.style.display = 'block';
          }
        }
      } catch (err) {
        console.error('AJAX form submission error:', err);
        if (feedback) {
          feedback.className = 'form-feedback-banner error';
          feedback.textContent = currentLang === 'mk'
            ? 'Настана грешка при испраќањето. Ве молиме обидете се повторно.'
            : 'An error occurred during submission. Please try again.';
          feedback.style.display = 'block';
        }
      } finally {
        if (btn) {
          btn.disabled = false;
          btn.textContent = originalBtnText;
        }
      }
    });
  }

  // Initialize script execution on DOMContentLoaded
  document.addEventListener('DOMContentLoaded', () => {
    const initialTheme = getPreferredTheme();
    setTheme(initialTheme);

    const initialLang = getPreferredLang();
    setLanguage(initialLang);

    initAjaxRegistrationForm();

    const themeBtn = document.getElementById('theme-toggle');
    if (themeBtn) {
      themeBtn.addEventListener('click', toggleTheme);
    }

    const langBtn = document.getElementById('lang-toggle');
    if (langBtn) {
      langBtn.addEventListener('click', toggleLanguage);
    }

    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
      if (!localStorage.getItem(THEME_KEY)) {
        setTheme(e.matches ? 'dark' : 'light');
      }
    });
  });
})();
