from django.db import models
from accounts.models import Account , User
import uuid

class Transaction(models.Model):

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reference_id = models.CharField(max_length=20, unique=True, default=uuid.uuid4)
    method = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Beneficiary(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    beneficiary_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="received_transfers"
    )
    nickname = models.CharField(max_length=50)


    def __str__(self):
        return self.nickname

class Account(models.Model):
    user = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    related_name="corebank_account"
)
