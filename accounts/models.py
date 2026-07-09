"""
User model for biUNestar
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.utils import timezone
import hashlib
import os

class User(AbstractUser):
    # Campos adicionales para estudiante
    institutional_email = models.EmailField(
        unique=True,
        validators=[EmailValidator(message="Por favor ingresa un correo institucional válido")]
    )
    student_id = models.CharField(
    max_length=50,
    unique=True,
    verbose_name="Código Estudiantil"
)
    career = models.CharField(
        max_length=100,
        verbose_name="Carrera"
    )
    semester = models.IntegerField(
        default=1,
        verbose_name="Semestre"
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        verbose_name="Teléfono"
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de Nacimiento"
    )
    
    # Campos de seguridad
    password_salt = models.CharField(
        max_length=64,
        blank=True,
        editable=False
    )
    last_password_change = models.DateTimeField(
        auto_now=True,
        verbose_name="Último Cambio de Contraseña"
    )
    
    # Campos de seguimiento
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Registro"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Actualización"
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name="Correo Verificado"
    )

    def clean(self):
        """
        Validaciones de modelo. Levantar ValidationError (no ValueError).
        Preferimos institutional_email si está presente, sino email.
        """
        super().clean()
        # elegir correo a validar (prioriza institutional_email)
        email_to_check = (self.institutional_email or self.email or '').strip().lower()
        if email_to_check and not email_to_check.endswith(('.edu.co', '.edu')):
            # Asociar el error al campo institucional_email para que los ModelForms lo muestren ahí
            raise ValidationError({'institutional_email': "El correo debe ser institucional (.edu.co o .edu)."})
        
        # normalizar ambos campos para evitar inconsistencias
        if self.email:
            self.email = self.email.strip().lower()
        if self.institutional_email:
            self.institutional_email = self.institutional_email.strip().lower()

    def save(self, *args, **kwargs):
        """
        No lanzar errores crudos aquí. Si quieres forzar validación automática,
        podrías llamar a self.full_clean() pero ten en cuenta que eso lanza
        ValidationError si el formulario no la está manejando.
        Aquí nos limitamos a normalizar y a delegar la validación al form/model.clean.
        """
        # normalización adicional por si se invoca save() desde fuera de un form
        if self.email:
            self.email = self.email.lower()
        if self.institutional_email:
            self.institutional_email = self.institutional_email.lower()

        super().save(*args, **kwargs)
    
    def set_password(self, raw_password):
        """Override para incluir salt en el hash de forma correcta"""
        if raw_password is None:
            # comportarnos igual que la implementación por defecto
            super().set_unusable_password()
            return

        if not self.password_salt:
            # generar salt si aún no existe
            self.password_salt = hashlib.sha256(os.urandom(60)).hexdigest()
        
        # concatenar y hashear usando la infraestructura de Django
        salted = f"{raw_password}{self.password_salt}"
        self.password = make_password(salted)
        # actualizar fecha de cambio
        self.last_password_change = timezone.now()

    def check_password(self, raw_password):
        """Verificar contraseña con el mismo esquema (concatenar salt y delegar)"""
        if not self.password_salt:
            return False
        salted = f"{raw_password}{self.password_salt}"
        # delegamos a la implementación estándar que compara con self.password
        return super().check_password(salted)
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.get_full_name()} - {self.student_id}"
