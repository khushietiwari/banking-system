from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from corebank.models import Account, Transaction, Loan, KYC
from django.contrib import messages

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def admin_dashboard(request):
    total_users = User.objects.filter(is_superuser=False).count()
    total_accounts = Account.objects.count()
    total_balance = Account.objects.aggregate(Sum("balance"))["balance__sum"] or 0
    pending_loans = Loan.objects.filter(status="Pending").count()
    pending_kyc = KYC.objects.filter(status="Pending").count()
    
    # Fetch recent data for "Live" feel
    recent_users = User.objects.filter(is_superuser=False).order_by('-date_joined')[:5]
    recent_transactions = Transaction.objects.all().order_by('-created_at')[:5]

    context = {
        "total_users": total_users,
        "total_accounts": total_accounts,
        "total_balance": total_balance,
        "pending_loans": pending_loans,
        "pending_kyc": pending_kyc,
        "recent_users": recent_users,
        "recent_transactions": recent_transactions,
    }
    return render(request, "admin_dashboard.html", context)

@login_required
@user_passes_test(is_superuser)
def manage_customers(request):
    customers = User.objects.filter(is_superuser=False)
    return render(request, "adminpanel/manage_accounts.html", {"customers": customers})

@login_required
@user_passes_test(is_superuser)
def delete_customer(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not user.is_superuser:
        user.delete()
        messages.success(request, "Customer deleted successfully.")
    else:
        messages.error(request, "Cannot delete superuser.")
    return redirect('manage_customers')

@login_required
@user_passes_test(is_superuser)
def manage_transactions(request):
    transactions = Transaction.objects.all().order_by('-created_at')
    return render(request, "adminpanel/manage_transactions.html", {"transactions": transactions})

@login_required
@user_passes_test(is_superuser)
def update_transaction_status(request, txn_id, action):
    txn = get_object_or_404(Transaction, id=txn_id)
    if action == "approve" and txn.status == "Pending":
       txn.status = "Approved"
       # Logic to update balance if needed (e.g. for held transactions)
       # For now assuming simple status update
       txn.save()
    elif action == "reject" and txn.status == "Pending":
       txn.status = "Rejected"
       # Revert balance if necessary
       txn.save()
    return redirect('manage_transactions')

@login_required
@user_passes_test(is_superuser)
def manage_loans(request):
    loans = Loan.objects.all().order_by('-applied_at')
    return render(request, "adminpanel/manage_loans.html", {"loans": loans})

@login_required
@user_passes_test(is_superuser)
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

@login_required
@user_passes_test(is_superuser)
def manage_kyc(request):
    kyc_requests = KYC.objects.all().order_by('-submitted_at')
    return render(request, "adminpanel/manage_kyc.html", {"kyc_requests": kyc_requests})

@login_required
@user_passes_test(is_superuser)
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

@login_required
@user_passes_test(is_superuser)
def system_reports(request):
    total_users = User.objects.count()
    total_accounts = Account.objects.count()
    total_balance = Account.objects.aggregate(Sum("balance"))["balance__sum"] or 0
    total_transactions = Transaction.objects.count()
    approved_transactions = Transaction.objects.filter(status="Approved").count()
    rejected_transactions = Transaction.objects.filter(status="Rejected").count()
    total_loans = Loan.objects.count()
    approved_loans = Loan.objects.filter(status="Approved").count()
    rejected_loans = Loan.objects.filter(status="Rejected").count()

    context = {
        "total_users": total_users,
        "total_accounts": total_accounts,
        "total_balance": total_balance,
        "total_transactions": total_transactions,
        "approved_transactions": approved_transactions,
        "rejected_transactions": rejected_transactions,
        "total_loans": total_loans,
        "approved_loans": approved_loans,
        "rejected_loans": rejected_loans,
    }
    return render(request, "adminpanel/reports.html", context)
@login_required
@user_passes_test(is_superuser)
def manage_staff(request):
    staff_members = User.objects.filter(is_staff=True, is_superuser=False)
    return render(request, "adminpanel/manage_staff.html", {"staff_members": staff_members})

@login_required
@user_passes_test(is_superuser)
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
