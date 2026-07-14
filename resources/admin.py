"""
Admin configuration for resources app
"""

from django.contrib import admin
from .models import Resource, ResourceCategory

@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'category', 'is_featured', 'is_active', 'views', 'downloads')
    list_filter = ('resource_type', 'category', 'is_featured', 'is_active', 'published_date')
    search_fields = ('title', 'description', 'author', 'tags')
    readonly_fields = ('views', 'downloads', 'created_at', 'updated_at')
    fieldsets = (
        ('Información Básica', {
            'fields': ('title', 'description', 'resource_type', 'category')
        }),
        ('Contenido', {
            'fields': ('file', 'url', 'thumbnail', 'author')
        }),
        ('Configuración', {
            'fields': ('is_featured', 'is_active', 'tags')
        }),
        ('Estadísticas', {
            'fields': ('views', 'downloads', 'created_at', 'updated_at')
        }),
    )
    actions = ['make_featured', 'make_unfeatured', 'activate', 'deactivate']
    
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f'{queryset.count()} recursos marcados como destacados.')
    make_featured.short_description = "Marcar como destacado"
    
    def make_unfeatured(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, f'{queryset.count()} recursos quitados de destacados.')
    make_unfeatured.short_description = "Quitar de destacados"
    
    def activate(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f'{queryset.count()} recursos activados.')
    activate.short_description = "Activar recursos"
    
    def deactivate(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f'{queryset.count()} recursos desactivados.')
    deactivate.short_description = "Desactivar recursos"