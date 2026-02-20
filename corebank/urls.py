from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.customer_dashboard, name="customer_dashboard"),
    path('view-balance/', views.view_balance, name="view_balance"),
    path('transfer/', views.transfer_view, name="transfer"),
    path('transactions/', views.transaction_history, name="transaction_history"),
    path('pay-bills/', views.pay_bills, name="pay_bills"),
    path('manage-profile/', views.manage_profile, name="manage_profile"),
    path('edit-profile/', views.edit_profile, name="edit_profile"),
    path('password-change/', views.CustomPasswordChangeView.as_view(), name="password_change"),
    path('add-beneficiary/', views.add_beneficiary, name="add_beneficiary"),
    path('apply-loan/', views.apply_loan, name="apply_loan"),
path('my-loans/', views.my_loans, name="my_loans"),
path('upload-kyc/', views.upload_kyc, name="upload_kyc"),
path('kyc-status/', views.kyc_status, name="kyc_status"),
path('deposit/', views.deposit_view, name="deposit"),
    path('withdraw/', views.withdraw_view, name="withdraw"),
    path('apply-debit-card/', views.apply_debit_card, name="apply_debit_card"),
    path('apply-credit-card/', views.apply_credit_card, name="apply_credit_card"),
    path('card-status/', views.view_card_status, name="view_card_status"),
    path("support/", views.support_view, name="support"),
]
