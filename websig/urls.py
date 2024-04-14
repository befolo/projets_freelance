"""
URL configuration for websig project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import authentication.views
import projet.views
import map.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('connexion/', authentication.views.connexion, name='connexion'),
    path('home/', projet.views.home, name='home'),
    path('deconnexion/', authentication.views.deconnexion, name='deconnexion'),
    path('inscription/', authentication.views.creer_un_compte, name='inscription'),
    path('map/', map.views.view_map, name='map'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
