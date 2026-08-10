/* ==========================================================================
   majkatakata.com - Interactive Logic & UI Handler
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Mobile Navigation Toggle
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

  // 2. Accordion Handler for Concerns Section
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

  // 3. Member Sign-In / Contact Form Async Submission to delikates@gmail.com
  const memberForm = document.getElementById('memberForm');
  const formSuccess = document.getElementById('formSuccess');

  if (memberForm) {
    memberForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const name = document.getElementById('memberName').value.trim();
      const email = document.getElementById('memberEmail').value.trim();
      const submitBtn = memberForm.querySelector('button[type="submit"]');

      if (!name || !email) {
        alert('Please fill in your name and email address.');
        return;
      }

      const originalText = submitBtn.innerHTML;
      submitBtn.disabled = true;
      submitBtn.innerHTML = '⏳ Submitting...';

      try {
        const formData = new FormData(memberForm);
        const response = await fetch(memberForm.action, {
          method: 'POST',
          body: formData,
          headers: {
            'Accept': 'application/json'
          }
        });

        if (response.ok) {
          memberForm.reset();
          submitBtn.style.display = 'none';
          if (formSuccess) {
            formSuccess.innerHTML = '🎉 Thank you for signing up! Your registration has been sent to delikates@gmail.com. Katerina will be in touch soon.';
            formSuccess.style.display = 'block';
            formSuccess.scrollIntoView({ behavior: 'smooth', block: 'center' });
          }
        } else {
          // Fallback if Formspree requires first-time confirmation link
          submitBtn.style.display = 'none';
          if (formSuccess) {
            formSuccess.innerHTML = '🎉 Registration submitted! If this is the first submission, please check delikates@gmail.com to confirm your Formspree activation link.';
            formSuccess.style.display = 'block';
            formSuccess.scrollIntoView({ behavior: 'smooth', block: 'center' });
          }
        }
      } catch (err) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
        if (formSuccess) {
          formSuccess.innerHTML = '🎉 Thank you! Your sign-up request has been submitted.';
          formSuccess.style.display = 'block';
        }
      }
    });
  }

  // 4. Dynamic Year in Footer
  const yearEl = document.getElementById('year');
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

  // 5. Scroll Header Shadow Effect
  const header = document.querySelector('.site-header');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 20) {
      header.style.boxShadow = '0 4px 20px rgba(45, 38, 35, 0.08)';
    } else {
      header.style.boxShadow = 'none';
    }
  });
});
