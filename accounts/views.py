from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
import re


# ==================================
# SIGNUP
# ==================================

def signup(request):

    # Handle live AJAX request for username availability check
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        username = request.GET.get('username', '').strip()
        if username:
            exists = User.objects.filter(username__iexact=username).exists()
            return JsonResponse({'exists': exists})
        return JsonResponse({'exists': False})

    # Prevent logged-in users from accessing signup
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        # ----------------------------
        # Empty fields
        # ----------------------------

        if not username or not email or not password or not confirm_password:
            messages.error(request, "Please fill all fields.")
            return redirect("signup")

        # ----------------------------
        # Email validation
        # ----------------------------

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Please enter a valid email address.")
            return redirect("signup")

        # ----------------------------
        # Passwords match
        # ----------------------------

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        # ----------------------------
        # Password strength
        # ----------------------------

        if len(password) < 8:
            messages.error(request, "Password must contain at least 8 characters.")
            return redirect("signup")

        if not re.search(r"[A-Z]", password):
            messages.error(request, "Password must contain at least one uppercase letter.")
            return redirect("signup")

        if not re.search(r"[a-z]", password):
            messages.error(request, "Password must contain at least one lowercase letter.")
            return redirect("signup")

        if not re.search(r"\d", password):
            messages.error(request, "Password must contain at least one number.")
            return redirect("signup")

        if not re.search(r"[@$!%*?&#]", password):
            messages.error(request, "Password must contain at least one special character.")
            return redirect("signup")

        # ----------------------------
        # Username exists
        # ----------------------------

        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("signup")

        # ----------------------------
        # Email exists
        # ----------------------------

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect("signup")

        # ----------------------------
        # Create user
        # ----------------------------

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        messages.success(
            request,
            "Account created successfully! Please sign in."
        )

        return redirect("login")

    return render(request, "signup.html")


# ==================================
# LOGIN
# ==================================

def user_login(request):

    # Prevent logged-in users from accessing login
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                f"Welcome back, {user.username}!"
            )

            return redirect("home")

        messages.error(
            request,
            "Invalid username or password."
        )

        return redirect("login")

    return render(request, "login.html")


# ==================================
# LOGOUT
# ==================================

def user_logout(request):

    logout(request)

    messages.success(
        request,
        "Logged out successfully."
    )

    return redirect("landing")


# ==================================
# PASSWORD RESET CONFIRM (CUSTOM)
# ==================================

def custom_password_reset_confirm(request, uidb64=None, token=None):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            new_password1 = request.POST.get("new_password1", "")
            new_password2 = request.POST.get("new_password2", "")

            if not new_password1 or not new_password2:
                messages.error(request, "Please fill in all fields.")
            elif new_password1 != new_password2:
                messages.error(request, "Passwords do not match.")
            elif len(new_password1) < 8:
                messages.error(request, "Password must contain at least 8 characters.")
            elif not re.search(r"[A-Z]", new_password1):
                messages.error(request, "Password must contain at least one uppercase letter.")
            elif not re.search(r"[a-z]", new_password1):
                messages.error(request, "Password must contain at least one lowercase letter.")
            elif not re.search(r"\d", new_password1):
                messages.error(request, "Password must contain at least one number.")
            elif not re.search(r"[@$!%*?&#]", new_password1):
                messages.error(request, "Password must contain at least one special character.")
            else:
                user.set_password(new_password1)
                user.save()
                messages.success(request, "Your password has been successfully reset. You can now log in.")
                return redirect("login")

        return render(request, "password_reset_form.html")
    else:
        messages.error(request, "The password reset link is invalid or has expired.")
        return redirect("password_reset")