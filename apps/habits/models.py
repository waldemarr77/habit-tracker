from django.db import models
from django.conf import settings

class Habit(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Щодня'),
        ('weekly', 'Щотижня'),
        ('custom', 'Вибрані дні'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habit',
        verbose_name='Користувач'
    )

    title = models.CharField(max_length=200, verbose_name='Назва')
    description = models.TextField(blank=True, verbose_name='Опис')
    color = models.CharField(max_length=7, default='#6C63FF', verbose_name='Колір')
    icon = models.CharField(max_length=10, default='✅', verbose_name='Іконка')
    frequency = models.CharField(
        max_length=10,
        choices=FREQUENCY_CHOICES,
        default='daily',
        verbose_name='Частота'
    )

    target_days = models.JSONField(
        default=list,
        verbose_name='Цільові дні тижня'
    )

    is_active = models.BooleanField(default=True, verbose_name='Активна')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Звичка'
        verbose_name_plural = 'Звички'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.icon} {self.title}'