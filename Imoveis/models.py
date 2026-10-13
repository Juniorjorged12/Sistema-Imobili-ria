from django.db import models

class Imovel(models.Model):
    FINALIDADE_CHOICES = [
        ('venda', 'Venda'),
        ('aluguel', 'Aluguel'),
    ]

    TIPO_CHOICES = [
        ('casa', 'Casa'),
        ('apartamento', 'Apartamento'),
        ('comercial', 'Comercial'),
        ('sala_comercial', 'Sala Comercial'),
        ('galpao', 'Galpão'),
        ('chacara', 'Chácara'),
        ('sitio', 'Sítio'),
        ('terreno_comercial', 'Terreno Comercial'),
        ('terreno_residencial', 'Terreno Residencial'),
    ]

    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('vendido', 'Vendido'),
        ('alugado', 'Alugado'),
    ]

    QUANTIDADE_CHOICES = [(i, str(i)) for i in range(0, 6)] + [(6, 'mais de 5')]

    finalidade = models.CharField(max_length=10, choices=FINALIDADE_CHOICES)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    cidade = models.ForeignKey('Cidades.Cidade', on_delete=models.PROTECT)
    bairro = models.ForeignKey('Bairros.Bairro', on_delete=models.PROTECT)
    endereco = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    dormitorios = models.IntegerField(choices=QUANTIDADE_CHOICES)
    suites = models.IntegerField(choices=QUANTIDADE_CHOICES)
    banheiros = models.IntegerField(choices=QUANTIDADE_CHOICES)
    vagas = models.IntegerField(choices=QUANTIDADE_CHOICES)
    area_total = models.DecimalField(max_digits=10, decimal_places=2)
    area_construida = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='disponivel')
    corretor = models.ForeignKey('Corretores.Corretor', on_delete=models.PROTECT)
    piscina = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.id} - {self.tipo} em {self.bairro.nome}, {self.cidade.nome} - {self.finalidade.capitalize()} - R$ {self.valor:,.2f}"
    
