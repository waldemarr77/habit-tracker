from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets, permissions
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .models import Habit
from .serializers import HabitSerializers
from apps.tracking.models import HabitCheckIn
from django.db.models import Count, Avg, Max, Min, Q
from datetime import timedelta
from .decorators import habit_owner_required
from .forms import HabitForm
from .services import StreakAnalyzer, CompletionRateAnalyzer

class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.for_user(self.request.user)
    

import datetime

@login_required(login_url='/login/')
def dashboard_view(request):
    user = request.user
    today = timezone.now().date()
    start_of_week = today - datetime.timedelta(days=today.weekday())

    # Беремо всі звички і їхні відмітки
    habits = list(Habit.objects.for_user(user).prefetch_related('checkins').select_related('user'))
    total_active_habits = len(habits)

    for habit in habits:
        # Чи виконано сьогодні
        habit.is_completed_today = any(c.date == today and c.is_completed for c in habit.checkins.all())
        
        # Відмітки за поточний тиждень (від понеділка до неділі)
        week_completed_days = set(c.date.weekday() for c in habit.checkins.all() if c.date >= start_of_week and c.is_completed)
        
        habit.week_days = []
        days_letters = ['П', 'В', 'С', 'Ч', 'П', 'С', 'Н']
        for i in range(7):
            habit.week_days.append({
                'letter': days_letters[i],
                'completed': i in week_completed_days
            })

        # Динамічний розрахунок норми води (не залежить від БД)
        if habit.icon == '💧' and user.weight:
            daily_ml = int(user.weight) * 35
            daily_liters = round(daily_ml / 1000, 1)
            habit.description = f'Денна норма: {daily_liters}л ({daily_ml}мл)'

    completed_today = sum(1 for h in habits if h.is_completed_today)

    # 1. Current Streak
    current_streak = 0
    check_date = today
    
    # Спочатку перевіряємо, чи є хоч один чек-ін сьогодні
    has_checkin_today = HabitCheckIn.objects.filter(
        habit__user=user, date=today, is_completed=True
    ).exists()
    
    # Якщо сьогодні немає, перевіряємо з учорашнього дня
    if not has_checkin_today:
        check_date = today - timedelta(days=1)
        
    while True:
        has_checkin = HabitCheckIn.objects.filter(
            habit__user=user,
            date=check_date,
            is_completed=True
        ).exists()
        
        if has_checkin:
            current_streak += 1
            check_date -= timedelta(days=1)
        else:
            break

    # 2. Perfect Days (цього місяця)
    first_day_of_month = today.replace(day=1)
    daily_checkins = HabitCheckIn.objects.filter(
        habit__user=user,
        date__gte=first_day_of_month,
        date__lte=today,
        is_completed=True
    ).values('date').annotate(
        completed_count=Count('id')
    )
    
    perfect_days = 0
    if total_active_habits > 0:
        for day_data in daily_checkins:
            if day_data['completed_count'] >= total_active_habits:
                perfect_days += 1

    # 3. Weekly Goal (за останні 7 днів)
    week_ago = today - timedelta(days=7)
    checkins_last_7_days = HabitCheckIn.objects.filter(
        habit__user=user,
        date__gt=week_ago,
        date__lte=today,
        is_completed=True
    ).count()
    
    total_possible_week = total_active_habits * 7
    weekly_percentage = 0
    if total_possible_week > 0:
        weekly_percentage = int((checkins_last_7_days / total_possible_week) * 100)

    context = {
        'habits': habits,
        'total_habits': total_active_habits,
        'active_habits': total_active_habits,
        'completed_today': completed_today,
        'current_streak': current_streak,
        'perfect_days': perfect_days,
        'weekly_percentage': weekly_percentage,
    }

    return render(request, 'habits/dashboard.html', context)

@login_required(login_url='/login/')
@habit_owner_required
def habit_detail_view(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    checkins = HabitCheckIn.objects.filter(habit=habit).order_by('-date')
    return render(request, 'habits/detail.html', {'habit': habit, 'checkins': checkins})


class HabitCreateView(LoginRequiredMixin, CreateView):
    model = Habit
    form_class = HabitForm
    template_name = 'habits/create.html'
    success_url = '/habits/'
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Звичку створено')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Помилка у формі. Перевірте дані')
        return super().form_invalid(form)
    

@login_required(login_url='/login/')
@habit_owner_required
def habit_checkin_view(request, habit_id):
    if request.method == 'POST':
        habit = get_object_or_404(Habit, id=habit_id, user=request.user)
        today = timezone.now().date()
        checkin, created = HabitCheckIn.objects.get_or_create(
            habit=habit,
            date=today,
            defaults={'is_completed': True, 'note': request.POST.get('note', '')}
        )
        if created:
            messages.success(request, 'Виконано!')
        else:
            messages.error(request, 'Сьогодні вже відмічено.')
    return redirect('/habits/')


@login_required(login_url='/login/')
@habit_owner_required
def habit_delete_view(request, habit_id):
    if request.method == 'POST':
        habit = get_object_or_404(Habit, id=habit_id, user=request.user)
        habit.delete()
        messages.success(request, 'Звичку видалено')
    return redirect('/habits/')


@login_required(login_url='/login/')
@habit_owner_required
def habit_edit_view(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)

    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)

        if form.is_valid():
            form.save()
            messages.success(request, 'Звичку оновлено!')
            return redirect('/habits/')
        else:
            messages.error(request, 'Помилка в формі. Перевірте дані')
    
    return render(request, 'habits/edit.html', {'habit': habit})


@login_required(login_url='/login/')
def statistics_view(request):
    user = request.user
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    total_stats = HabitCheckIn.objects.filter(
        habit__user=user
    ).aggregate(
        total_checkins=Count('id'),
        completed=Count('id', filter=Q(is_completed=True))
    )

    habits_with_stats = Habit.objects.for_user(user).with_stats()

    weekly_stats = HabitCheckIn.objects.filter(
        habit__user=user,
        date__gte=week_ago
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')

    streak = 0
    check_date = today
    while True:
        has_checkin = HabitCheckIn.objects.filter(
            habit__user=user,
            date=check_date,
            is_completed=True
        ).exists()
        if has_checkin:
            streak += 1
            check_date -= timedelta(days=1)
        else:
            break

    best_habit = Habit.objects.for_user(user).annotate(
        count=Count('checkins')
    ).order_by('-count').first()

    # Аналізуємо кожну звичку через сервіси
    streak_analyzer = StreakAnalyzer()
    rate_analyzer = CompletionRateAnalyzer()

    habits_analytics = [
        {
            'habit': habit,
            'streak': streak_analyzer.analyze(habit),
            'completion_rate': rate_analyzer.analyze(habit),
        }
        for habit in habits_with_stats
    ]

    total_habits = Habit.objects.for_user(user).count()

    context = {
        'total_stats': total_stats,
        'total_habits': total_habits,
        'habits_with_stats': habits_with_stats,
        'weekly_stats': list(weekly_stats),
        'streak': streak,
        'best_habit': best_habit,
        'month_ago': month_ago,
        'habits_analytics': habits_analytics,
    }

    return render(request, 'habits/statistics.html', context)


@login_required(login_url='/login/')
@require_POST
def habit_reorder_view(request):
    """Saves drag-and-drop order of habits."""
    try:
        data = json.loads(request.body)
        habit_ids = data.get('habit_ids', [])
        for index, habit_id in enumerate(habit_ids):
            Habit.objects.filter(id=int(habit_id), user=request.user).update(order=index)
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)