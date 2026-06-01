from rest_framework import serializers
from .models import HabitCheckIn

class HabitCheckInSerializers(serializers.ModelSerializer):
    class Meta:
        model = HabitCheckIn
        fields = ('id', 'habit', 'date', 'is_completed', 'note', 'created_at')
        read_only_fields = ('created_at',)