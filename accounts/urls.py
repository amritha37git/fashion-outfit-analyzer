from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

    # Authentication

    path(
        "signup/",
        views.signup,
        name="signup"
    ),

    path(
        "login/",
        views.user_login,
        name="login"
    ),

    path(
        "logout/",
        views.user_logout,
        name="logout"
    ),



    # Password Reset

    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="password_reset.html"
        ),
        name="password_reset"
    ),


    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_sent.html"
        ),
        name="password_reset_done"
    ),


    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_form.html"
        ),
        name="password_reset_confirm"
    ),


    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete"
    ),



    # Profile

    path(
        "profile/",
        views.profile_view,
        name="profile"
    ),


    path(
        "profile/update/",
        views.update_profile,
        name="update_profile"
    ),

]