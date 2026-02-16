from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from .models import Account, Transaction, Beneficiary
from .services import deposit, withdraw
from .models import Loan
from decimal import Decimal


@login_required
def apply_loan(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        reason = request.POST.get("reason")

        Loan.objects.create(
            user=request.user,
            amount=amount,
            reason=reason
        )

        return redirect("my_loans")

    return render(request, "corebank/apply_loan.html")


@login_required
def my_loans(request):
    loans = Loan.objects.filter(user=request.user)
    return render(request, "corebank/my_loans.html", {"loans": loans})



# ---------------- DASHBOARD ---------------- #

from .models import Account, KYC

from .models import KYC, Loan

@login_required
def customer_dashboard(request):
    account = request.user.account
    kyc = KYC.objects.filter(user=request.user).first()
    loans = Loan.objects.filter(user=request.user)

    return render(request, "customer_dashboard.html", {
        "name": request.user.first_name,
        "balance": account.balance,
        "account_number": account.account_number,
        "ifsc": account.ifsc_code,
        "kyc": kyc,
        "loans": loans
    })


# ---------------- BALANCE ---------------- #

@login_required
def view_balance(request):
    account = Account.objects.filter(user=request.user).first()

    if not account:
        messages.error(request, "Account not found.")
        return redirect('customer_dashboard')


    masked_account = "****" + account.account_number[-4:]

    context = {
        "balance": "{:,.2f}".format(account.balance),
        "account_number": masked_account,
        "ifsc": account.ifsc_code,
    }

    return render(request, "view_balance.html", context)

# ---------------- TRANSFER ---------------- #

from decimal import Decimal
from django.db import transaction

@login_required
def transfer_view(request):
    account = request.user.account
    beneficiaries = Beneficiary.objects.filter(account=account)

    if account.status == "Frozen":
        messages.error(request, "Account is frozen.")
        return redirect("customer_dashboard")

    if not KYC.objects.filter(user=request.user, status="Approved").exists():
        messages.error(request, "Complete KYC to transfer funds.")
        return redirect("customer_dashboard")

    if request.method == "POST":
        beneficiary_id = request.POST.get("beneficiary")
        amount = Decimal(request.POST.get("amount"))

        if amount <= 0:
            messages.error(request, "Invalid amount.")
            return redirect("transfer")

        try:
            beneficiary = Beneficiary.objects.get(id=beneficiary_id)
        except Beneficiary.DoesNotExist:
            messages.error(request, "Invalid beneficiary.")
            return redirect("transfer")

        receiver = beneficiary.beneficiary_account

        if amount > account.balance:
            messages.error(request, "Insufficient balance.")
            return redirect("transfer")

        with transaction.atomic():

            account.balance -= amount
            receiver.balance += amount

            account.save()
            receiver.save()

            reference = str(uuid.uuid4())[:10]

            Transaction.objects.create(
                account=account,
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

        messages.success(request, "Transfer successful.")
        return redirect("customer_dashboard")

    return render(request, "transfer.html", {
        "account": account,
        "beneficiaries": beneficiaries
    })


# ---------------- TRANSACTION HISTORY ---------------- #

@login_required
def transaction_history(request):
    account = Account.objects.get(user=request.user)
    transactions = account.transactions.all().order_by("-created_at")

    return render(request, "transactions.html", {
        "transactions": transactions
    })


# ---------------- BENEFICIARY ---------------- #

@login_required
def add_beneficiary(request):
    account = Account.objects.get(user=request.user)
    message = None

    if request.method == "POST":
        receiver_account_number = request.POST.get("receiver")
        nickname = request.POST.get("nickname")

        try:
            receiver = Account.objects.get(account_number=receiver_account_number)

            if receiver == account:
                message = "You cannot add your own account."

            elif Beneficiary.objects.filter(
                account=account,
                beneficiary_account=receiver
            ).exists():
                message = "Beneficiary already added."

            else:
                Beneficiary.objects.create(
                    account=account,
                    beneficiary_account=receiver,
                    nickname=nickname
                )
                message = "Beneficiary Added Successfully!"

        except Account.DoesNotExist:
            message = "Receiver account not found."

    beneficiaries = Beneficiary.objects.filter(account=account)

    return render(request, "add_beneficiary.html", {
        "beneficiaries": beneficiaries,
        "message": message
    })


@login_required
def pay_bills(request):
    return render(request, "pay_bills.html")


@login_required
def manage_profile(request):
    return render(request, "manage_profile.html")
@login_required
def view_balance(request):
    account = Account.objects.get(user=request.user)

    return render(request, "view_balance.html", {
        "balance": account.balance,
        "account_number": account.account_number
    })
from .models import KYC

@login_required
def upload_kyc(request):
    if request.method == "POST":
        document = request.FILES.get("document")

        KYC.objects.update_or_create(
            user=request.user,
            defaults={"document": document, "status": "Pending"}
        )

        return redirect("kyc_status")

    return render(request, "upload_kyc.html")


@login_required
def kyc_status(request):
    kyc = KYC.objects.filter(user=request.user).first()
    return render(request, "kyc_status.html", {"kyc": kyc})
from .models import Account, Transaction, KYC
from django.contrib import messages


from decimal import Decimal
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction, KYC


# ---------------- DEPOSIT ---------------- #

from decimal import Decimal
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction, KYC

@login_required
def deposit_view(request):
    account = request.user.account

    if account.status == "Frozen":
        messages.error(request, "Account is frozen.")
        return redirect("customer_dashboard")

    if not KYC.objects.filter(user=request.user, status="Approved").exists():
        messages.error(request, "Complete KYC to deposit funds.")
        return redirect("customer_dashboard")

    if request.method == "POST":
        amount = Decimal(request.POST.get("amount"))

        account.balance += amount
        account.save()

        Transaction.objects.create(
            account=account,
            transaction_type="Deposit",
            amount=amount,
            method="Self Deposit"
        )

        messages.success(request, "Deposit successful.")
        return redirect("customer_dashboard")

    return render(request, "deposit.html", {
        "account": account,
        "balance": account.balance   # ✅ THIS WAS MISSING
    })


# ---------------- WITHDRAW ---------------- #

from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Account, Transaction, KYC

@login_required
def withdraw_view(request):
    account = request.user.account

    # Block if frozen
    if account.status == "Frozen":
        messages.error(request, "Account is frozen.")
        return redirect("customer_dashboard")

    # Block if KYC not approved
    if not KYC.objects.filter(user=request.user, status="Approved").exists():
        messages.error(request, "Complete KYC to withdraw funds.")
        return redirect("customer_dashboard")

    if request.method == "POST":
        amount = Decimal(request.POST.get("amount"))

        if amount <= 0:
            messages.error(request, "Invalid amount.")
            return redirect("withdraw")

        if amount > account.balance:
            messages.error(request, "Insufficient balance.")
            return redirect("withdraw")

        account.balance -= amount
        account.save()

        Transaction.objects.create(
            account=account,
            transaction_type="Withdrawal",
            amount=amount,
            method="Self Withdrawal"
        )

        messages.success(request, "Withdrawal successful.")
        return redirect("customer_dashboard")

    return render(request, "withdraw.html", {
        "account": account
    })
