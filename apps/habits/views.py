from rest_framework import viewsets, permissions
from .models import Habit
from .serializers import HabitSerializers

class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user, is_active=True)