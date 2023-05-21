from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, ("Ошибка авторизации, попробуйте еще раз"))
            return redirect('login')  
    else:
        return render(request, "user/login.html")
    

def logout_user(request):
    print("logout")
    logout(request)
    messages.success(request, ("Вы вышли из аккаунта"))
    return redirect('home')


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, ("Аккаунт зарегистрирован"))
            return redirect('home')
    else:
        form = RegisterUserForm()
    return render(request, "user/registation.html",{
        'form': form,
    })
