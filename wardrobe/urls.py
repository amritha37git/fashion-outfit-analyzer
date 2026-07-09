from django.urls import path
from . import views

urlpatterns = [
    path('', views.wardrobe, name='wardrobe'),

    path('upload/', views.ai_upload, name='upload'),

    path('ai-upload/', views.ai_upload, name='ai_upload'),

    path('save-ai-item/', views.save_ai_item, name='save_ai_item'),

    path('edit/<int:item_id>/', views.edit_item, name='edit_item'),

    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),
]