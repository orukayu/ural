from django import forms
from .models import Kasa
from .models import Sefer


class KasaForm(forms.ModelForm):
    class Meta:
        model = Kasa
        fields = ['Tarih', 'Plaka', 'Fisno', 'Sofor']
        widgets = {
            'Tarih': forms.TextInput(attrs={'class': 'form-control', 'id': 'tarih'}),
            'Plaka': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '55 CKC 1919 - 34 DRS 567', 'id': 'plaka'}),
            'Fisno': forms.TextInput(attrs={'class': 'form-control', 'id': 'fisno', 'placeholder': '0019'}),
            'Sofor': forms.TextInput(attrs={'class': 'form-control', 'id': 'sofor', 'placeholder': 'Ali YILMAZ'}),
        }

    # Tarih için birden fazla format belirtiyoruz
    Tarih = forms.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y'],  # Kabul edilen formatlar
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '23.04.2025'}),
        required=True
    )

class TahsilatForm(forms.ModelForm):
    class Meta:
        model = Kasa
        fields = ['Aciklama1', 'Aciklama2', 'Giris', 'Cikis']
        widgets = {
            'Aciklama1': forms.TextInput(attrs={'class': 'form-control', 'id': 'aciklama1'}),
            'Aciklama2': forms.TextInput(attrs={'class': 'form-control', 'id': 'aciklama2'}),
            'Giris': forms.NumberInput(attrs={'class': 'form-control', 'id': 'giris'}),
            'Cikis': forms.NumberInput(attrs={'class': 'form-control', 'id': 'cikis'}),
        }

    def __init__(self, *args, **kwargs):
        super(TahsilatForm, self).__init__(*args, **kwargs)
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
            'Plakacekici',
            'Plakadorse',
            'Sofor',
            'Not',
            'Musteri',
            'Yuk',
            'Yol',
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
            'Plakacekici': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '55 ABC 1919', 'id': 'plaka'}),
            'Plakadorse': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '55 ABC 1919', 'id': 'plaka'}),
            'Sofor': forms.TextInput(attrs={'class': 'form-control', 'id': 'sofor'}),
            'Not': forms.Textarea(attrs={'class': 'form-control', 'id': 'not', 'rows': '4'}),
            'Musteri': forms.TextInput(attrs={'class': 'form-control', 'id': 'musteri'}),
            'Yuk': forms.TextInput(attrs={'class': 'form-control', 'id': 'yuk'}),
            'Yol': forms.NumberInput(attrs={'class': 'form-control', 'id': 'yol'}),
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

class TarihFiltreForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), 
        label="Başlangıç Tarihi"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), 
        label="Bitiş Tarihi"
    )