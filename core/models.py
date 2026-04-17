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

    LACRE_CHOICES = [
        ("3", "3"),
        ("6", "6"),
        ("12", "12"),
        ("15", "15"),
        ("18", "18"),
        ("21", "21"),
        ("24", "24"),
    ]

    motorista = models.CharField("motorista", max_length=100)
    placa = models.CharField("placa", max_length=10)
    distribuidora = models.CharField("distribuidora", max_length=50)
    transportador = models.CharField("transportador", max_length=50)
    litragem_sem_excesso = models.IntegerField("litragem sem excesso")
    ordem = models.CharField("ordem", max_length=10, choices=ORDEM_CHOICES)
    situacao = models.CharField("situacao", max_length=20, choices=SITUACAO_CHOICES)
    lacres = models.CharField("lacres", max_length=10, choices=LACRE_CHOICES)
    data_hora_cadastro = models.DateTimeField("data/hora cadastro", default=timezone.now, editable=False)
    alterado_por = models.CharField("alterado por", max_length=150, blank=True, default="")
    data_hora_alteracao = models.DateTimeField("data/hora alteração", null=True, blank=True)

    class Meta:
        verbose_name = "carregamento"
        verbose_name_plural = "carregamentos"
        ordering = ["id"]

    def __str__(self):
        return f"{self.motorista} - {self.placa}"
