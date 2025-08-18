from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("guest/", views.guest, name="guest")
]
