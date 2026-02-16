from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from .models import Account, Transaction, Beneficiary
from .services import deposit, withdraw


# ---------------- DASHBOARD ---------------- #

@login_required
def customer_dashboard(request):
    account = Account.objects.filter(user=request.user).first()

    context = {
        "name": request.user.get_full_name(),   # ✅ Full Name
        "balance": account.balance if account else 0,
        "account_number": account.account_number if account else "Not Available",
    }

    return render(request, "customer_dashboard.html", context)


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


# ---------------- DEPOSIT ---------------- #

@login_required
def deposit_view(request):
    account = Account.objects.get(user=request.user)

    if request.method == "POST":
        amount = request.POST.get("amount")
        message = deposit(account, amount)
        account.refresh_from_db()

        return render(request, "deposit.html", {
            "account": account,
            "message": message
        })

    return render(request, "deposit.html", {"account": account})


# ---------------- WITHDRAW ---------------- #

@login_required
def withdraw_view(request):
    account = Account.objects.get(user=request.user)

    if request.method == "POST":
        amount = request.POST.get("amount")
        message = withdraw(account, amount)
        account.refresh_from_db()

        return render(request, "withdraw.html", {
            "account": account,
            "message": message
        })

    return render(request, "withdraw.html", {"account": account})


# ---------------- TRANSFER ---------------- #

@login_required
def transfer_view(request):
    account = Account.objects.get(user=request.user)
    beneficiaries = Beneficiary.objects.filter(account=account)

    if request.method == "POST":
        beneficiary_id = request.POST.get("beneficiary")
        amount = Decimal(request.POST.get("amount"))

        beneficiary = Beneficiary.objects.get(id=beneficiary_id)

        if account.balance < amount:
            messages.error(request, "Insufficient balance.")
            return redirect("corebank:transfer")

        account.balance -= amount
        beneficiary.beneficiary_account.balance += amount

        account.save()
        beneficiary.beneficiary_account.save()

        Transaction.objects.create(
            account=account,
            transaction_type="Transfer",
            amount=amount,
            method="Online"
        )

        messages.success(request, "Transfer Successful!")
        return redirect('customer_dashboard')


    return render(request, "transfer.html", {
        "beneficiaries": beneficiaries,
        "balance": account.balance
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
