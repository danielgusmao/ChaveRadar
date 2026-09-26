from django import forms

from .models import MonitoringProfile


class ImportCommentsForm(forms.Form):
    arquivo = forms.FileField(
        label='Arquivo CSV',
        help_text='Aceita CSV separado por ponto e virgula ou virgula. Use o modelo incluido no projeto.',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.csv,text/csv'}),
    )


class MonitoringProfileForm(forms.ModelForm):
    class Meta:
        model = MonitoringProfile
        fields = ['handle', 'display_name', 'active', 'alerts_enabled', 'keywords', 'notes']
        labels = {
            'handle': 'Perfil do Instagram',
            'display_name': 'Nome / apelido',
            'active': 'Monitoramento ativo',
            'alerts_enabled': 'Gerar alertas',
            'keywords': 'Palavras-chave adicionais',
            'notes': 'Observacoes',
        }
        widgets = {
            'handle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '@minhacorretora'}),
            'display_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Minha Corretora'}),
            'keywords': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'ex.: cobertura, apartamento, financiamento'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Observacoes opcionais'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'alerts_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_handle(self):
        value = (self.cleaned_data.get('handle') or '').strip().lower()
        if not value:
            raise forms.ValidationError('Informe o perfil do Instagram.')
        if not value.startswith('@'):
            value = '@' + value
        if ' ' in value:
            raise forms.ValidationError('O perfil nao pode conter espacos.')
        return value
