from django.db import models

class Fotoimovel(models.Model):
    imovel = models.ForeignKey('Imoveis.Imovel', on_delete=models.CASCADE, related_name='fotos')
    imagem = models.ImageField(upload_to='fotos/')
    destaque = models.BooleanField(default=False)

    def __str__(self):
        return f"Foto de {self.imovel}"
