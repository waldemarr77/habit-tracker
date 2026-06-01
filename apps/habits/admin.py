from django.contrib import admin
from .models import Habit

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'frequency', 'is_active', 'created_at')
    list_filter = ('frequency', 'is_active')
    search_fields = ('title', 'user__email')
    ordering = ('-created_at',)
