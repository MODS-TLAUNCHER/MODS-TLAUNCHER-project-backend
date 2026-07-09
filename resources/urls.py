"""
URLs for resources app
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.resource_list, name='resource_list'),
    path('<int:pk>/', views.resource_detail, name='resource_detail'),
    path('upload/', views.resource_upload, name='resource_upload'),
]