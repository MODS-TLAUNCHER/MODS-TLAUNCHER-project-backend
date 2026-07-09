from django.db import models
from django.conf import settings

class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="Nombre del Hábito")
    description = models.TextField(blank=True, verbose_name="Descripción")

    FREQUENCY_CHOICES = [
        ('DAILY', 'Diario'),
        ('WEEKLY', 'Semanal'),
    ]

    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='DAILY')
    target_value = models.PositiveIntegerField(default=1)
    unit = models.CharField(max_length=50, default="veces")

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='logs')
    completed_at = models.DateTimeField(auto_now_add=True)
    value = models.PositiveIntegerField(default=1)

    def _str_(self):
        return f"{self.habit.name} - {self.completed_at}"