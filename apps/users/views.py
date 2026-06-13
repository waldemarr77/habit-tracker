from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import RegisterSerialezer, UserProfileSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

User = get_user_model()


def landing_view(request):
    return render(request, 'landing.html')


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerialezer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/habits/')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('/habits/')
        else:
            messages.error(request, 'Невірний gmail/нікнейн або пароль')

    return render(request, 'auth/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('/habits/')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Паролі не співпадають, спробуйте ще раз.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Ця електронна адреса вже використовується')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Цей нікнейм вже зайнятий. Спробуйте інший.')
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Аккаунт створено.')
            return redirect('/login/')
        
    return render(request, 'auth/register.html')
    

def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required(login_url='/login/')
def profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username', user.username)
        user.timezone = request.POST.get('timezone', user.timezone)
        user.weight = request.POST.get('weight') or None

        if request.FILES.get('avatar'):
            user.avatar = request.FILES['avatar']

        user.save()

        if user.weight:
            from apps.habits.models import Habit
            water_habit = Habit.objects.filter(
                user=user,
                icon='💧'
            ).first()

            if water_habit:
                daily_ml, daily_liters = Habit.calculate_water_norm(int(user.weight))
                water_habit.description = f'Денна норма: {daily_liters}л ({daily_ml}мл)'
                water_habit.save()

        messages.success(request, 'Профіль оновлено!')

        return redirect('/profile/')
    
    return render(request, 'auth/profile.html', {'user': request.user})