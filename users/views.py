import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from .models import User

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'users/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return render(request, 'users/register.html')

        user = User(username=username, password=make_password(password))
        user.save()

        login(request, user)
        return redirect('login')

    return render(request, 'users/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials!")
            return render(request, 'users/login.html')

    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # 登出后重定向到登录页面

def home_view(request):
    return render(request, 'users/home.html')

