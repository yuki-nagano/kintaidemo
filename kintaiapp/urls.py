from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dokintai', views.dokintai, name='dokintai'),
    path('record', views.RecordViews, name='record'),
    path('record/monthly', views.RecordViews, name='record/monthly'),
    path('export/csv', views.export_csv, name='export_csv'),
]