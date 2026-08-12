import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

try:
    from django.contrib.auth.models import User
    u, created = User.objects.get_or_create(
        username='ledjape',
        defaults={'email': 'pejahs@gmail.com', 'is_staff': True, 'is_superuser': True}
    )
    u.set_password('K9#mQ2!vL8')
    u.is_staff = True
    u.is_superuser = True
    u.is_active = True
    u.save()
    print("WSGI: Superuser ledjape verified and password set.")
except Exception as e:
    print(f"WSGI: Error initializing superuser: {e}")
