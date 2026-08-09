from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.tokens import default_token_generator
# from django.utils.http import urlsafe_base64_decode

from .models import Profile

import re


# ==================================
# SIGNUP
# ==================================

def signup(request):

    # AJAX username check
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        username = request.GET.get(
            'username',
            ''
        ).strip()

        if username:
            exists = User.objects.filter(
                username__iexact=username
            ).exists()

            return JsonResponse({
                'exists': exists
            })

        return JsonResponse({
            'exists': False
        })


    if request.user.is_authenticated:
        return redirect("home")


    if request.method == "POST":


        username = request.POST.get(
            "username",
            ""
        ).strip()


        email = request.POST.get(
            "email",
            ""
        ).strip()


        password = request.POST.get(
            "password",
            ""
        )


        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )


        if not username or not email or not password or not confirm_password:

            messages.error(
                request,
                "Please fill all fields."
            )

            return redirect("signup")



        try:

            validate_email(email)

        except ValidationError:

            messages.error(
                request,
                "Please enter a valid email address."
            )

            return redirect("signup")



        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return redirect("signup")



        if len(password) < 8:

            messages.error(
                request,
                "Password must contain at least 8 characters."
            )

            return redirect("signup")



        if not re.search(r"[A-Z]", password):

            messages.error(
                request,
                "Password must contain one uppercase letter."
            )

            return redirect("signup")



        if not re.search(r"[a-z]", password):

            messages.error(
                request,
                "Password must contain one lowercase letter."
            )

            return redirect("signup")



        if not re.search(r"\d", password):

            messages.error(
                request,
                "Password must contain one number."
            )

            return redirect("signup")



        if not re.search(r"[@$!%*?&#]", password):

            messages.error(
                request,
                "Password must contain one special character."
            )

            return redirect("signup")



        if User.objects.filter(
            username__iexact=username
        ).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return redirect("signup")



        if User.objects.filter(
            email__iexact=email
        ).exists():

            messages.error(
                request,
                "Email already registered."
            )

            return redirect("signup")



        # Profile will be created automatically by signals

        User.objects.create_user(

            username=username,

            email=email,

            password=password

        )



        messages.success(

            request,

            "Account created successfully! Please login."

        )


        return redirect("login")



    return render(
        request,
        "signup.html"
    )



# ==================================
# LOGIN
# ==================================

def user_login(request):

    if request.user.is_authenticated:

        return redirect("home")



    if request.method == "POST":


        username = request.POST.get(
            "username",
            ""
        ).strip()


        password = request.POST.get(
            "password",
            ""
        )



        user = authenticate(

            request,

            username=username,

            password=password

        )



        if user:


            login(
                request,
                user
            )


            messages.success(

                request,

                f"Welcome back, {user.username}!"

            )


            return redirect("home")



        messages.error(

            request,

            "Invalid username or password."

        )


    return render(
        request,
        "login.html"
    )



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
# PROFILE VIEW
# ==================================

@login_required
def profile_view(request):


    profile, created = Profile.objects.get_or_create(

        user=request.user

    )


    return render(

        request,

        "profile.html",

        {

            "profile": profile,

            "user": request.user

        }

    )



# ==================================
# UPDATE PROFILE
# ==================================

@login_required
def update_profile(request):


    profile, created = Profile.objects.get_or_create(

        user=request.user

    )



    if request.method == "POST":


        request.user.first_name = request.POST.get(

            "first_name",

            ""

        )


        request.user.last_name = request.POST.get(

            "last_name",

            ""

        )


        request.user.email = request.POST.get(

            "email",

            ""

        )


        request.user.save()



        profile.location = request.POST.get(

            "location",

            ""

        )


        profile.phone = request.POST.get(

            "phone",

            ""

        )


        profile.bio = request.POST.get(

            "bio",

            ""

        )



        if request.FILES.get("avatar"):

            profile.avatar = request.FILES["avatar"]



        profile.save()



        messages.success(

            request,

            "Profile updated successfully."

        )



        return redirect("profile")



    return redirect("profile")