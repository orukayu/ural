from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import get_object_or_404

from django.db.models import Sum

from django.contrib.auth.models import User

import pandas as pd
from io import BytesIO
from django.http import HttpResponse

from .forms import KasaForm, TahsilatForm
from .forms import SeferForm
from .forms import TarihFiltreForm

from .models import Kasa
from .models import Sefer

def base(request):
    return redirect('girisurl')

def giris(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('seferurl')  # Ana sayfa URL'inizi buraya yazın
        else:
            messages.error(request, 'Kullanıcı adı veya şifre yanlış.')
    return render(request, 'malihes/giris.html')

def anasayfa(request):
    kullanici_adi = request.user.username
    return render(request, 'malihes/anasayfa.html', {'kullanici_adi': kullanici_adi})

def sefer(request):
    kullanici_adi = request.user.username

    if request.method == 'POST':
        form = SeferForm(request.POST)
        if form.is_valid():
            form.save()  # Verileri doğrudan modelle ilişkilendir ve kaydet
            return redirect('seferurl')  # Başka bir sayfaya yönlendirme yapabilirsiniz
    else:
        form = SeferForm()
    
    return render(request, 'malihes/sefer.html', {'form': form, 'kullanici_adi': kullanici_adi})

def seferliste(request):
    kullanici_adi = request.user.username
    seferliste = Sefer.objects.all()
    return render(request, 'malihes/seferliste.html', {'seferliste': seferliste, 'kullanici_adi': kullanici_adi})

def kasa(request):
    kullanici_adi = request.user.username
    if request.method == 'POST':
        form = KasaForm(request.POST)
        if form.is_valid():
            form.save()  # Verileri doğrudan modelle ilişkilendir ve kaydet
            return redirect('kasaurl')  # Başka bir sayfaya yönlendirme yapabilirsiniz
    else:
        form = KasaForm()
    
    return render(request, 'malihes/kasa.html', {'form': form, 'kullanici_adi': kullanici_adi})


def kasaliste(request):
    kullanici_adi = request.user.username
    form = TarihFiltreForm(request.GET or None)
    kasaliste = Kasa.objects.all()

    # Filtreleme
    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        if start_date and end_date:
            kasaliste = kasaliste.filter(Tarih__range=[start_date, end_date])

    toplam_giris = kasaliste.aggregate(giris_sum=Sum('Giris'))['giris_sum'] or 0
    toplam_cikis = kasaliste.aggregate(cikis_sum=Sum('Cikis'))['cikis_sum'] or 0
    kalan = toplam_giris - toplam_cikis

    context = {
        'kullanici_adi': kullanici_adi,
        'kasaliste': kasaliste,
        'form': form,
        'tg': toplam_giris,
        'tc': toplam_cikis,
        'kalan': kalan,
    }
    return render(request, 'malihes/kasaliste.html', context)


def kasaexceli(request):
    kullanici_adi = request.user.username
    if request.method == "POST":
        if 'excel_file' in request.FILES:
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)

            # NaN değerleri None ile değiştirme
            df = df.where(pd.notnull(df), None)
            
            for index, row in df.iterrows():
                kasa = Kasa(
                    Tarih = row['Tarih'],
                    Plaka = row['Plaka'],
                    Fisno = row['Fiş No'],
                    Sofor = row['Şoför'],
                    Aciklama1 = row['Açıklama 1'],
                    Aciklama2 = row['Açıklama 2'],
                    Giris=row['Giren'] if row['Giren'] is not None else 0.00,  # Varsayılan değer
                    Cikis=row['Çıkan'] if row['Çıkan'] is not None else 0.00,  # Varsayılan değer
                )
                kasa.save()
            
            return redirect('kasalisteurl')

    return render(request, 'malihes/kasaexceli.html', {'kullanici_adi': kullanici_adi})


def kasaexceliindir(request):

    # Kasa modelinden tüm verileri al
    kasalar = Kasa.objects.all()

    # Kasa verilerini bir DataFrame'e dönüştür
    data = {
        'Tarih': [kasa.Tarih.strftime('%d.%m.%Y') for kasa in kasalar],
        'Plaka': [kasa.Plaka for kasa in kasalar],
        'Fiş No': [kasa.Fisno for kasa in kasalar],
        'Şoför': [kasa.Sofor for kasa in kasalar],
        'Açıklama 1': [kasa.Aciklama1 for kasa in kasalar],
        'Açıklama 2': [kasa.Aciklama2 for kasa in kasalar],
        'Giren': [float(kasa.Giris) for kasa in kasalar],
        'Çıkan': [float(kasa.Cikis) for kasa in kasalar],
    }
    df = pd.DataFrame(data)

    # DataFrame'i Excel dosyasına dönüştür
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)  # Buffer'ın başına git

    # HTTP yanıtı olarak Excel dosyasını döndür
    response = HttpResponse(excel_buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="ural_kasa_exceli.xlsx"'

    return response


def tahsilat_ekle(request):
    kullanici_adi = request.user.username
    if request.method == 'POST':
        kasa_form = KasaForm(request.POST)  # Kasa bilgileri için formu alıyoruz
        tahsilat_forms = [TahsilatForm(request.POST, prefix=str(i)) for i in range(5)]  # Tahsilat formunu 5 satır olarak alıyoruz

        if kasa_form.is_valid():
            # Kasa formundan bilgileri al
            tarih = kasa_form.cleaned_data['Tarih']
            plaka = kasa_form.cleaned_data['Plaka']
            fisno = kasa_form.cleaned_data['Fisno']
            sofor = kasa_form.cleaned_data['Sofor']

            # Her bir tahsilat formunu kontrol ediyoruz
            for tahsilat_form in tahsilat_forms:
                if tahsilat_form.is_valid():  # Her formun geçerli olup olmadığını kontrol et
                    aciklama1 = tahsilat_form.cleaned_data.get('Aciklama1')
                    aciklama2 = tahsilat_form.cleaned_data.get('Aciklama2')
                    giris = tahsilat_form.cleaned_data.get('Giris')
                    cikis = tahsilat_form.cleaned_data.get('Cikis')

                    # Eğer tahsilat satırı doluysa veritabanına kaydet
                    if aciklama1 or aciklama2 or giris or cikis:
                        Kasa.objects.create(  # Burada model kaydı yapıyoruz
                            Tarih=tarih,
                            Plaka=plaka,
                            Fisno=fisno,
                            Sofor=sofor,
                            Aciklama1=aciklama1,
                            Aciklama2=aciklama2,
                            Giris=giris or 0.00,  # Eğer giriş boşsa varsayılan 0.00 olarak kaydediyoruz
                            Cikis=cikis or 0.00   # Eğer çıkış boşsa varsayılan 0.00 olarak kaydediyoruz
                        )
            return redirect('kasalisteurl')  # İşlem tamamlanınca listeleme sayfasına yönlendiriyoruz

    else:
        # GET isteğinde formları boş bir şekilde oluştur
        kasa_form = KasaForm()
        tahsilat_forms = [TahsilatForm(prefix=str(i)) for i in range(5)]

    return render(request, 'malihes/kasa.html', {'kasa_form': kasa_form, 'tahsilat_forms': tahsilat_forms, 'kullanici_adi': kullanici_adi})


def kasadetay_eski(request, pk):
    kullanici_adi = request.user.username
    kontrolkasa = get_object_or_404(Kasa, pk=pk)
    form = KasaForm(instance=kontrolkasa)
    return render(request, 'malihes/kasadetay.html', {'form': form, 'kullanici_adi': kullanici_adi})

def kasadetay(request, pk):
    kullanici_adi = request.user.username
    kontrolkasa = get_object_or_404(Kasa, pk=pk)
    if request.method == 'POST':
        form = KasaForm(request.POST, instance=kontrolkasa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kasa kaydı başarıyla güncellendi.')
            return redirect('kasa_listesi')  # Liste sayfasına yönlendirme
        else:
            messages.error(request, 'Formda hatalar var. Lütfen kontrol edin.')
    else:
        form = KasaForm(instance=kontrolkasa)

    return render(request, 'malihes/kasadetay.html', {'form': form, 'kullanici_adi': kullanici_adi})