#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

python manage.py shell -c "
from django.contrib.auth.models import User
u, created = User.objects.get_or_create(username='ledjape', defaults={'email': 'pejahs@gmail.com', 'is_staff': True, 'is_superuser': True})
u.set_password('K9#mQ2!vL8')
u.is_staff = True
u.is_superuser = True
u.is_active = True
u.save()
print('Superuser ledjape initialized for production')
"
