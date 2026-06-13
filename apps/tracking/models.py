from django.db import models
from apps.habits.models import Habit

class HabitCheckIn(models.Model):
    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name='checkins',
        verbose_name='Звичка'
    )

    date = models.DateField(db_index=True, verbose_name='Дата')
    is_completed = models.BooleanField(default=True, verbose_name='Виконано')
    note = models.TextField(blank=True, verbose_name='Нотатка')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Check-in'
        verbose_name_plural = 'Check-ins'
        unique_together = [('habit', 'date')]
        ordering = ['-date']

    def __str__(self):
        status = '✅' if self.is_completed else '❌'
        return f'{status} {self.habit.title} - {self.date}'