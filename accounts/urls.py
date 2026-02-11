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
]
