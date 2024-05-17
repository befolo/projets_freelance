from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from .models import PartiPrenante


class CustomSessionMiddleware(SessionMiddleware):
    def process_request(self, request):
        super().process_request(request)

        user = getattr(request, 'user', None)
        if user and not isinstance(user, AnonymousUser):  # Vérifie si l'utilisateur est authentifié
            try:
                is_participant = PartiPrenante.objects.filter(lepartiprenant=user).exists()
                request.session['est_participant'] = is_participant
            except Exception:
                pass

