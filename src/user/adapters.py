from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import redirect
from allauth.exceptions import ImmediateHttpResponse

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Obtener el email de extra_data
        email = sociallogin.account.extra_data.get('email')
        
        if not email:
            return  # Detenemos la ejecución si no hay email

        # Verificamos si el usuario ya existe
        if sociallogin.is_existing:
            return

        # Buscar el usuario por email
        User = sociallogin.user.__class__
        try:
            user = User.objects.get(email=email)
            # Conectar la cuenta social con el usuario existente
            sociallogin.connect(request, user)
        except User.DoesNotExist:
            # Si no existe, guardar el email en la sesión y redirigir al registro
            request.session['choose_path'] = email
            raise ImmediateHttpResponse(redirect('choose_path'))  # Asegúrate que 'register' esté en tus urls