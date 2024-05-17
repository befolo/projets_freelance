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
import chat.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('connexion/', authentication.views.connexion, name='connexion'),
    path('', projet.views.home, name='home'),
    path('data/', projet.views.load_data, name='data'),
    path('deconnexion/', authentication.views.deconnexion, name='deconnexion'),
    path('inscription/', authentication.views.creer_un_compte, name='inscription'),
    path('projet/<int:projet_id>', projet.views.projet_detail, name='view_projet'),
    path('contribution/', projet.views.toutlescommentaires, name='contribution'),
    path('chat/', chat.views.afficher_groupes_chat, name='groupe_list'),
    path('chat/<int:groupe_chat_id>', chat.views.discussion, name='discussion'),
    path('chat/messages/<int:groupe_chat_id>', chat.views.liste_messaages, name='messages'),
    path('chat/creategroupe', chat.views.creer_groupchat, name='creategroupe'),
    path('chat/<int:groupe_chat_id>/editspp', chat.views.edit_spp_groupechat, name='edit_grpchat'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
