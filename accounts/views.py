from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
import random
from .models import OTP
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from .utils import create_account
from .models import Account
from django.contrib.auth.decorators import login_required
from .models import KYC

@login_required
def verify_kyc(request):
    pending_kyc = KYC.objects.filter(is_approved=False)
    return render(request, 'verify_kyc.html', {'kyc_list': pending_kyc})


def role_required(required_role):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.userprofile.role != required_role:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def home(request):
    return render(request, "home.html")
def register(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        role = request.POST['role']

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        user.userprofile.role = role
        user.userprofile.save()

        # 💳 CREATE ACCOUNT ONLY FOR CUSTOMER 😏🔥
        if role == "Customer":
            create_account(user)

        return redirect('login')

    return render(request, "register.html")

@login_required
@role_required("Admin")
def admin_dashboard(request):
    return render(request, "admin_dashboard.html")
def login_view(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:

            login(request, user)

            generate_otp(user)

            return redirect('verify_otp')

        else:

            return render(request, "login.html", {
                "error": "Invalid Credentials ❌"
            })

    return render(request, "login.html")


@login_required
@role_required("Employee")
def employee_dashboard(request):
    return render(request, "employee_dashboard.html")


@login_required
@role_required("Customer")
def customer_dashboard(request):

    account = Account.objects.get(user=request.user)

    return render(request, "customer_dashboard.html", {
        "account": account
    })

def generate_otp(user):

    otp = random.randint(100000, 999999)

    OTP.objects.create(
        user=user,
        otp_code=otp
    )

    print("Sending OTP to:", user.email)   # DEBUG LINE 🔥

    send_mail(
        'Your OTP Code',
        f'Your OTP is {otp}',
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )

    return otp

def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST['otp']

        otp_obj = OTP.objects.filter(user=request.user).last()

        if otp_obj:

            expiry_time = otp_obj.created_at + timedelta(seconds=60)

            if timezone.now() > expiry_time:
                return render(request, "verify_otp.html", {
                    "error": "OTP Expired 😢"
                })

            if str(otp_obj.otp_code) == str(entered_otp):
                otp_obj.delete()  # 🔥 Prevent OTP reuse
            return redirect('customer_dashboard')


    return render(request, "verify_otp.html")
    
