from django.urls import path

from .views import (
    api_carregamentos,
    editar_carregamento,
    fila_carregamento,
    relatorio_pdf,
    relatorio_xlsx,
)

urlpatterns = [
    path("", fila_carregamento, name="fila_carregamento"),
    path("editar/<int:pk>/", editar_carregamento, name="editar_carregamento"),
    path("api/carregamentos/", api_carregamentos, name="api_carregamentos"),
    path("relatorio/xlsx/", relatorio_xlsx, name="relatorio_xlsx"),
    path("relatorio/pdf/", relatorio_pdf, name="relatorio_pdf"),
]
