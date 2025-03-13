from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.models import Group

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = request.POST['role']
        print(role)

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match')
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            profile = UserProfile.objects.create(user=user, role=role)
            if role == "student":
                group, created = Group.objects.get_or_create(name="Students")
                user.groups.add(group)
            elif role == "placement_officer":
                group, created = Group.objects.get_or_create(name="Placement Officers")
                user.groups.add(group)

            elif role == "company":
                group, created = Group.objects.get_or_create(name="Companies")
                user.groups.add(group)

            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')

    return render(request, 'register.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        print("is user a superuser", user.is_superuser)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')  
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login')  
