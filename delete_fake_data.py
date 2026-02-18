
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ibanking.settings')
django.setup()

from django.contrib.auth.models import User

def delete_fake_users():
    fake_usernames = ['alice', 'bob', 'charlie', 'dave', 'eve', 'user123']
    
    deleted_count = 0
    for username in fake_usernames:
        try:
            user = User.objects.get(username=username)
            user.delete()
            print(f"Deleted user: {username} and all associated data.")
            deleted_count += 1
        except User.DoesNotExist:
            print(f"User {username} not found (already deleted or never existed).")
            
    print(f"\nTotal fake users deleted: {deleted_count}")

if __name__ == "__main__":
    delete_fake_users()
