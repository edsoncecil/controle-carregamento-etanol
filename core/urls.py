from django.urls import path

from .views import api_carregamentos, editar_carregamento, fila_carregamento

urlpatterns = [
    path("", fila_carregamento, name="fila_carregamento"),
    path("editar/<int:pk>/", editar_carregamento, name="editar_carregamento"),
    path("api/carregamentos/", api_carregamentos, name="api_carregamentos"),
]
