from django.urls import path
from . import views

urlpatterns = [

    path('transfer/', views.transfer_view, name="transfer"),
    path('transactions/', views.transaction_history, name="transaction_history"),

    path('pay-bills/', views.pay_bills, name="pay_bills"),
    path('manage-profile/', views.manage_profile, name="manage_profile"),
]
