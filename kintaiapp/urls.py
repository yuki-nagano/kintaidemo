from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('dokintai', views.dokintai),
    # test
    path('hello', views.index),
]