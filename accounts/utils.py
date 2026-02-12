import random
from .models import Account

def create_account(user):

    while True:
        acc_num = random.randint(10000000, 99999999)

        if not Account.objects.filter(account_number=acc_num).exists():
            break

    account = Account.objects.create(
        user=user,
        account_number=acc_num
    )

    return account
