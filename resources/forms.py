"""
Forms for resources app
"""

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Resource, ResourceCategory

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = [
            'title', 'description', 'resource_type', 'category',
            'file', 'url', 'thumbnail', 'author', 'is_featured',
            'tags'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del recurso'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'resource_type': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://ejemplo.com'}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'etiqueta1, etiqueta2'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='col-md-8'),
                Column('resource_type', css_class='col-md-4'),
            ),
            'description',
            Row(
                Column('category', css_class='col-md-6'),
                Column('author', css_class='col-md-6'),
            ),
            Row(
                Column('file', css_class='col-md-6'),
                Column('url', css_class='col-md-6'),
            ),
            'thumbnail',
            Row(
                Column('is_featured', css_class='col-md-6'),
                Column('tags', css_class='col-md-6'),
            ),
            Submit('submit', 'Guardar Recurso', css_class='btn-success w-100')
        )

class ResourceCategoryForm(forms.ModelForm):
    class Meta:
        model = ResourceCategory
        fields = ['name', 'description', 'icon', 'color']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'fas fa-folder'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Guardar Categoría', css_class='btn-primary'))