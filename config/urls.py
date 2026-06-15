from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from apps.users.views import login_view, register_view, logout_view, profile_view, landing_view
from apps.habits.views import HabitCreateView, dashboard_view, habit_detail_view, habit_checkin_view, habit_delete_view, habit_edit_view, statistics_view, habit_reorder_view

urlpatterns = [
    path('', landing_view, name='landing'),
    
    path('admin/', admin.site.urls),

    path('api/auth/', include('apps.users.urls')),
    path('api/habits/', include('apps.habits.urls')),
    path('api/', include('apps.tracking.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),

    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),

    path('habits/', dashboard_view, name='dashboard'),
    path('habits/create/', HabitCreateView.as_view(), name='habit_create'),
    path('habits/statistics/', statistics_view, name='statistics'),
    path('habits/<int:habit_id>/', habit_detail_view, name='habit_detail'),
    path('habits/<int:habit_id>/checkin/', habit_checkin_view, name='habit_checkin'),
    path('habits/<int:habit_id>/delete/', habit_delete_view, name='habit_delete'),
    path('habits/<int:habit_id>/edit/', habit_edit_view, name='habit_edit'),
    path('habits/reorder/', habit_reorder_view, name='habit_reorder'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
