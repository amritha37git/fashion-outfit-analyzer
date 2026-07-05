from django.urls import path
from . import views

urlpatterns = [
    path('', views.wardrobe, name='wardrobe'),
    path('upload/', views.upload_item, name='upload'),
]