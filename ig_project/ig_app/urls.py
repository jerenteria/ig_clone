from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('home', views.success),
    path('create_user', views.register),
    path('login', views.login),
    path('terms_conditions', views.terms_conditions),
    path('upload', views.upload),
]