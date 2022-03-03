from django.urls import path
from datetime import datetime
from . import views

urlpatterns = [
    path('', views.home),
    path('dokintai', views.dokintai, name='dokintai'),
    path('record', views.record, name='record'),
    path('record/monthly', views.record, name='record/monthly'),
    path('export/csv', views.export_csv, name='export_csv'),
]