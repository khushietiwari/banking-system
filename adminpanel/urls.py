from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('customers/', views.manage_customers, name='manage_customers'),
    path('transactions/', views.manage_transactions, name='manage_transactions'),
    path('loans/', views.manage_loans, name='manage_loans'),
    path('kyc/', views.manage_kyc, name='manage_kyc'),
    path('reports/', views.system_reports, name='system_reports'),
    path('customer/delete/<int:user_id>/', views.delete_customer, name='delete_customer'),
    path('transaction/<int:txn_id>/<str:action>/', views.update_transaction_status, name='update_transaction_status'),
    path('loan/<int:loan_id>/<str:action>/', views.update_loan_status, name='update_loan_status'),
    path('kyc/<int:user_id>/<str:action>/', views.update_kyc_status, name='update_kyc_status'),
]
