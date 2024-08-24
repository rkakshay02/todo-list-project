from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('add_task/', views.add_task, name='add_task'),
    path('update_task/<int:task_id>/', views.update_task, name='update_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('welcome/', views.welcome, name='welcome'),
    path('tasks/', views.task_list, name='task_list'),
    
]
