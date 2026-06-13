from functools import wraps
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

def habit_owner_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        habit_id = kwargs.get('habit_id')

        if habit_id:
            from apps.habits.models import Habit
            habit = get_object_or_404(Habit, id=habit_id)

            if habit.user != request.user:
                messages.error(request, 'У Вас немає доступу до цієї звички')
                return redirect('/habits/')
            
        return view_func(request, *args, **kwargs)
    
    return wrapper