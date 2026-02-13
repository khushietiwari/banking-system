from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from .services import deposit
from .models import Transaction


@login_required
def deposit_view(request):

    account = Account.objects.get(user=request.user)

    if request.method == "POST":
        amount = request.POST.get("amount")
        message = deposit(account, amount)

        account.refresh_from_db()  # Important!

        return render(request, "deposit.html", {
            "account": account,
            "message": message
        })

    return render(request, "deposit.html", {
        "account": account
    })
from .services import withdraw

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

    return render(request, "withdraw.html", {
        "account": account
    })

from .services import transfer

@login_required
def transfer_view(request):

    account = Account.objects.get(user=request.user)

    if request.method == "POST":
        receiver_account = request.POST.get("receiver")
        amount = request.POST.get("amount")

        message = transfer(account, receiver_account, amount)

        account.refresh_from_db()

        return render(request, "transfer.html", {
            "account": account,
            "message": message
        })

    return render(request, "transfer.html", {
        "account": account
    })

@login_required
def transaction_history(request):

    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-created_at')


    return render(request, "transactions.html", {
        "transactions": transactions
    })
from .models import Beneficiary
from accounts.models import Account
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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


def customer_dashboard(request):
    try:
        account = Account.objects.get(user=request.user)
    except Account.DoesNotExist:
        account = None

    context = {
        'balance': account.balance if account else 0,
        'account_number': account.account_number if account else 'Not Available',
    }

    return render(request, 'customer_dashboard.html', context)
