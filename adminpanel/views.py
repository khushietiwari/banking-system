from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum

from corebank.models import Account, Transaction, Loan, KYC
from accounts.models import UserProfile


# ADMIN ACCESS CONTROL
from django.http import HttpResponseForbidden

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, "profile") and request.user.profile.role.lower() == "admin":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You are not authorized to access this page.")
    return wrapper

# ADMIN DASHBOARD

@admin_required
def admin_dashboard(request):

    context = {
        "total_users": User.objects.count(),
        "total_accounts": Account.objects.count(),
        "active_accounts": Account.objects.filter(status="Active").count(),
        "blocked_accounts": Account.objects.filter(status="Blocked").count(),
        "pending_loans": Loan.objects.filter(status="Pending").count(),
        "pending_kyc": KYC.objects.filter(status="Pending").count(),
        "total_transactions": Transaction.objects.count(),
    }

    return render(request, "adminpanel/dashboard.html", context)



#  MANAGE USERS


@admin_required
def manage_customers(request):
    customers = User.objects.filter(is_superuser=False).select_related("profile")
    return render(request, "adminpanel/manage_customers.html", {"customers": customers})


@admin_required
def delete_customer(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not user.is_superuser:
        user.delete()
        messages.success(request, "Customer deleted successfully.")
    else:
        messages.error(request, "Cannot delete superuser.")
    return redirect('manage_customers')


# MANAGE ACCOUNTS


@admin_required
def manage_accounts(request):
    accounts = Account.objects.select_related("user").all()
    return render(request, "adminpanel/manage_accounts.html", {"accounts": accounts})


@admin_required
def block_account(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    account.status = "Blocked"
    account.save()
    messages.success(request, "Account blocked successfully.")
    return redirect("manage_accounts")


@admin_required
def activate_account(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    account.status = "Active"
    account.save()
    messages.success(request, "Account activated successfully.")
    return redirect("manage_accounts")



# MANAGE TRANSACTIONS


@admin_required
def manage_transactions(request):
    transactions = Transaction.objects.select_related("account").order_by("-created_at")
    return render(request, "adminpanel/manage_transactions.html", {
        "transactions": transactions
    })


@admin_required
def update_transaction_status(request, txn_id, action):
    txn = get_object_or_404(Transaction, id=txn_id)
    if action == "approve" and txn.status == "Pending":
       txn.status = "Approved"
       txn.save()
       messages.success(request, "Transaction approved.")
    elif action == "reject" and txn.status == "Pending":
       txn.status = "Rejected"
       txn.save()
       messages.success(request, "Transaction rejected.")
    return redirect('manage_transactions')


@admin_required
def approve_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    transaction.status = "Approved"
    transaction.save()
    messages.success(request, "Transaction approved.")
    return redirect("manage_transactions")


@admin_required
def reject_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    transaction.status = "Rejected"
    transaction.save()
    messages.success(request, "Transaction rejected.")
    return redirect("manage_transactions")



# LOAN MANAGEMENT


@admin_required
def manage_loans(request):
    loans = Loan.objects.select_related("user").all()
    return render(request, "adminpanel/manage_loans.html", {"loans": loans})


@admin_required
def update_loan_status(request, loan_id, action):
    loan = get_object_or_404(Loan, id=loan_id)
    if action == "approve" and loan.status == "Pending":
        loan.status = "Approved"
        # Credit amount to user account
        account = loan.user.account
        account.balance += loan.amount
        account.save()
        Transaction.objects.create(
            account=account,
            transaction_type="Loan Disbursal",
            amount=loan.amount,
            method="System",
            status="Approved"
        )
        loan.save()
        messages.success(request, "Loan Approved and Disbursed.")
    elif action == "reject":
        loan.status = "Rejected"
        loan.save()
        messages.success(request, "Loan Rejected.")
    return redirect('manage_loans')


@admin_required
def approve_loan(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    loan.status = "Approved"
    loan.save()
    messages.success(request, "Loan approved successfully.")
    return redirect("manage_loans")


@admin_required
def reject_loan(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    loan.status = "Rejected"
    loan.save()
    messages.success(request, "Loan rejected.")
    return redirect("manage_loans")



# KYC MANAGEMENT


@admin_required
def manage_kyc(request):
    kycs = KYC.objects.select_related("user").all()
    return render(request, "adminpanel/manage_kyc.html", {"kycs": kycs})


@admin_required
def update_kyc_status(request, user_id, action):
    kyc = get_object_or_404(KYC, user__id=user_id)
    if action == "approve":
        kyc.status = "Approved"
        messages.success(request, "KYC Approved.")
    elif action == "reject":
        kyc.status = "Rejected"
        messages.success(request, "KYC Rejected.")
    kyc.save()
    return redirect('manage_kyc')


@admin_required
def approve_kyc(request, kyc_id):
    kyc = get_object_or_404(KYC, id=kyc_id)
    kyc.status = "Approved"
    kyc.save()
    messages.success(request, "KYC approved successfully.")
    return redirect("manage_kyc")


@admin_required
def reject_kyc(request, kyc_id):
    kyc = get_object_or_404(KYC, id=kyc_id)
    kyc.status = "Rejected"
    kyc.save()
    messages.success(request, "KYC rejected.")
    return redirect("manage_kyc")


# STAFF MANAGEMENT

@admin_required
def manage_staff(request):
    staff_members = User.objects.filter(is_staff=True, is_superuser=False)
    return render(request, "adminpanel/manage_staff.html", {"staff_members": staff_members})


@admin_required
def update_staff_status(request, user_id, action):
    user = get_object_or_404(User, id=user_id)
    if action == "promote":
        user.is_staff = True
        messages.success(request, f"{user.username} promoted to Staff.")
    elif action == "demote":
        user.is_staff = False
        messages.success(request, f"{user.username} demoted from Staff.")
    user.save()
    return redirect('manage_staff')


#  SYSTEM REPORTS


@admin_required
def system_reports(request):

    total_balance = Account.objects.aggregate(total=Sum("balance"))["total"] or 0

    context = {
        "total_users": User.objects.count(),
        "total_accounts": Account.objects.count(),
        "total_balance": total_balance,

        "total_transactions": Transaction.objects.count(),
        "approved_transactions": Transaction.objects.filter(status="Approved").count(),
        "rejected_transactions": Transaction.objects.filter(status="Rejected").count(),

        "total_loans": Loan.objects.count(),
        "approved_loans": Loan.objects.filter(status="Approved").count(),
        "rejected_loans": Loan.objects.filter(status="Rejected").count(),
    }

    return render(request, "adminpanel/reports.html", context)
