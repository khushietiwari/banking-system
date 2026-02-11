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
        email = request.POST['email']   # ⭐ ADD THIS
        password = request.POST['password']
        role = request.POST['role']

        user = User.objects.create_user(
            username=username,
            email=email,   # ⭐ ADD THIS
            password=password
        )

        user.userprofile.role = role
        user.userprofile.save()

        return redirect('login')

    return render(request, "register.html")

def login_view(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        try:
            user_obj = User.objects.get(username=username)
            profile = user_obj.userprofile

            if profile.is_locked:
                return render(request, "login.html", {
                    "error": "Account Locked 🔒 Contact Bank"
                })

        except User.DoesNotExist:
            return render(request, "login.html", {
                "error": "Invalid Credentials"
            })

        user = authenticate(username=username, password=password)

        if user:

            profile.failed_attempts = 0
            profile.save()

            login(request, user)

            otp = generate_otp(user)
            print("OTP:", otp)

            return redirect('verify_otp')

        else:

            profile.failed_attempts += 1

            if profile.failed_attempts >= 3:
                profile.is_locked = True

            profile.save()

            return render(request, "login.html", {
                "error": f"Invalid Credentials ({profile.failed_attempts}/3)"
            })

    return render(request, "login.html")
@login_required
@role_required("Admin")
def admin_dashboard(request):
    return render(request, "admin_dashboard.html")


@login_required
@role_required("Employee")
def employee_dashboard(request):
    return render(request, "employee_dashboard.html")


@login_required
@role_required("Customer")
def customer_dashboard(request):
    return render(request, "customer_dashboard.html")

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
                return redirect('customer_dashboard')

    return render(request, "verify_otp.html")

