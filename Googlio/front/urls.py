from django.urls import path

from . import views

app_name = 'front'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('send/', views.send, name='send'),
    path('tyGoogle/', views.tyGoogle, name='tyGoogle'),
]
