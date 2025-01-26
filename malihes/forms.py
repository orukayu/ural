from django import forms
from .models import Kasa
from .models import Sefer
from .models import Araclar
from .models import Personel


class PersonelForm(forms.ModelForm):
    class Meta:
        model = Personel
        fields = ['Adsoyad', 'Bolum', 'Telefon', 'Maas']
        widgets = {
            'Adsoyad': forms.TextInput(attrs={'class': 'form-control', 'id': 'adsoyad', 'placeholder': 'Ali YILMAZ'}),
            'Telefon': forms.TextInput(attrs={'class': 'form-control', 'id': 'telefon', 'placeholder': '+905001112233 formatında giriniz'}),
            'Maas': forms.NumberInput(attrs={'class': 'form-control', 'id': 'maas'}),
        }

    BOLUMLER = [
    ('Dış Ticaret', 'Dış Ticaret'),
    ('Oto Bakım Onarımcısı', 'Oto Bakım Onarımcısı'),
    ('Oto Yıkama Elemanı', 'Oto Yıkama Elemanı'),
    ('Sevkiyat Görevlisi', 'Sevkiyat Görevlisi'),
    ('Şoför', 'Şoför'),
    ('Tır Çekici Şoförü', 'Tır Çekici Şoförü'),
    ('Tır Şoförü', 'Tır Şoförü'),
    ('Diğer...', 'Diğer...'),
    ]

    Bolum = forms.ChoiceField(
        choices=BOLUMLER,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'bolum'}),
        initial='Diğer...'
    )


class KasaForm(forms.ModelForm):
    class Meta:
        model = Kasa
        fields = ['Tarih', 'Plaka', 'Fisno', 'Sofor']
        widgets = {
            'Tarih': forms.TextInput(attrs={'class': 'form-control', 'id': 'tarih'}),
            'Plaka': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '55 CKC 1919 - 34 DRS 567', 'id': 'kasaplaka'}),
            'Fisno': forms.TextInput(attrs={'class': 'form-control', 'id': 'fisno', 'placeholder': '0019'}),
            'Sofor': forms.TextInput(attrs={'class': 'form-control', 'id': 'sofor', 'name': 'sofor', 'autocomplete': 'off', 'placeholder': 'Ali YILMAZ'}),
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
            'Plakacekici', 'Plakadorse', 'Sofor', 'Cikistarihi', 'Cikisyeri', 'Cikiskm',
            'Varistarihi', 'Varisyeri', 'Variskm', 'Musteri', 'Yuk', 'Yol', 'Tasimabedeli',
            'Dovizkuru', 'Toplamfiyat', 'Istasyon', 'Litre', 'Litrefiyati', 'Toplamyakit',
            'Not', 'Digergiderler', 'Kalan'
        ]
        widgets = {
            'Cikisyeri': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Samsun-Mersin', 'id': 'cikisyeri'}),
            'Cikiskm': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_Cikiskm'}),
            'Varisyeri': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mersin-Samsun', 'id': 'varisyeri'}),
            'Variskm': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_Variskm'}),
            'Plakacekici': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '55 CKC 1919', 'id': 'cekiciplaka'}),
            'Plakadorse': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12 DRS 345', 'id': 'dorseplaka'}),
            'Not': forms.Textarea(attrs={'class': 'form-control', 'id': 'not', 'rows': '4'}),
            'Musteri': forms.TextInput(attrs={'class': 'form-control', 'id': 'musteri'}),
            'Yuk': forms.TextInput(attrs={'class': 'form-control', 'id': 'yuk'}),
            'Yol': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_Yol'}),
            'Dovizkuru': forms.NumberInput(attrs={'class': 'form-control', 'id': 'Dovizkuru', 'name': 'Dovizkuru'}),
            'Toplamfiyat': forms.NumberInput(attrs={'class': 'form-control', 'id': 'toplamfiyat'}),
            'Istasyon': forms.TextInput(attrs={'class': 'form-control', 'id': 'istasyon'}),
            'Litre': forms.NumberInput(attrs={'class': 'form-control', 'id': 'litre'}),
            'Litrefiyati': forms.NumberInput(attrs={'class': 'form-control', 'id': 'litrefiyati'}),
            'Toplamyakit': forms.NumberInput(attrs={'class': 'form-control', 'id': 'toplamyakit'}),
            'Digergiderler': forms.NumberInput(attrs={'class': 'form-control', 'id': 'digergiderler'}),
            'Kalan': forms.NumberInput(attrs={'class': 'form-control', 'id': 'kalan'})
        }

    Cikistarihi = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'cikistarihi'}),
    )

    Varistarihi = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'Varistarihi'}),
        required=False,
    )

    Tasimabedeli = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'tasimabedeli'})
    )

    Sofor = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'sofor'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Varsayılan değerleri atama
        default_values = {
            'Cikiskm': 0, 'Variskm': 0, 'Yol': 0, 'Tasimabedeli': 0.0,
            'Dovizkuru': 0.0, 'Toplamfiyat': 0.0, 'Litre': 0.0, 'Litrefiyati': 0.0, 'Toplamyakit': 0.0
        }
        for field, value in default_values.items():
            self.fields[field].initial = value

        # Kasa modelinde 'Açıklama1' sütunu 'Harcırah' olan şoförleri al
        harcırah_soforler = Kasa.objects.filter(Aciklama1='Harcırah').values_list('Sofor', flat=True)

        # Sefer modelinde kullanılan şoförleri al
        kullanılan_soforler = Sefer.objects.values_list('Sofor', flat=True)

        # Kullanılabilir şoförleri filtrele
        mevcut_soforler = set(harcırah_soforler) - set(kullanılan_soforler)

        # Dropdown için seçenekleri belirle
        self.fields['Sofor'].choices = [(sofor, sofor) for sofor in mevcut_soforler]



class TarihFiltreForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), 
        label="Başlangıç Tarihi"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), 
        label="Bitiş Tarihi"
    )

class AraclarForm(forms.ModelForm):
    class Meta:
        model = Araclar
        fields = [
            'Plaka',
            'Firma',
            'Tür',
            'Marka',
            'Model',
            'Sigbastarihi',
            'Sigbittarihi',
            'Sigtutari',
            'Kasbastarihi',
            'Kasbittarihi',
            'Kastutari',
            'Toplamtutar',
            'Ayliktutar'
        ]
        widgets = {
            'Plaka': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '55 ABC 1919', 'id': 'plaka'}),
            'Marka': forms.TextInput(attrs={'class': 'form-control', 'id': 'marka'}),
            'Model': forms.TextInput(attrs={'class': 'form-control', 'id': 'model'}),
            'Sigtutari': forms.NumberInput(attrs={'class': 'form-control', 'id': 'sigtutari'}),
            'Kastutari': forms.NumberInput(attrs={'class': 'form-control', 'id': 'kastutari'}),
            'Toplamtutar': forms.NumberInput(attrs={'class': 'form-control', 'id': 'toplamtutar'}),
            'Ayliktutar': forms.NumberInput(attrs={'class': 'form-control', 'id': 'ayliktutar'}),
        }

    # Firma için seçenekler
    FIRMALAR = [
        ('Asya Fresh', 'Asya Fresh'),
        ('Ural Lojistik', 'Ural Lojistik'),
    ]

    Firma = forms.ChoiceField(
        choices=FIRMALAR,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'firma'}),
        initial='Ural Lojistik'
    )

    TURLER = [
        ('Çekici', 'Çekici'),
        ('Dorse', 'Dorse'),
    ]

    Tür = forms.ChoiceField(
        choices=TURLER,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'tur'}),
        initial='Çekici'
    )

    Sigbastarihi = forms.DateField(
        required=False,
        input_formats=['%d/%m/%Y', '%d.%m.%Y'],  # Kabul edilen formatlar
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '17.03.2025', 'id': 'sigbastarihi'})
    )

    Sigbittarihi = forms.DateField(
        required=False,
        input_formats=['%d/%m/%Y', '%d.%m.%Y'],  # Kabul edilen formatlar
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '17.03.2025', 'id': 'sigbittarihi'})
    )

    Kasbastarihi = forms.DateField(
        required=False,
        input_formats=['%d/%m/%Y', '%d.%m.%Y'],  # Kabul edilen formatlar
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '17.03.2025', 'id': 'kasbastarihi'})
    )

    Kasbittarihi = forms.DateField(
        required=False,
        input_formats=['%d/%m/%Y', '%d.%m.%Y'],  # Kabul edilen formatlar
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '17.03.2025', 'id': 'kasbittarihi'})
    )

    def __init__(self, *args, **kwargs):
        super(AraclarForm, self).__init__(*args, **kwargs)
        self.fields['Sigtutari'].initial = 0.00  # Varsayılan değer
        self.fields['Kastutari'].initial = 0.00  # Varsayılan değer
        self.fields['Toplamtutar'].initial = 0.00  # Varsayılan değer
        self.fields['Ayliktutar'].initial = 0.00  # Varsayılan değer