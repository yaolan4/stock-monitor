from os import name
from django.urls import path

from . import views

app_name = "stock_dashboard"
urlpatterns = [
    path('', views.index, name='index'),
    path('chart/', views.detail, name='detail'),
]