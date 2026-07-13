from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re


# ==================================
# SIGNUP
# ==================================

def signup(request):

    print("SIGNUP VIEW CALLED")

    if request.method == "POST":

        print("POST REQUEST RECEIVED")

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        print("Username:", username)
        print("Email:", email)

        # ----------------------------
        # Empty fields
        # ----------------------------

        if not username or not email or not password or not confirm_password:
            print("FAILED : Empty fields")
            messages.error(request, "Please fill all fields.")
            return redirect("signup")

        # ----------------------------
        # Email validation
        # ----------------------------

        try:
            validate_email(email)

        except ValidationError:
            print("FAILED : Invalid email")
            messages.error(request, "Please enter a valid email address.")
            return redirect("signup")

        # ----------------------------
        # Passwords match
        # ----------------------------

        if password != confirm_password:
            print("FAILED : Password mismatch")
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        # ----------------------------
        # Password strength
        # ----------------------------

        if len(password) < 8:
            print("FAILED : Less than 8 characters")
            messages.error(request, "Password must contain at least 8 characters.")
            return redirect("signup")

        if not re.search(r"[A-Z]", password):
            print("FAILED : Missing uppercase")
            messages.error(request, "Password must contain an uppercase letter.")
            return redirect("signup")

        if not re.search(r"[a-z]", password):
            print("FAILED : Missing lowercase")
            messages.error(request, "Password must contain a lowercase letter.")
            return redirect("signup")

        if not re.search(r"\d", password):
            print("FAILED : Missing number")
            messages.error(request, "Password must contain a number.")
            return redirect("signup")

        if not re.search(r"[@$!%*?&#]", password):
            print("FAILED : Missing special character")
            messages.error(request, "Password must contain a special character.")
            return redirect("signup")

        # ----------------------------
        # Username exists
        # ----------------------------

        if User.objects.filter(username=username).exists():
            print("FAILED : Username exists")
            messages.error(request, "Username already exists.")
            return redirect("signup")

        # ----------------------------
        # Email exists
        # ----------------------------

        if User.objects.filter(email=email).exists():
            print("FAILED : Email exists")
            messages.error(request, "Email already registered.")
            return redirect("signup")

        # ----------------------------
        # Create user
        # ----------------------------

        print("CREATING USER...")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        user.save()

        print("USER CREATED SUCCESSFULLY")

        messages.success(
            request,
            "Account created successfully! Please login."
        )

        print("REDIRECTING TO LOGIN")

        return redirect("/accounts/login/")

    return render(request, "signup.html")


# ==================================
# LOGIN
# ==================================

def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("home")

        else:

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

    return redirect("login")