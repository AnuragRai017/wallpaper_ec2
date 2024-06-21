# images/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.image_list, name='image_list'),
    path('image/<int:pk>/', views.image_detail, name='image_detail'),
    path('upload/', views.image_upload, name='upload_image'),
    path('download/<int:pk>/<int:width>/<int:height>/', views.download_image, name='download_image'),
]
