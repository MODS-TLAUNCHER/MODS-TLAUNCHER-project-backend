"""
Resources models for biUNestar
"""

from django.db import models
from django.core.validators import FileExtensionValidator

class ResourceCategory(models.Model):
    """Category for resources"""
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    icon = models.CharField(max_length=50, default='fas fa-folder', verbose_name="Ícono")
    color = models.CharField(max_length=7, default='#6c757d', verbose_name="Color")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Resource(models.Model):
    """Resource model for educational materials"""
    
    RESOURCE_TYPES = [
        ('guide', '📖 Guía'),
        ('video', '🎥 Video'),
        ('link', '🔗 Enlace'),
        ('document', '📄 Documento'),
        ('presentation', '📊 Presentación'),
        ('exercise', '💪 Ejercicio'),
        ('tool', '🛠️ Herramienta'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")
    resource_type = models.CharField(
        max_length=20,
        choices=RESOURCE_TYPES,
        default='document',
        verbose_name="Tipo de Recurso"
    )
    category = models.ForeignKey(
        ResourceCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resources',
        verbose_name="Categoría"
    )
    file = models.FileField(
        upload_to='resources/files/',
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'txt', 'zip'])
        ],
        verbose_name="Archivo"
    )
    url = models.URLField(blank=True, verbose_name="Enlace Externo")
    thumbnail = models.ImageField(
        upload_to='resources/thumbnails/',
        blank=True,
        null=True,
        verbose_name="Miniatura"
    )
    author = models.CharField(max_length=100, blank=True, verbose_name="Autor")
    published_date = models.DateField(auto_now_add=True, verbose_name="Fecha de Publicación")
    is_featured = models.BooleanField(default=False, verbose_name="Destacado")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    views = models.IntegerField(default=0, verbose_name="Visitas")
    downloads = models.IntegerField(default=0, verbose_name="Descargas")
    tags = models.CharField(max_length=200, blank=True, verbose_name="Etiquetas")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")
    
    class Meta:
        verbose_name = "Recurso"
        verbose_name_plural = "Recursos"
        ordering = ['-published_date']
    
    def __str__(self):
        return self.title
    
    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])
    
    def increment_downloads(self):
        self.downloads += 1
        self.save(update_fields=['downloads'])