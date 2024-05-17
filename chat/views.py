from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import GroupeChatForm, MessageForm
from .models import GroupeChat, Message
from projet.models import PartiPrenante
from django.http import JsonResponse
from itertools import chain

from . import forms, models


@login_required
def afficher_groupes_chat(request):
    # Récupérer tous les projets auxquels l'utilisateur est partiprenant
    projets_participant = PartiPrenante.objects.filter(lepartiprenant=request.user).values_list('projet', flat=True)

    # Récupérer tous les groupes de chat associés à ces projets
    groupes_chat = GroupeChat.objects.filter(projet__in=projets_participant)
    groupes_chat = sorted(
        chain(groupes_chat),
        key=lambda instance: instance.date_created,
        reverse=True
    )

    # Regrouper les groupes de chat par projet
    groupes_par_projet = {}
    for groupe in groupes_chat:
        if groupe.projet.id not in groupes_par_projet:
            groupes_par_projet[groupe.projet.id] = {'projet': groupe.projet, 'groupes_chat': []}
        groupes_par_projet[groupe.projet.id]['groupes_chat'].append(groupe)

    # Passer les données à votre template
    context = {'groupes_par_projet': groupes_par_projet.values()}
    return render(request, 'chat/groupe_list.html', context)


@login_required
def creer_groupchat(request):
    if request.method == 'POST':
        form = GroupeChatForm(request.POST, user=request.user)
        print(form)
        if form.is_valid():
            print("valid")
            groupchat = form.save(commit=False)
            groupchat.createur = request.user
            groupchat.save()
            return redirect('groupe_list')  # Rediriger vers une page de confirmation
        else:
            print("nonvalid")
    else:

        form = GroupeChatForm(user=request.user)

    return render(request, 'chat/creer_groupchat.html', {'form': form})


@login_required
def edit_spp_groupechat(request, groupe_chat_id):
    groupchat = get_object_or_404(models.GroupeChat, id=groupe_chat_id)
    edit_form = forms.GroupeChatForm(instance=groupchat, user=request.user)
    delete_form = forms.DeleteGroupeChatForm()
    if request.method == 'POST':
        if 'edit_grpchat' in request.POST:
            edit_form = forms.GroupeChatForm(request.POST, instance=groupchat, user=request.user)
            if edit_form.is_valid():
                print("oui 2")
                edit_form.save()
                return redirect('groupe_list')
        if 'delete_grpchat' in request.POST:
            delete_form = forms.DeleteGroupeChatForm(request.POST)
            print("oui 1")
            if delete_form.is_valid():
                groupchat.delete()
                return redirect('groupe_list')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
        'groupechat': groupchat
    }
    return render(request, 'chat/edit_spp_grpchat.html', context=context)


@login_required
def discussion(request, groupe_chat_id):
    groupechat = get_object_or_404(GroupeChat, pk=groupe_chat_id)

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.auteur = request.user
            message.groupechat = groupechat
            message.save()
            return JsonResponse({'success': True, 'message_id': message.id})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = MessageForm()

    context = {'form': form, 'groupe_id': groupe_chat_id, "groupechat": groupechat}
    return render(request, 'chat/discussion.html', context=context)


def liste_messaages(request, groupe_chat_id):
    groupe_chat = get_object_or_404(GroupeChat, id=groupe_chat_id)
    messages_groupe = Message.objects.filter(groupechat=groupe_chat)

    messages_list = []
    for message in messages_groupe:
        partie_prenante = PartiPrenante.objects.filter(lepartiprenant=message.auteur, projet=groupe_chat.projet).first()
        role_partie_prenante = partie_prenante.get_role_display()
        message_data = {
            'id': message.id,
            'contenu': message.contenu,
            'date_envoi': message.date_envoi,  # Format de date personnalisé
            'auteur': message.auteur.username,
            'file_url': message.file.url if message.file else None,  # URL du fichier s'il existe
            # Vérification si le fichier est une image
            'is_image': message.file.url.endswith(('png', 'jpg', 'jpeg', 'gif')) if message.file else False,
            'role': role_partie_prenante,
        }
        messages_list.append(message_data)

    return JsonResponse({"messages": messages_list})
