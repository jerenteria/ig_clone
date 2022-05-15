from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('home', views.success),
    path('create_user', views.register),
    path('login', views.login),
    path('terms_conditions', views.terms_conditions),
    path('upload_pic', views.image_upload_view),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)