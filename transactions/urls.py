from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_server_check, name='serverCheck'),
    path('report/', views.generate_report, name='report')
]
