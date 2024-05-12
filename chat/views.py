from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import GroupeChatForm, MessageForm
from .models import GroupeChat, Message
from projet.models import PartiPrenante
from django.http import JsonResponse


@login_required
def afficher_groupes_chat(request):
    # Récupérer tous les projets auxquels l'utilisateur est partiprenant
    projets_participant = PartiPrenante.objects.filter(lepartiprenant=request.user).values_list('projet', flat=True)

    # Récupérer tous les groupes de chat associés à ces projets
    groupes_chat = GroupeChat.objects.filter(projet__in=projets_participant)

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
def supprimer_groupe_chat(request, groupe_chat_id):
    groupe_chat = get_object_or_404(GroupeChat, id=groupe_chat_id)
    if request.method == 'POST':
        groupe_chat.delete()
        messages.success(request, 'Le groupe de chat a été supprimé avec succès.')
        return redirect('nom_de_la_vue_pour_afficher_les_groupes')

    context = {'groupe_chat': groupe_chat}
    return render(request, 'supprimer_groupe_chat.html', context)


@login_required
def supprimer_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    groupe_chat = message.groupechat  # Récupérer le groupe de chat associé au message
    if request.method == 'POST':
        message.delete()
        messages.success(request, 'Le message a été supprimé avec succès.')
        return redirect('nom_de_la_vue_pour_afficher_le_groupe', groupe_chat_id=groupe_chat.id)

    context = {'message': message, 'groupe_chat': groupe_chat}
    return render(request, 'supprimer_message.html', context)


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
        message_data = {
            'id': message.id,
            'contenu': message.contenu,
            'date_envoi': message.date_envoi.strftime('%d/%m/%Y %H:%M'),  # Format de date personnalisé
            'auteur': message.auteur.username,
            'file_url': message.file.url if message.file else None,  # URL du fichier s'il existe
            'is_image': message.file.url.endswith(('png', 'jpg', 'jpeg', 'gif')) if message.file else False
            # Vérification si le fichier est une image
        }
        messages_list.append(message_data)

    return JsonResponse({"messages": messages_list})
