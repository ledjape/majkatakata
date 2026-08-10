/* ==========================================================================
   majkatakata.com - Interactive Logic & Localization (i18n) Handler
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Language Switcher (Primary: Macedonian 'mk', Secondary: English 'en')
  let currentLang = localStorage.getItem('majkatakata_lang') || 'mk';

  function applyLanguage(lang) {
    if (!translations[lang]) return;
    currentLang = lang;
    localStorage.setItem('majkatakata_lang', lang);
    document.documentElement.lang = lang;

    const dict = translations[lang];

    // Update innerHTML / textContent for data-i18n
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (dict[key] !== undefined) {
        el.innerHTML = dict[key];
      }
    });

    // Update placeholders for data-i18n-placeholder
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
      const key = el.getAttribute('data-i18n-placeholder');
      if (dict[key] !== undefined) {
        el.setAttribute('placeholder', dict[key]);
      }
    });

    // Update language toggle buttons active state
    document.querySelectorAll('.lang-btn').forEach(btn => {
      if (btn.getAttribute('data-lang') === lang) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });
  }

  // Initialize Language
  applyLanguage(currentLang);

  // Language Switcher Toggle Click Listener
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const lang = btn.getAttribute('data-lang');
      applyLanguage(lang);
    });
  });

  // 2. Mobile Navigation Toggle
  const mobileToggle = document.getElementById('mobileToggle');
  const navLinks = document.getElementById('navLinks');

  if (mobileToggle && navLinks) {
    mobileToggle.addEventListener('click', () => {
      navLinks.classList.toggle('active');
      const isExpanded = navLinks.classList.contains('active');
      mobileToggle.setAttribute('aria-expanded', isExpanded);
      mobileToggle.innerHTML = isExpanded ? '✕' : '☰';
    });

    // Close menu when clicking a link
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('active');
        mobileToggle.innerHTML = '☰';
      });
    });
  }

  // 3. Accordion Handler for Concerns Section
  const accordionItems = document.querySelectorAll('.accordion-item');

  accordionItems.forEach(item => {
    const header = item.querySelector('.accordion-header');
    header.addEventListener('click', () => {
      const isActive = item.classList.contains('active');
      
      // Close all other accordion items
      accordionItems.forEach(i => i.classList.remove('active'));

      // Toggle current item
      if (!isActive) {
        item.classList.add('active');
      }
    });
  });

  // 4. Member Sign-In / Contact Form Async Submission via FormSubmit
  const memberForm = document.getElementById('memberForm');
  const formSuccess = document.getElementById('formSuccess');

  if (memberForm) {
    memberForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const name = document.getElementById('memberName').value.trim();
      const email = document.getElementById('memberEmail').value.trim();
      const submitBtn = memberForm.querySelector('button[type="submit"]');

      if (!name || !email) {
        alert(currentLang === 'mk' ? 'Ве молиме внесете ги вашето име и е-пошта.' : 'Please fill in your name and email address.');
        return;
      }

      const originalText = submitBtn.innerHTML;
      submitBtn.disabled = true;
      submitBtn.innerHTML = currentLang === 'mk' ? '⏳ Се испраќа...' : '⏳ Submitting...';

      try {
        const formData = new FormData(memberForm);
        const ajaxUrl = memberForm.action.replace('formsubmit.co/', 'formsubmit.co/ajax/');
        const response = await fetch(ajaxUrl, {
          method: 'POST',
          body: formData,
          headers: {
            'Accept': 'application/json'
          }
        });

        const result = await response.json().catch(() => ({}));

        if (response.ok || result.success === "true" || result.success === true) {
          memberForm.reset();
          submitBtn.style.display = 'none';
          if (formSuccess) {
            formSuccess.innerHTML = currentLang === 'mk'
              ? '🎉 Ви благодариме за пријавата! Вашите податоци се успешно испратени до Катерина.'
              : '🎉 Thank you for signing up! Your registration has been sent to Katerina.';
            formSuccess.style.display = 'block';
            formSuccess.scrollIntoView({ behavior: 'smooth', block: 'center' });
          }
        } else if (result.message && result.message.includes('Activate')) {
          submitBtn.style.display = 'none';
          if (formSuccess) {
            formSuccess.innerHTML = '🎉 Form submitted! Please check inbox to confirm activation.';
            formSuccess.style.display = 'block';
          }
        } else {
          memberForm.submit();
        }
      } catch (err) {
        memberForm.submit();
      }
    });
  }

  // 5. Dynamic Year in Footer
  const yearEl = document.getElementById('year');
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

  // 6. Scroll Header Shadow Effect
  const header = document.querySelector('.site-header');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 20) {
      header.style.boxShadow = '0 4px 20px rgba(45, 38, 35, 0.08)';
    } else {
      header.style.boxShadow = 'none';
    }
  });
});
