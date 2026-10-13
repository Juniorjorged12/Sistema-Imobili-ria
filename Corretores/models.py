from django.db import models

class Corretor(models.Model):
    usuario = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    creci = models.CharField(max_length=20, unique=True, blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.usuario.username
