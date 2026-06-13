from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def create_default_habit(sender, instance, created, **kwargs):
    if created:
        from apps.habits.models import Habit

        Habit.setup_water_norm(user=instance, weight=instance.weight)