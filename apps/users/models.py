from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.FileField(upload_to='avatars/', null=True, blank=True)
    timezone = models.CharField(max_length=50, default='Europe/Kyiv')
    weight = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Вага (кг)'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'

    def __str__(self):
        return self.email


