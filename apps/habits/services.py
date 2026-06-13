from abc import ABC, abstractmethod
from django.utils import timezone
from datetime import timedelta

class BaseHabitAnalyzer(ABC):
    @abstractmethod
    def analyze(self, habit):
        pass


class StreakAnalyzer(BaseHabitAnalyzer):
    def analyze(self, habit):
        checkins = habit.checkins.filter(
            is_completed=True
        ).order_by('-date')

        if not checkins.exists():
            return 0
        
        streak = 0
        expected_date = timezone.now().date()

        for checkin in checkins:
            if checkin.date == expected_date:
                streak += 1
                expected_date -= timedelta(days=1)
            else:
                break

        return streak
    

class CompletionRateAnalyzer(BaseHabitAnalyzer):
    def analyze(self, habit):
        today = timezone.now().date()
        month_ago = today - timedelta(days=30)

        total = habit.checkins.filter(
            date__gte=month_ago
        ).count()

        if total == 0:
            return 0
        
        completed = habit.checkins.filter(
            date__gte=month_ago,
            is_completed=True
        ).count()

        return round((completed / total) * 100, 1)