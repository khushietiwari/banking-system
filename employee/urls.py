from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.create_customer, name='create_customer'),
    path('customers/update/<int:user_id>/', views.update_customer, name='update_customer'),
    path('loans/', views.view_loans, name="view_loans"),
path('loan-update/<int:loan_id>/<str:action>/', views.update_loan, name="update_loan"),
path('kyc-requests/', views.view_kyc, name="view_kyc"),
path('kyc-update/<int:user_id>/<str:action>/', views.update_kyc, name="update_kyc"),
path('transactions/', views.view_transactions, name="view_transactions"),
path('transaction-update/<int:txn_id>/<str:action>/', views.update_transaction, name="update_transaction"),

    

]
