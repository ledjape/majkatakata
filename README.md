# majkatakata.com

Official web platform for **Baby Led Weaning (BLW) со Катерина** — certified BLW instructor and Solid Starts accredited representative in North Macedonia.

🌐 **Live Website**: [https://majkatakata.com](https://majkatakata.com)

---

## 🚀 Tech Stack

- **Backend**: Django 5.2 & Python 3.12
- **Database**: SQLite
- **Frontend**: HTML5, Vanilla JavaScript, Custom CSS Design System
- **i18n**: Macedonian (`mk`) Primary / English (`en`) Secondary
- **Hosting & CI/CD**: Render ([`render.yaml`](render.yaml) & [`build.sh`](build.sh))
- **DNS**: AWS Route53

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
