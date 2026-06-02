from django.urls import path
from .views import CheckInListCreateView

urlpatterns = [
    path('habit/<int:habit_id>/checkins/', CheckInListCreateView.as_view(), name='checkins')
]