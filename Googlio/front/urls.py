from django.urls import path

from . import views

urlpatterns = [
    # ex: /front/
    path('', views.index, name='index'),
    # ex: /front/5/dashboard/
    path('<int:question_id>/', views.dashboard, name='dashboard'),
    # ex: /front/5/send/
    path('<int:question_id>/results/', views.send, name='send'),
]
