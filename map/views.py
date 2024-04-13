from django.shortcuts import render


def view_map(request):
    return render(request, 'map/map.html')
