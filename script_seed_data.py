import os
import django
import random
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ibanking.settings')
django.setup()

from django.contrib.auth.models import User
from corebank.models import Account, Transaction, Beneficiary, Loan, KYC
from accounts.models import UserProfile

def clean_data():
    print("Cleaning old data...")
    Transaction.objects.all().delete()
    Beneficiary.objects.all().delete()
    Loan.objects.all().delete()
    KYC.objects.all().delete()
    Account.objects.all().delete()
    User.objects.exclude(username='admin').delete() # Keep the admin if exists

def create_users():
    print("Creating users...")
    
    # 1. Superuser (if not exists)
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@primetrust.com', 'admin123')
        print(" - Superuser 'admin' created (password: admin123)")

    # 2. Employees
    employees = [
        ('emp1', 'Sarah', 'Connor'),
        ('emp2', 'John', 'Wick')
    ]
    for username, first, last in employees:
        u = User.objects.create_user(username, f'{username}@primetrust.com', 'pass123', first_name=first, last_name=last, is_staff=True)
        # Create UserProfile if needed, though models.py didn't enforce it strictly for login
        print(f" - Employee '{username}' created")

    # 3. Customers
    customers = [
        ('alice', 'Alice', 'Wonderland'),
        ('bob', 'Bob', 'Builder'),
        ('charlie', 'Charlie', 'Chaplin'),
        ('dave', 'Dave', 'Diver'),
        ('eve', 'Eve', 'Polastri')
    ]
    
    for username, first, last in customers:
        u = User.objects.create_user(username, f'{username}@example.com', 'pass123', first_name=first, last_name=last)
        
        # Create Account
        acc_no = f"PRIME{random.randint(100000, 999999)}"
        balance = Decimal(random.randint(5000, 500000))
        acc = Account.objects.create(user=u, account_number=acc_no, balance=balance, status='Active')
        
        # Create KYC
        KYC.objects.create(user=u, status='Approved', document='dummy.pdf')
        
        print(f" - Customer '{username}' created with Balance INR {balance}")

        # Create Transactions
        for _ in range(random.randint(3, 8)):
            tx_type = random.choice(['Deposit', 'Withdrawal', 'Transfer Sent', 'Transfer Received'])
            amount = Decimal(random.randint(100, 5000))
            status = 'Approved'
            
            if tx_type in ['Withdrawal', 'Transfer Sent']:
                acc.balance -= amount
            else:
                acc.balance += amount
            
            Transaction.objects.create(
                account=acc,
                transaction_type=tx_type,
                amount=amount,
                status=status,
                reference_id=f"TXN{random.randint(10000,99999)}",
                method="Online"
            )
        acc.save()

        # Create Loans
        if random.choice([True, False]):
            Loan.objects.create(
                user=u,
                amount=Decimal(random.randint(10000, 500000)),
                reason="Home Renovation",
                status=random.choice(['Pending', 'Approved', 'Rejected'])
            )

    print("Data seeding completed!")

if __name__ == '__main__':
    clean_data()
    create_users()
