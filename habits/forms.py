from django import forms
from .models import Habit

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'description', 'frequency', 'target_value', 'unit']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }