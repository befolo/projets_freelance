from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.core.validators import validate_email
from django.db.models import Q
from .models import User
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
    error = False
    msg = ''
    if request.method == 'POST':
        email = request.POST.get('email', None)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        rpassword = request.POST.get('rpassword', None)

        try:
            validate_email(email)
        except:
            msg = 'Votre email est invalid !'
            error = True

        if not error:
            if password != rpassword:
                msg = 'Les deux mot de passe ne correspondent pas !'
                error = True
        if not error:
            user = User.objects.filter(Q(email=email) | Q(username=username)).first()
            if user:
                msg = f'l\'utilisateur avec l\'email:{email} ou le nom : {username} existe déjà  !'
                error = True
        if not error:
            user = User(
                email=email,
                username=username
            )
            user.save()
            user.password = password
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect('home')
    messages.error(request, msg)
    return render(request, 'authentication/inscription.html')
