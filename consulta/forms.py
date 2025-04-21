from django import forms

class ConsultaAsociado(forms.Form):
    identificacion = forms.CharField(
        required=True,
        min_length=4,
        max_length=30,
        label='',
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-create',  # Clase CSS adicional para personalización
            'id': 'identificacion',
            'placeholder': 'Digite número de identificación'
        })
    )
