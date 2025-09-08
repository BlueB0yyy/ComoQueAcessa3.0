from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Campos que aparecem na tela de listagem
    list_display = ("email", "first_name", "last_name", "is_staff", "is_active")

    # Filtros laterais
    list_filter = ("is_staff", "is_active", "is_superuser", "groups")

    # Campos editáveis
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Informações pessoais", {"fields": ("first_name", "last_name")}),
        ("Permissões", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Datas importantes", {"fields": ("last_login", "date_joined")}),
    )

    # Campos para adicionar usuário
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
