from django.urls import path, include
from . import views
from allauth.socialaccount.providers.google.views import oauth2_login

def google_login_redirect(request):
    return oauth2_login(request)

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", google_login_redirect, name="login"),
    path("historico/", views.historico_pesquisas, name="historico_pesquisas"),
    path("historico/<int:pk>/", views.ver_pesquisa, name="ver_pesquisa"),
    path("accounts/", include("allauth.urls"))
]
