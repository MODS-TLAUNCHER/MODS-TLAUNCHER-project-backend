"""
Admin configuration for accounts app
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'institutional_email', 'student_id', 'career', 'is_active', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'semester', 'career')
    search_fields = ('username', 'email', 'institutional_email', 'student_id', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'birth_date')
        }),
        ('Información Académica', {
            'fields': ('institutional_email', 'student_id', 'career', 'semester')
        }),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Fechas Importantes', {
            'fields': ('last_login', 'date_joined', 'last_password_change')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'institutional_email', 'student_id', 'password1', 'password2'),
        }),
    )