# majkatakata.com

Official web platform for **Baby Led Weaning (BLW) со Катерина** — certified BLW instructor and Solid Starts accredited representative in North Macedonia.

🌐 **Live Website**: [https://majkatakata.com](https://majkatakata.com)

---

## 🚀 Tech Stack

- **Backend**: Django 5.2 & Python 3.12 (WSGI / Gunicorn & WhiteNoise)
- **Database**: SQLite3
- **Frontend**: Semantic HTML5, Vanilla JavaScript (ES6+), Custom Responsive CSS Design System (Light/Dark mode)
- **UI/UX & Performance**: Zero-CLS dimensioning, LCP preloading, CSS Grid dynamic accordion, `content-visibility` containment
- **Forms & Security**: Django CSRF, AJAX async submission, multi-layer bot defense (stealth honeypot & time-gate validation)
- **Email Notifications**: Resend HTTPS API (Port 443) with background worker thread & fallback SMTP
- **SEO & Social**: OpenGraph, Twitter Cards, Schema.org JSON-LD Structured Data (`Person` & `LocalBusiness`)
- **i18n**: Bilingual client-side runtime switching — Macedonian (`mk`) Primary / English (`en`) Secondary
- **Hosting & CI/CD**: Render Web Service ([`render.yaml`](render.yaml) & [`build.sh`](build.sh))
- **DNS & SSL**: AWS Route53 & Automated Managed TLS

---

## 🛠 Local Development

```bash
# Activate virtual environment
.\.venv\Scripts\activate

# Run database migrations
python manage.py migrate

# Run local development server
python manage.py runserver
```

---

## 🚢 Deployment

Commits pushed to the `django-web` branch automatically trigger zero-downtime deployments on Render.
