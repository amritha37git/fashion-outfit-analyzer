from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.landing_page,
        name="landing"
    ),
    path(
        "dashboard/",
        views.home,
        name="home"
    ),
    
    # --- ADDED ROUTES ---
    path(
        "profile/",
        views.profile_view,
        name="profile"
    ),
    
    # Optional stub to prevent the "Save Changes" button from crashing
    path(
        "profile/update/",
        views.profile_view, 
        name="profile_update"
    ),
]