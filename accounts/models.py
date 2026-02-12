from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username
class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
class Account(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    account_number = models.IntegerField(unique=True)
    balance = models.FloatField(default=0)
    status = models.CharField(default="Active", max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.account_number)

