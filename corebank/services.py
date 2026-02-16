from decimal import Decimal
from django.db import transaction
from .models import Transaction, Beneficiary
from .models import Account

import uuid

DAILY_LIMIT = Decimal("50000")


# ==========================
# 💰 DEPOSIT
# ==========================
from decimal import Decimal

def deposit(account, amount):
    try:
        amount = Decimal(amount)

        if amount <= 0:
            return "Amount must be greater than zero."

        account.balance += amount
        account.save()

        return "Deposit successful."

    except Exception:
        return "Invalid amount."



# ==========================
# 💸 WITHDRAW
# ==========================

def withdraw(account, amount):
    try:
        amount = Decimal(amount)

        if amount <= 0:
            return "Amount must be greater than zero."

        if amount > account.balance:
            return "Insufficient balance."

        account.balance -= amount
        account.save()

        return "Withdrawal successful."

    except Exception:
        return "Invalid amount."



# ==========================
# 🔁 TRANSFER
# ==========================
def transfer(sender, receiver_account_number, amount, otp_verified=True):

    amount = Decimal(amount)

    if not otp_verified:
        return "OTP Verification Required"

    if sender.status != "Active":
        return "Account Blocked"

    if amount <= 0:
        return "Invalid Amount"

    try:
        receiver = Account.objects.get(account_number=receiver_account_number)
    except Account.DoesNotExist:
        return "Receiver Account Not Found"

    if not Beneficiary.objects.filter(
        account=sender,
        beneficiary_account=receiver
    ).exists():
        return "Beneficiary Not Registered"

    if Decimal(sender.balance) < amount:   # ✅ SAFE CHECK
        return "Insufficient Balance"

    if Decimal(sender.daily_transfer_used) + amount > DAILY_LIMIT:
        return "Daily Transfer Limit Exceeded"

    with transaction.atomic():

        sender.balance -= float(amount)   # ✅ FIX
        receiver.balance += float(amount)
        sender.daily_transfer_used += float(amount)

        sender.save()
        receiver.save()

        reference = str(uuid.uuid4())[:10]

        Transaction.objects.create(
            account=sender,
            transaction_type="Transfer Sent",
            amount=amount,
            reference_id=reference,
            method="IMPS"
        )

        Transaction.objects.create(
            account=receiver,
            transaction_type="Transfer Received",
            amount=amount,
            reference_id=reference,
            method="IMPS"
        )

    return "Transfer Successful ✅"
