from rest_framework import serializers
from .models import Habit

class HabitSerializers(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Habit
        fields = (
            'id', 'user_name', 'title', 'description',
            'color', 'icon', 'frequency', 'target_days',
            'is_active', 'created_at', 'updated_at'
        )
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)