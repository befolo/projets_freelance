from django.shortcuts import render
from .models import User
from django.contrib.auth import login, authenticate
from . import forms


def home(request):
    message = ''

    if request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        user = User.objects.filter(email=email).first()
        if user:
            message = 'ok'
        message = 'ras'
    return render(
        request, 'authentication/conexion.html', context={'message': message})
