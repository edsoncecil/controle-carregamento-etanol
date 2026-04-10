from django.contrib import admin

from .models import Carregamento


@admin.register(Carregamento)
class CarregamentoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "motorista",
        "placa",
        "transportador",
        "distribuidora",
        "litragem_sem_excesso",
        "ordem",
        "situacao",
        "lacres",
    )
    list_filter = ("situacao", "ordem", "distribuidora", "transportador")
    search_fields = ("motorista", "placa", "transportador", "distribuidora")
