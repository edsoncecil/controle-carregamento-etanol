from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from urllib.parse import urlencode

from .forms import CarregamentoForm
from .models import Carregamento


def logout_view(request):
    logout(request)
    return render(request, "registration/logged_out.html")


STATUS_FILTER_OPTIONS = [
    ("ATIVOS", "Somente ativos (esconde finalizados)"),
    ("TODOS", "Todos os status"),
    ("CARREGANDO", "Apenas carregando"),
    ("PATIO", "Apenas pátio"),
    ("FINALIZADO", "Apenas finalizado"),
]
PER_PAGE_OPTIONS = [10, 20, 50, 100]

SORT_FIELDS = {
    "motorista": "motorista",
    "placa": "placa",
    "distribuidora": "distribuidora",
    "transportador": "transportador",
    "litragem": "litragem_sem_excesso",
    "ordem": "ordem",
    "situacao": "situacao",
    "lacres": "lacres",
    "cadastro": "data_hora_cadastro",
}


def _sanitize_sort_by(raw_sort_by):
    if raw_sort_by in SORT_FIELDS:
        return raw_sort_by
    return "cadastro"


def _sanitize_sort_dir(raw_sort_dir):
    if raw_sort_dir == "asc":
        return "asc"
    return "desc"


def _sanitize_per_page(raw_per_page):
    try:
        value = int(raw_per_page)
    except (TypeError, ValueError):
        return 20
    if value in PER_PAGE_OPTIONS:
        return value
    return 20


def _build_query_string(status_filtro, busca, sort_by, sort_dir, per_page, page=None):
    query = {
        "status": status_filtro,
        "q": busca,
        "sort": sort_by,
        "dir": sort_dir,
        "per_page": per_page,
    }
    if page is not None:
        query["page"] = page
    return urlencode(query)


def _build_sort_links(status_filtro, busca, sort_by, sort_dir, per_page):
    links = {}
    for key in SORT_FIELDS:
        next_dir = "asc"
        if sort_by == key and sort_dir == "asc":
            next_dir = "desc"
        links[key] = _build_query_string(status_filtro, busca, key, next_dir, per_page)
    return links


def _listar_carregamentos(status_filtro, busca, sort_by, sort_dir):
    carregamentos = Carregamento.objects.all()

    if status_filtro == "ATIVOS":
        carregamentos = carregamentos.exclude(situacao="FINALIZADO")
    elif status_filtro != "TODOS":
        carregamentos = carregamentos.filter(situacao=status_filtro)

    busca = busca.strip()
    if busca:
        filtro_busca = (
            Q(motorista__icontains=busca)
            | Q(placa__icontains=busca)
            | Q(distribuidora__icontains=busca)
            | Q(transportador__icontains=busca)
            | Q(ordem__icontains=busca)
            | Q(situacao__icontains=busca)
        )
        if busca.isdigit():
            valor_numerico = int(busca)
            filtro_busca |= Q(lacres=valor_numerico) | Q(litragem_sem_excesso=valor_numerico)
        carregamentos = carregamentos.filter(filtro_busca)

    sort_field = SORT_FIELDS[sort_by]
    order_by = sort_field if sort_dir == "asc" else f"-{sort_field}"
    carregamentos = carregamentos.order_by(order_by, "-id")

    return carregamentos


def _sanitize_status_filter(raw_status):
    allowed_filters = {opt[0] for opt in STATUS_FILTER_OPTIONS}
    if raw_status in allowed_filters:
        return raw_status
    return "ATIVOS"


def _render_fila(
    request,
    form,
    carregamento_em_edicao=None,
    status_filtro="ATIVOS",
    busca="",
    sort_by="cadastro",
    sort_dir="asc",
    per_page=20,
    page=1,
):
    carregamentos_qs = _listar_carregamentos(status_filtro, busca, sort_by, sort_dir)
    paginator = Paginator(carregamentos_qs, per_page)
    page_obj = paginator.get_page(page)
    carregamentos = page_obj.object_list

    query_string = _build_query_string(status_filtro, busca, sort_by, sort_dir, per_page, page_obj.number)
    base_query_string = _build_query_string(status_filtro, busca, sort_by, sort_dir, per_page)
    sort_links = _build_sort_links(status_filtro, busca, sort_by, sort_dir, per_page)

    return render(
        request,
        "core/fila_carregamento.html",
        {
            "form": form,
            "carregamentos": carregamentos,
            "page_obj": page_obj,
            "carregamento_em_edicao": carregamento_em_edicao,
            "status_filtro": status_filtro,
            "status_filter_options": STATUS_FILTER_OPTIONS,
            "per_page_options": PER_PAGE_OPTIONS,
            "busca": busca,
            "sort_by": sort_by,
            "sort_dir": sort_dir,
            "per_page": per_page,
            "sort_links": sort_links,
            "query_string": query_string,
            "base_query_string": base_query_string,
        },
    )


@login_required
def fila_carregamento(request):
    status_filtro = _sanitize_status_filter(request.GET.get("status", "ATIVOS"))
    busca = request.GET.get("q", "").strip()
    sort_by = _sanitize_sort_by(request.GET.get("sort", "cadastro"))
    sort_dir = _sanitize_sort_dir(request.GET.get("dir", "asc"))
    per_page = _sanitize_per_page(request.GET.get("per_page", "20"))
    page = request.GET.get("page", "1")

    if request.method == "POST":
        status_filtro = _sanitize_status_filter(request.POST.get("status_filtro", "ATIVOS"))
        busca = request.POST.get("busca", "").strip()
        sort_by = _sanitize_sort_by(request.POST.get("sort_by", "cadastro"))
        sort_dir = _sanitize_sort_dir(request.POST.get("sort_dir", "asc"))
        per_page = _sanitize_per_page(request.POST.get("per_page", "20"))
        page = request.POST.get("page", "1")
        form = CarregamentoForm(request.POST)
        if form.is_valid():
            carregamento = form.save(commit=False)
            carregamento.alterado_por = str(request.user)
            carregamento.data_hora_alteracao = timezone.now()
            carregamento.save()
            messages.success(
                request,
                f"Carregamento de {carregamento.motorista} ({carregamento.placa}) cadastrado com sucesso.",
            )
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"success": True, "message": f"Carregamento de {carregamento.motorista} ({carregamento.placa}) cadastrado com sucesso."})
            query_string = _build_query_string(status_filtro, busca, sort_by, sort_dir, per_page, page)
            return redirect(f"{reverse('fila_carregamento')}?{query_string}")
    else:
        form = CarregamentoForm()

    return _render_fila(
        request,
        form,
        status_filtro=status_filtro,
        busca=busca,
        sort_by=sort_by,
        sort_dir=sort_dir,
        per_page=per_page,
        page=page,
    )


@login_required
def editar_carregamento(request, pk):
    carregamento = get_object_or_404(Carregamento, pk=pk)
    status_filtro = _sanitize_status_filter(request.GET.get("status", "ATIVOS"))
    busca = request.GET.get("q", "").strip()
    sort_by = _sanitize_sort_by(request.GET.get("sort", "cadastro"))
    sort_dir = _sanitize_sort_dir(request.GET.get("dir", "asc"))
    per_page = _sanitize_per_page(request.GET.get("per_page", "20"))
    page = request.GET.get("page", "1")

    if request.method == "POST":
        status_filtro = _sanitize_status_filter(request.POST.get("status_filtro", "ATIVOS"))
        busca = request.POST.get("busca", "").strip()
        sort_by = _sanitize_sort_by(request.POST.get("sort_by", "cadastro"))
        sort_dir = _sanitize_sort_dir(request.POST.get("sort_dir", "asc"))
        per_page = _sanitize_per_page(request.POST.get("per_page", "20"))
        page = request.POST.get("page", "1")
        form = CarregamentoForm(request.POST, instance=carregamento)
        if form.is_valid():
            carregamento = form.save(commit=False)
            carregamento.alterado_por = str(request.user)
            carregamento.data_hora_alteracao = timezone.now()
            carregamento.save()
            messages.success(
                request,
                f"Registro de {carregamento.motorista} ({carregamento.placa}) atualizado com sucesso.",
            )
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"success": True, "message": f"Registro de {carregamento.motorista} ({carregamento.placa}) atualizado com sucesso."})
            query_string = _build_query_string(status_filtro, busca, sort_by, sort_dir, per_page, page)
            return redirect(f"{reverse('fila_carregamento')}?{query_string}")
    else:
        form = CarregamentoForm(instance=carregamento)

    return _render_fila(
        request,
        form,
        carregamento_em_edicao=carregamento,
        status_filtro=status_filtro,
        busca=busca,
        sort_by=sort_by,
        sort_dir=sort_dir,
        per_page=per_page,
        page=page,
    )


@login_required
def api_carregamentos(request):
    status_filtro = _sanitize_status_filter(request.GET.get("status", "ATIVOS"))
    busca = request.GET.get("q", "").strip()
    sort_by = _sanitize_sort_by(request.GET.get("sort", "cadastro"))
    sort_dir = _sanitize_sort_dir(request.GET.get("dir", "asc"))
    per_page = _sanitize_per_page(request.GET.get("per_page", "20"))
    page = request.GET.get("page", "1")

    carregamentos_qs = _listar_carregamentos(status_filtro, busca, sort_by, sort_dir)
    paginator = Paginator(carregamentos_qs, per_page)
    page_obj = paginator.get_page(page)

    query_string = _build_query_string(status_filtro, busca, sort_by, sort_dir, per_page)
    sort_links = _build_sort_links(status_filtro, busca, sort_by, sort_dir, per_page)

    html = render_to_string(
        "core/_tabela_carregamentos.html",
        {
            "carregamentos": page_obj.object_list,
            "page_obj": page_obj,
            "status_filtro": status_filtro,
            "status_filter_options": STATUS_FILTER_OPTIONS,
            "per_page_options": PER_PAGE_OPTIONS,
            "busca": busca,
            "sort_by": sort_by,
            "sort_dir": sort_dir,
            "per_page": per_page,
            "sort_links": sort_links,
            "query_string": query_string,
            "base_query_string": _build_query_string(status_filtro, busca, sort_by, sort_dir, per_page),
        },
    )

    return JsonResponse({"html": html, "success": True})
