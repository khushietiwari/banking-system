import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ibanking.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile

try:
    # Create a dummy user if not exists
    user, created = User.objects.get_or_create(username='test_user_repro')
    if created:
        user.set_password('password')
        user.save()
        # Create profile manually if signal didn't work (but signal should work)
        # Check if profile exists
        if not hasattr(user, 'profile_account') and not hasattr(user, 'userprofile'):
             UserProfile.objects.create(user=user, role='Customer')
    
    print(f"User created/retrieved: {user.username}")
    
    # Try to access userprofile
    try:
        print(f"Accessing user.userprofile: {user.userprofile}")
    except AttributeError as e:
        print(f"Caught expected error: {e}")

    # Try to access profile_account
    try:
        print(f"Accessing user.profile_account: {user.profile_account}")
    except AttributeError as e:
        print(f"Caught error accessing profile_account: {e}")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
