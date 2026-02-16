from decimal import Decimal
from django.db import transaction
from .models import Transaction, Beneficiary
from .models import Account

import uuid

DAILY_LIMIT = Decimal("50000")


# ==========================
# 💰 DEPOSIT
# ==========================
def deposit(account, amount):

    amount = Decimal(amount)

    if account.status != "Active":
        return "Account Blocked"

    if amount <= 0:
        return "Invalid Amount"

    with transaction.atomic():

        account.balance += float(amount)   # ✅ FIX
        account.save()

        Transaction.objects.create(
            account=account,
            transaction_type="Deposit",
            amount=amount,
            reference_id=str(uuid.uuid4())[:10]
        )

    return "Deposit Successful ✅"


# ==========================
# 💸 WITHDRAW
# ==========================
def withdraw(account, amount):

    amount = Decimal(amount)

    if account.status != "Active":
        return "Account Blocked"

    if amount <= 0:
        return "Invalid Amount"

    if Decimal(account.balance) < amount:   # ✅ SAFE CHECK
        return "Insufficient Balance ❌"

    with transaction.atomic():

        account.balance -= float(amount)   # ✅ FIX
        account.save()

        Transaction.objects.create(
            account=account,
            transaction_type="Withdrawal",
            amount=amount,
            reference_id=str(uuid.uuid4())[:10]
        )

    return "Withdrawal Successful ✅"


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
