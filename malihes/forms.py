from django import forms
from .models import Kasa
from .models import Sefer

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

class SeferForm(forms.ModelForm):
    class Meta:
        model = Sefer
        fields = [
            'Cikisyeri',
            'Cikistarihi',
            'Cikiskm',
            'Varisyeri',
            'Varistarihi',
            'Variskm',
            'Plaka',
            'Sofor',
            'Not',
            'Musteri',
            'Yuk',
            'Tasimabedeli',
            'Dovizkuru',
            'Toplamfiyat',
            'Istasyon',
            'Litre',
            'Litrefiyati',
            'Toplamyakit',
            'Digergiderler',
            'Kalan'
        ]
        widgets = {
            'Cikisyeri': forms.TextInput(attrs={'class': 'form-control', 'id': 'cikisyeri'}),
            'Cikistarihi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '17/03/2025', 'id': 'cikistarihi'}),
            'Cikiskm': forms.NumberInput(attrs={'class': 'form-control', 'id': 'cikiskm'}),
            'Varisyeri': forms.TextInput(attrs={'class': 'form-control', 'id': 'varisyeri'}),
            'Varistarihi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '21/03/2025', 'id': 'varistarihi'}),
            'Variskm': forms.NumberInput(attrs={'class': 'form-control', 'id': 'variskm'}),
            'Plaka': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '55 ABC 1919', 'id': 'plaka'}),
            'Sofor': forms.TextInput(attrs={'class': 'form-control', 'id': 'sofor'}),
            'Not': forms.Textarea(attrs={'class': 'form-control', 'id': 'not', 'rows': '4'}),
            'Musteri': forms.TextInput(attrs={'class': 'form-control', 'id': 'musteri'}),
            'Yuk': forms.TextInput(attrs={'class': 'form-control', 'id': 'yuk'}),
            'Tasimabedeli': forms.NumberInput(attrs={'class': 'form-control', 'id': 'tasimabedeli'}),
            'Dovizkuru': forms.NumberInput(attrs={'class': 'form-control', 'id': 'dovizkuru'}),
            'Toplamfiyat': forms.NumberInput(attrs={'class': 'form-control', 'id': 'toplamfiyat'}),
            'Istasyon': forms.TextInput(attrs={'class': 'form-control', 'id': 'istasyon'}),
            'Litre': forms.NumberInput(attrs={'class': 'form-control', 'id': 'litre'}),
            'Litrefiyati': forms.NumberInput(attrs={'class': 'form-control', 'id': 'litrefiyati'}),
            'Toplamyakit': forms.NumberInput(attrs={'class': 'form-control', 'id': 'toplamyakit'}),
            'Digergiderler': forms.NumberInput(attrs={'class': 'form-control', 'id': 'digergiderler'}),
            'Kalan': forms.NumberInput(attrs={'class': 'form-control', 'id': 'kalan'}),
        }

    def __init__(self, *args, **kwargs):
        super(SeferForm, self).__init__(*args, **kwargs)
        self.fields['Cikiskm'].initial = 0  # Varsayılan değer
        self.fields['Variskm'].initial = 0  # Varsayılan değer
