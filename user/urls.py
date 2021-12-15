from django.contrib import admin
from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    # path('create/<int:pk>', views.OwnerCreate.as_view(), name='create'),
    path('list/', views.OwnerView.as_view(), name='list'),
]