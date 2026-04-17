from django.contrib import admin
from django.utils import timezone

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
        "ultima_alteracao",
    )
    list_filter = ("situacao", "ordem", "distribuidora", "transportador")
    search_fields = ("motorista", "placa", "transportador", "distribuidora")

    def save_model(self, request, obj, form, change):
        if not obj.alterado_por:
            obj.alterado_por = str(request.user)
            obj.data_hora_alteracao = timezone.now()
        super().save_model(request, obj, form, change)

    def ultima_alteracao(self, obj):
        if obj.alterado_por and obj.data_hora_alteracao:
            return f"{obj.alterado_por} - {obj.data_hora_alteracao.strftime('%d/%m/%Y %H:%M')}"
        return "-"
    ultima_alteracao.short_description = "ÚLTIMA ALTERAÇÃO"
