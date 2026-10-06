from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('text/', views.text_page, name='text'),
    path('audio/', views.audio_page, name='audio'),
    path('image/', views.image_page, name='image'),
    path('video/', views.video_page, name='video'),
]