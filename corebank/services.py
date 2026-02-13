from decimal import Decimal
from django.db import transaction
from .models import Transaction, Beneficiary
from accounts.models import Account
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
        account.balance += amount
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

    if account.balance < amount:
        return "Insufficient Balance ❌"

    with transaction.atomic():
        account.balance -= amount
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

    # 1️⃣ OTP check
    if not otp_verified:
        return "OTP Verification Required"

    # 2️⃣ Account status
    if sender.status != "Active":
        return "Account Blocked"

    # 3️⃣ Amount validation
    if amount <= 0:
        return "Invalid Amount"

    # 4️⃣ Get receiver account
    try:
        receiver = Account.objects.get(account_number=receiver_account_number)
    except Account.DoesNotExist:
        return "Receiver Account Not Found"

    # 5️⃣ Beneficiary validation
    if not Beneficiary.objects.filter(
        account=sender,
        beneficiary_account=receiver
    ).exists():
        return "Beneficiary Not Registered"

    # 6️⃣ Balance check
    if sender.balance < amount:
        return "Insufficient Balance"

    # 7️⃣ Daily limit check
    if sender.daily_transfer_used + amount > DAILY_LIMIT:
        return "Daily Transfer Limit Exceeded"

    # 8️⃣ Atomic banking operation
    with transaction.atomic():

        sender.balance -= amount
        receiver.balance += amount
        sender.daily_transfer_used += amount

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
