from django.shortcuts import render


def home(request):
    if request.method == 'POST':
        print(request.POST)
    message = 'Identifiants invalides.'
    return render(request, 'index.html', context={'message': message})
