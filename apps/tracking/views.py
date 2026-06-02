from rest_framework import generics, permissions
from .models import HabitCheckIn
from .serializers import HabitCheckInSerializers

class CheckInListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitCheckInSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        habit_id = self.kwargs.get('habit_id')
        return HabitCheckIn.objects.filter(
            habit_id=habit_id,
            habit__user=self.request.user
        )