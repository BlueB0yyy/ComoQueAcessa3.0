from django.urls import path, include
from django.shortcuts import redirect
from . import views
from allauth.socialaccount.providers.google.views import oauth2_login

def google_login_redirect(request):
    return oauth2_login(request)

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", google_login_redirect, name="login"),
    path("historico/", views.historico_pesquisas, name="historico_pesquisas"),
    path("accounts/", include("allauth.urls"))
]
