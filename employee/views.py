from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from corebank.models import Account
from .forms import CustomerForm,CustomerUpdateForm, AccountUpdateForm


def is_employee(user):
    return user.is_staff


from django.db.models import Sum
from corebank.models import Account

from django.db.models import Sum
from corebank.models import Account, Loan, KYC

from corebank.models import Transaction, Loan, KYC

from django.db.models import Sum
from django.contrib.auth.models import User
from corebank.models import Account, Transaction, Loan, KYC

@login_required
@user_passes_test(is_employee)
def employee_dashboard(request):

    total_customers = User.objects.filter(is_staff=False).count()
    total_accounts = Account.objects.count()
    total_balance = Account.objects.aggregate(Sum("balance"))["balance__sum"] or 0

    pending_transactions = Transaction.objects.filter(status="Pending").count()
    pending_loans = Loan.objects.filter(status="Pending").count()
    pending_kyc = KYC.objects.filter(status="Pending").count()

    # Fetch recent activity for "Live Feed"
    recent_transactions = Transaction.objects.all().order_by('-created_at')[:5]
    recent_loans = Loan.objects.all().order_by('-applied_at')[:5]
    recent_kyc = KYC.objects.all().order_by('-submitted_at')[:5]

    return render(request, "employee/dashboard.html", {
        "total_customers": total_customers,
        "total_accounts": total_accounts,
        "total_balance": total_balance,
        "pending_transactions": pending_transactions,
        "pending_loans": pending_loans,
        "pending_kyc": pending_kyc,
        "recent_transactions": recent_transactions,
        "recent_loans": recent_loans,
        "recent_kyc": recent_kyc,
    })



@login_required
@user_passes_test(is_employee)
def customer_list(request):
    customers = User.objects.filter(is_staff=False)
    return render(request, "employee/customer_list.html", {
        "customers": customers
    })


@login_required
@user_passes_test(is_employee)
def create_customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            user = form.save()

            account_number = "PRIME" + str(user.id).zfill(6)

            Account.objects.create(
                user=user,
                account_number=account_number,
                balance=0
            )

            return redirect('customer_list')
    else:
        form = CustomerForm()

    return render(request, "employee/create_customer.html", {
        "form": form
    })


from .forms import CustomerUpdateForm, AccountUpdateForm

@login_required
@user_passes_test(is_employee)
def update_customer(request, user_id):
    user = get_object_or_404(User, id=user_id)
    account = user.account

    user_form = CustomerUpdateForm(request.POST or None, instance=user)
    account_form = AccountUpdateForm(request.POST or None, instance=account)

    if request.method == "POST":
        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()
            return redirect('customer_list')

    return render(request, "employee/update_customer.html", {
        "user_form": user_form,
        "account_form": account_form
    })
from corebank.models import Loan

@login_required
@user_passes_test(is_employee)
def view_loans(request):
    loans = Loan.objects.all()
    return render(request, "employee/loans.html", {"loans": loans})


@login_required
@user_passes_test(is_employee)
def update_loan(request, loan_id, action):
    loan = Loan.objects.get(id=loan_id)

    if action == "approve":
        loan.status = "Approved"

        # Add loan amount to customer balance
        account = loan.user.account
        account.balance += loan.amount
        account.save()

    elif action == "reject":
        loan.status = "Rejected"

    loan.save()

    return redirect("view_loans")
from corebank.models import KYC

@login_required
@user_passes_test(is_employee)
def view_kyc(request):
    kyc_requests = KYC.objects.all()
    return render(request, "employee/kyc_requests.html", {"kyc_requests": kyc_requests})


@login_required
@user_passes_test(is_employee)
def update_kyc(request, user_id, action):
    kyc = KYC.objects.get(user__id=user_id)

    if action == "approve":
        kyc.status = "Approved"
    elif action == "reject":
        kyc.status = "Rejected"

    kyc.save()

    return redirect("view_kyc")
from corebank.models import Transaction
from decimal import Decimal

@login_required
@user_passes_test(is_employee)
def view_transactions(request):
    transactions = Transaction.objects.filter(status="Pending")
    return render(request, "employee/transactions.html", {"transactions": transactions})


@login_required
@user_passes_test(is_employee)
def update_transaction(request, txn_id, action):
    txn = Transaction.objects.get(id=txn_id)

    if action == "approve":
        account = txn.account

        if txn.transaction_type == "Deposit":
            account.balance += txn.amount

        elif txn.transaction_type == "Withdrawal":
            if txn.amount > account.balance:
                txn.status = "Rejected"
                txn.save()
                return redirect("view_transactions")
            account.balance -= txn.amount

        account.save()
        txn.status = "Approved"

    elif action == "reject":
        txn.status = "Rejected"

    txn.save()
    return redirect("view_transactions")
