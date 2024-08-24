from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import UserProfile, Task
from .forms import LoginForm, TaskForm
from django.contrib.auth.models import User

def home(request):
    return render(request, 'frontpage/home.html')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            
            user, created = User.objects.get_or_create(username=email)
            
            if created:
                UserProfile.objects.create(user=user, name=name)
                return redirect('welcome')
            else:
                login(request, user)
                return redirect('user_profile')
    else:
        form = LoginForm()
    return render(request, 'frontpage/login.html', {'form': form})

@login_required
def user_profile(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'frontpage/user_profile.html', {'tasks': tasks})

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('user_profile')
    else:
        form = TaskForm()
    return render(request, 'frontpage/add_task.html', {'form': form})

@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = TaskForm(instance=task)
    return render(request, 'frontpage/update_task.html', {'form': form})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('user_profile')  # Redirect to profile to see the updated task list
    return render(request, 'frontpage/delete_task.html', {'task': task})

def task_list(request):
    # Assuming this is for logged-in users
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)
    else:
        tasks = Task.objects.none()  # No tasks if user is not logged in

    return render(request, 'frontpage/task_list.html', {'tasks': tasks})

def welcome(request):
    return render(request, 'frontpage/welcome.html')

# def is_superuser(user):
#     return user.is_superuser

# @user_passes_test(is_superuser)
# def admin_dashboard(request):
#     user_count = User.objects.count()
#     task_count = Task.objects.count()
#     return render(request, 'admin_dashboard/admin_dashboard.html', {
#         'user_count': user_count,
#         'task_count': task_count,
#     })
