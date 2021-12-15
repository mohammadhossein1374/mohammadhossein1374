from django.contrib import admin
from django.urls import path, re_path
from django.urls.conf import include
from . import views

app_name = 'management'

urlpatterns = [
    path('car/filter/',views.CarView.as_view(), name='car-filter'),
    path('car/info/', views.CarViewSomeInfo.as_view(), name='car-info'),
    path('car/create/', views.CarCreate.as_view(), name='car-create'),
]