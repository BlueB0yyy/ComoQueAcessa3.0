from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class MyAccountAdapter(DefaultAccountAdapter):
    # Se quiser customizar regras de login por e-mail normal
    pass

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Executa antes do login social.
        Aqui você pode, por exemplo, forçar o vínculo pelo e-mail.
        """
        # Se o usuário já estiver logado, não faz nada
        if request.user.is_authenticated:
            return

        # Se a resposta do Google já trouxe o email
        if sociallogin.account.extra_data.get("email"):
            from django.contrib.auth import get_user_model
            User = get_user_model()
            email = sociallogin.account.extra_data["email"]

            try:
                # Se o usuário já existir no banco, vincula
                user = User.objects.get(email=email)
                sociallogin.connect(request, user)
            except User.DoesNotExist:
                # Se não existir, o AUTO_SIGNUP vai criar normalmente
                pass
