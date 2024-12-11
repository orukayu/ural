from django import forms
from .models import Kasa

class KasaForm(forms.ModelForm):
    class Meta:
        model = Kasa
        fields = ['Tarih', 'Plaka', 'Fisno', 'Sofor', 'Aciklama1', 'Aciklama2', 'Giris', 'Cikis']
        widgets = {
            'Tarih': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '17/03/2025', 'id': 'tarih'}),
            'Plaka': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '55 ABC 1919', 'id': 'plaka'}),
            'Fisno': forms.TextInput(attrs={'class': 'form-control', 'id': 'fisno'}),
            'Sofor': forms.TextInput(attrs={'class': 'form-control', 'id': 'sofor'}),
            'Aciklama1': forms.TextInput(attrs={'class': 'form-control', 'id': 'aciklama1'}),
            'Aciklama2': forms.TextInput(attrs={'class': 'form-control', 'id': 'aciklama2'}),
            'Giris': forms.NumberInput(attrs={'class': 'form-control', 'id': 'giris'}),
            'Cikis': forms.NumberInput(attrs={'class': 'form-control', 'id': 'cikis'}),
        }

    def __init__(self, *args, **kwargs):
        super(KasaForm, self).__init__(*args, **kwargs)
        self.fields['Giris'].initial = 0.00  # Varsayılan değer
        self.fields['Cikis'].initial = 0.00  # Varsayılan değer
