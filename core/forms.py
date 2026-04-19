from django import forms

from .models import Carregamento


class CarregamentoForm(forms.ModelForm):
    class Meta:
        model = Carregamento
        fields = [
            "motorista",
            "transportador",
            "placa",
            "distribuidora",
            "litragem_sem_excesso",
            "ordem",
            "situacao",
            "lacres",
        ]
        widgets = {
            "motorista": forms.TextInput(attrs={"placeholder": "Nome do motorista"}),
            "transportador": forms.TextInput(attrs={"placeholder": "Transportadora"}),
            "placa": forms.TextInput(attrs={"placeholder": "ABC1D23", "style": "text-transform: uppercase;"}),
            "distribuidora": forms.TextInput(attrs={"placeholder": "Distribuidora"}),
            "litragem_sem_excesso": forms.NumberInput(attrs={"min": 0}),
            "ordem": forms.Select(),
            "situacao": forms.Select(),
            "lacres": forms.Select(),
        }

    def clean_placa(self):
        return self.cleaned_data["placa"].upper().strip()
