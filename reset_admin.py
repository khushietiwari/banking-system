import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ibanking.settings')
django.setup()

from django.contrib.auth.models import User

try:
    u = User.objects.get(username='admin')
    u.set_password('admin123')
    u.is_superuser = True
    u.is_staff = True
    u.save()
    print("Admin password reset to 'admin123'")
except User.DoesNotExist:
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Admin user created with password 'admin123'")
