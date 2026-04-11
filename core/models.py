from django.db import models
from django.utils import timezone


class Carregamento(models.Model):
    ORDEM_CHOICES = [
        ("SIM", "SIM"),
        ("NÃO TEM", "NÃO TEM"),
    ]

    SITUACAO_CHOICES = [
        ("FINALIZADO", "Finalizado"),
        ("CARREGANDO", "Carregando"),
        ("PATIO", "Patio"),
    ]

    motorista = models.CharField("motorista", max_length=100)
    placa = models.CharField("placa", max_length=10)
    distribuidora = models.CharField("distribuidora", max_length=50)
    transportador = models.CharField("transportador", max_length=50)
    litragem_sem_excesso = models.IntegerField("litragem sem excesso")
    ordem = models.CharField("ordem", max_length=10, choices=ORDEM_CHOICES)
    situacao = models.CharField("situacao", max_length=20, choices=SITUACAO_CHOICES)
    lacres = models.IntegerField("lacres")
    data_hora_cadastro = models.DateTimeField("data/hora cadastro", default=timezone.now, editable=False)

    class Meta:
        verbose_name = "carregamento"
        verbose_name_plural = "carregamentos"
        ordering = ["id"]

    def __str__(self):
        return f"{self.motorista} - {self.placa}"
