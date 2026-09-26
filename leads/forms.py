from django import forms


class ImportCommentsForm(forms.Form):
    arquivo = forms.FileField(
        label='Arquivo CSV',
        help_text='Aceita CSV separado por ponto e virgula ou virgula. Use o modelo incluido no projeto.',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.csv,text/csv'}),
    )
