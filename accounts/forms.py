from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm as DjangoPasswordChangeForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username',
            'institutional_email',
            'student_id',
            'first_name',
            'last_name',
            'career',
            'password1',
            'password2',
        )

    def clean_institutional_email(self):
        email = (self.cleaned_data.get('institutional_email') or '').strip().lower()
        if email and not (email.endswith('.edu.co') or email.endswith('.edu')):
            raise ValidationError("El correo debe ser institucional (.edu.co o .edu).")
        return email

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        if not student_id:
            raise ValidationError("El Código Estudiantil es obligatorio.")
        qs = User.objects.filter(student_id=student_id)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Este número ya está registrado.")
        return student_id

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'institutional_email', 'career', 'student_id']
        # ajusta según lo que permitas editar en perfil

    def clean_institutional_email(self):
        email = (self.cleaned_data.get('institutional_email') or '').strip().lower()
        if email and not (email.endswith('.edu.co') or email.endswith('.edu')):
            raise ValidationError("El correo debe ser institucional (.edu.co o .edu).")
        return email

class PasswordChangeForm(DjangoPasswordChangeForm):
    pass
    