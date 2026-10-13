from django.db import models

class Bairro(models.Model):
    nome = models.CharField(max_length=100)
    cidade = models.ForeignKey('Cidades.Cidade', on_delete=models.CASCADE, related_name='bairros')

    def __str__(self):
        return f"{self.nome} - {self.cidade}"
    
