from django.urls import path
from . import views

urlpatterns = [
    # Dashboard (Página principal)
    path('', views.dashboard, name='dashboard'),

    # CRUD de Hábitos
    path('habits/', views.habit_list, name='habit_list'),
    path('habits/create/', views.habit_create, name='habit_create'),
    path('habits/<int:pk>/edit/', views.habit_update, name='habit_update'),
    path('habits/<int:pk>/log/', views.habit_log, name='habit_log'),

    # Reportes
    path('reports/', views.reports, name='reports'),
]