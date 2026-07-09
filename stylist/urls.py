from django.urls import path
from . import views

urlpatterns = [
    path('', views.stylist, name='stylist'),
]