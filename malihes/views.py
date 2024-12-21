from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.db.models import Sum

from django.contrib.auth.models import User

import pandas as pd
from io import BytesIO
from django.http import HttpResponse

from .forms import KasaForm
from .forms import SeferForm

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
    kasaliste = Kasa.objects.all()
    tgt = Kasa.objects.filter(Giris__gt=0).aggregate(Sum('Giris'))["Giris__sum"]
    if tgt is None:
        tg = 0
    else:
        tg = tgt

    tct = Kasa.objects.filter(Cikis__gt=0).aggregate(Sum('Cikis'))["Cikis__sum"]
    if tct is None:
        tc = 0
    else:
        tc = tct


    kalan = tg - tc

    return render(request, 'malihes/kasaliste.html', {'kasaliste': kasaliste, 'tg': tg, 'tc': tc, 'kalan': kalan, 'kullanici_adi': kullanici_adi})

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