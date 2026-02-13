from django.urls import path
from . import views

urlpatterns = [
    path('deposit/', views.deposit_view, name='deposit'),
    path('withdraw/', views.withdraw_view, name='withdraw'),
    path('transfer/', views.transfer_view, name='transfer'),
    path('transactions/', views.transaction_history, name='transaction_history'),
    path('add-beneficiary/', views.add_beneficiary, name='add_beneficiary'),



    

]
