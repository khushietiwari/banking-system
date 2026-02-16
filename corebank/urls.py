from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.customer_dashboard, name="customer_dashboard"),
    path('view-balance/', views.view_balance, name="view_balance"),
    path('transfer/', views.transfer_view, name="transfer"),
    path('transactions/', views.transaction_history, name="transaction_history"),
    path('pay-bills/', views.pay_bills, name="pay_bills"),
    path('manage-profile/', views.manage_profile, name="manage_profile"),
    path('add-beneficiary/', views.add_beneficiary, name="add_beneficiary"),
]
