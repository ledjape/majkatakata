# majkatakata.com

Live site: [majkatakata.com](https://majkatakata.com)

A modern, responsive, bilingual web platform for **Baby-Led Weaning (BLW)** and infant nutrition led by Katerina, certified BLW instructor and Solid Starts representative in North Macedonia.

---

## 🚀 Tech Stack & Architecture

- **Frontend**: HTML5, Vanilla JavaScript (ES6+), custom CSS3 design system
- **Internationalization (i18n)**: Native bilingual support (**Macedonian `mk`** primary, **English `en`** secondary) via [`js/i18n.js`](js/i18n.js)
- **Form Handling**: Integrated with [FormSubmit](https://formsubmit.co/) for community member registrations, processed via asynchronous AJAX calls with interactive modal feedback ([`js/script.js`](js/script.js))
- **Assets & Branding**: Custom SVG brand system with adaptive desktop (`logo_horizontal.svg`) and mobile (`logo_badge.svg`) logo switching
- **Hosting & CI/CD**: GitHub Pages deployed automatically via GitHub Actions ([`.github/workflows/deploy.yml`](.github/workflows/deploy.yml))
- **SEO & Social Sharing**: Open Graph meta tags and semantic HTML structure

---

## 📁 Project Structure

```
├── .github/workflows/
│   └── deploy.yml            # GitHub Actions deployment workflow for GitHub Pages
├── css/
│   └── styles.css            # Custom responsive design system, typography, & component styles
├── js/
│   ├── i18n.js               # Translation dictionaries (MK / EN) & i18n switcher logic
│   └── script.js             # Navigation, smooth scroll, form validation & submit handling
├── resources/img/            # Brand imagery, photos, and responsive SVG logo assets
├── CNAME                     # Custom domain configuration (majkatakata.com)
├── index.html                # Main single-page application
└── README.md                 # Project documentation
```

---

## 🌐 Content & Translation Updates

- **Adding / Modifying Translations**: Update the dictionaries in [`js/i18n.js`](js/i18n.js). Use `data-i18n="key_name"` attributes on HTML elements in [`index.html`](index.html) to bind text.
- **Instagram Posts**: Update Instagram embed `<blockquote>` containers or post URLs inside the `#instagram` section of [`index.html`](index.html).
- **Form Configuration**: Form endpoint settings and submission redirect paths (`_next`) are managed within the `#connect` form in [`index.html`](index.html) and handled in [`js/script.js`](js/script.js).

---

## 🚢 Deployment & Domain Setup

### Deployment
Pushes to the `main` branch trigger the automated GitHub Actions workflow (`.github/workflows/deploy.yml`), which builds and publishes the artifact to GitHub Pages.

### Domain Configuration
Custom domain is managed via Route 53 DNS pointing to GitHub Pages:
- **A Records (@)**:
  - `185.199.108.153`
  - `185.199.109.153`
  - `185.199.110.153`
  - `185.199.111.153`
- **CNAME (www)**: `ledjape.github.io`
