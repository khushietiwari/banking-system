from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    path('register/', views.register, name="register"),
    path('login/', views.login_view, name="login"),

    path('admin-dashboard/', views.admin_dashboard, name="admin_dashboard"),
    path('employee-dashboard/', views.employee_dashboard, name="employee_dashboard"),
    path('customer-dashboard/', views.customer_dashboard, name="customer_dashboard"),
    path('verify-otp/', views.verify_otp, name="verify_otp"),
    path('verify-kyc/', views.verify_kyc, name='verify_kyc'),
    path('approve-kyc/<int:kyc_id>/', views.approve_kyc, name='approve_kyc'),
    path('loans/', views.loan_list, name='loan_list'),
    path('approve-loan/<int:loan_id>/', views.approve_loan, name='approve_loan'),

]
