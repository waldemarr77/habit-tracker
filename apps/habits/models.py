from django.db import models
from django.conf import settings
from django.db.models import Count, Q

class HabitQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)
    
    def for_user(self, user):
        return self.filter(user=user, is_active=True)
    
    def daily(self):
        return self.filter(frequency='daily')
    
    def with_stats(self):
        return self.annotate(
            total_checkins=Count('checkins'),
            completed_checkins=Count(
                'checkins',
                filter=Q(checkins__is_completed=True)
            )
        )

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
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = HabitQuerySet.as_manager()

    class Meta:
        verbose_name = 'Звичка'
        verbose_name_plural = 'Звички'
        ordering = ['order', '-created_at']

    def __str__(self):
        return f'{self.icon} {self.title}'
    
    def __repr__(self):
        return f"<Habit(id={self.id}, user='{self.user.username}', title='{self.title}')>"
    
    def __len__(self):
        return len(self.target_days) if isinstance(self.target_days, list) else 0

    @staticmethod
    def calculate_water_norm(weight):
        if not weight:
            return None, None
        daily_ml = weight * 35
        daily_liters = round(daily_ml / 1000, 1)
        return daily_ml, daily_liters
    
    @classmethod
    def setup_water_norm(cls, user, weight=None):
        daily_ml, daily_liters = cls.calculate_water_norm(weight)

        if daily_ml:
            desc = f'Денна норма: {daily_liters}л ({daily_ml}мл)'
        else:
            desc = 'Введи вагу в профілі для точного розрахунку'

        return cls.objects.create(
            user=user,
            title='Пити воду 💧',
            description=desc,
            color='#4facfe',
            icon='💧',
            frequency='daily',
        )
    
    @property
    def is_system_water_habit(self):
        return self.title == 'Пити воду 💧'
    
    @property
    def target_days_string(self):
        return ','.join(self.target_days) if isinstance(self.target_days, list) else ''
    
    @target_days_string.setter
    def target_days_string(self, value):
        if isinstance(value, str):
            self.target_days = [day.strip() for day in value.split(',') if day.strip()]
        else:
            self.target_days = []