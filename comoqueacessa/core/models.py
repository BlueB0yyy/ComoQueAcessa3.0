from django.db import models
from django.contrib.auth.models import User

class Hist_busca(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    busca = models.TextField()
    resposta = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.busca[:50]


