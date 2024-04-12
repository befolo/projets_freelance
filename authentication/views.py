from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


def connexion(request):
    msg = ''
    if request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            msg = 'Identifiants Invalid, veillez recommencer ! '
            messages.error(request, msg)
    return render(request, 'authentication/conexion.html')


def deconnexion(request):
    logout(request)
    return redirect('home')


def creer_un_compte(request):
    pass
