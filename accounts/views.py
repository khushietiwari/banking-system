from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from .models import OTP
import random
from django.contrib import messages
from corebank.models import Account


def home(request):
    return render(request, "home.html")


def register(request):
    if request.method == "POST":

        full_name = request.POST.get("full_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        role = request.POST.get("role")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        name_parts = full_name.strip().split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )

        # ✅ SET ROLE PROPERLY
        if role == "employee":
            user.is_staff = True
            user.save()

        # Create bank account only for customer
        if role == "customer":
            Account.objects.create(
                user=user,
                account_number=random.randint(1000000000, 9999999999),
                balance=0.0
            )

        messages.success(request, "Account created successfully.")
        return redirect("login")

    return render(request, "register.html")



def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            generate_otp(user)
            return redirect('verify_otp')

        return render(request, "login.html", {
            "error": "Invalid Credentials ❌"
        })

    return render(request, "login.html")


def generate_otp(user):
    otp = random.randint(100000, 999999)

    OTP.objects.create(
        user=user,
        otp_code=str(otp)
    )

    send_mail(
        'Your OTP Code',
        f'Your OTP is {otp}',
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )


@login_required
def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST['otp']
        otp_obj = OTP.objects.filter(user=request.user).last()

        if otp_obj:
            expiry_time = otp_obj.created_at + timedelta(seconds=60)

            if timezone.now() > expiry_time:
                return render(request, "verify_otp.html", {
                    "error": "OTP Expired"
                })

            if otp_obj.otp_code == entered_otp:
                otp_obj.delete()

                # ✅ Role-based redirection
                if request.user.is_staff:
                    return redirect('employee_dashboard')
                else:
                    return redirect('customer_dashboard')

        return render(request, "verify_otp.html", {
            "error": "Invalid OTP"
        })

    return render(request, "verify_otp.html")


def logout_view(request):
    logout(request)
    return redirect('login')
