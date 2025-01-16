from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404

from django.db.models import Sum

from django.contrib.auth.models import User

import pandas as pd
from io import BytesIO
from django.http import HttpResponse
from datetime import datetime

from .forms import KasaForm, TahsilatForm
from .forms import SeferForm
from .forms import TarihFiltreForm
from .forms import AraclarForm

from .models import Kasa
from .models import Sefer
from .models import Araclar

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

@login_required(login_url='/giris/')
def anasayfa(request):
    kullanici_adi = request.user.username
    ucs = Araclar.objects.filter(Firma='Ural Lojistik', Tür='Çekici').count()
    uds = Araclar.objects.filter(Firma='Ural Lojistik', Tür='Dorse').count()
    acs = Araclar.objects.filter(Firma='Asya Fresh', Tür='Çekici').count()
    ads = Araclar.objects.filter(Firma='Asya Fresh', Tür='Dorse').count()

    context = {
        'kullanici_adi': kullanici_adi,
        'ucs': ucs,
        'uds': uds,
        'acs': acs,
        'ads': ads
    }
    return render(request, 'malihes/anasayfa.html', context)

@login_required(login_url='/giris/')
def sefer(request):
    kullanici_adi = request.user.username

    if request.method == 'POST':
        form = SeferForm(request.POST)
        if form.is_valid():
            form.save()  # Verileri doğrudan modelle ilişkilendir ve kaydet
            return redirect('seferurl')  # Başka bir sayfaya yönlendirme yapabilirsiniz
    else:
        form = SeferForm()

    context = {
        'kullanici_adi': kullanici_adi,
        'form': form
    }
    return render(request, 'malihes/sefer.html', context)

@login_required(login_url='/giris/')
def seferliste(request):
    kullanici_adi = request.user.username
    seferliste = Sefer.objects.all()

    context = {
        'seferliste': seferliste,
        'kullanici_adi': kullanici_adi
    }
    return render(request, 'malihes/seferliste.html', context)

@login_required(login_url='/giris/')
def seferdetay(request, pk):
    kullanici_adi = request.user.username
    sefer_instance = get_object_or_404(Sefer, pk=pk)

    if request.method == 'POST':
        sefer_form = SeferForm(request.POST, instance=sefer_instance)
        if sefer_form.is_valid():
            # Formdan gelen verileri kaydet
            post = sefer_form.save()
            post.save()
            messages.success(request, "Kayıt başarıyla güncellendi.")
            return redirect('seferlisteurl')  # Liste sayfasına yönlendirin
        else:
            messages.error(request, "Formda hatalar var. Lütfen kontrol edin.")

    else:
        # Tarihi biçimlendirmek için strftime kullanıyoruz
        formatted_date1 = sefer_instance.Cikistarihi.strftime('%d.%m.%Y') if sefer_instance.Cikistarihi else ''
        formatted_date2 = sefer_instance.Varistarihi.strftime('%d.%m.%Y') if sefer_instance.Varistarihi else ''
        # GET isteğinde formları mevcut kayıtla doldur
        sefer_form = SeferForm(initial={
            'Plakacekici': sefer_instance.Plakacekici,
            'Plakadorse': sefer_instance.Plakadorse,
            'Sofor': sefer_instance.Sofor,
            'Cikistarihi': formatted_date1,
            'Cikisyeri': sefer_instance.Cikisyeri,
            'Cikiskm': sefer_instance.Cikiskm,
            'Varistarihi': formatted_date2,
            'Varisyeri': sefer_instance.Varisyeri,
            'Variskm': sefer_instance.Variskm,
            'Musteri': sefer_instance.Musteri,
            'Yuk': sefer_instance.Yuk,
            'Yol': sefer_instance.Yol,
            'Tasimabedeli': sefer_instance.Tasimabedeli,
            'Dovizkuru': sefer_instance.Dovizkuru,
            'Toplamfiyat': sefer_instance.Toplamfiyat,
            'Istasyon': sefer_instance.Istasyon,
            'Litre': sefer_instance.Litre,
            'Litrefiyati': sefer_instance.Litrefiyati,
            'Toplamyakit': sefer_instance.Toplamyakit,
            'Not': sefer_instance.Not,
            'Digergiderler': sefer_instance.Digergiderler,
            'Kalan': sefer_instance.Kalan
        })

    return render(request, 'malihes/seferdetay.html', {'sefer_form': sefer_form, 'kullanici_adi': kullanici_adi, 'pk': pk})

@login_required(login_url='/giris/')
def sefersil(request, pk):
    sefer_instance = get_object_or_404(Sefer, pk=pk)
    sefer_instance.delete()
    messages.success(request, "Kayıt başarıyla silindi.")
    return redirect('seferlisteurl')

@login_required(login_url='/giris/')
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

@login_required(login_url='/giris/')
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

@login_required(login_url='/giris/')
def tahsilat_ekle(request):
    kullanici_adi = request.user.username
    if request.method == 'POST':
        kasa_form = KasaForm(request.POST)  # Kasa bilgileri için formu alıyoruz
        tahsilat_form_count = int(request.POST.get('form_count', 0))  # Dinamik form sayısını al
        tahsilat_forms = [TahsilatForm(request.POST, prefix=str(i)) for i in range(tahsilat_form_count)]

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
                    giris = tahsilat_form.cleaned_data.get('Giris') or 0.00
                    cikis = tahsilat_form.cleaned_data.get('Cikis') or 0.00

                    # Eğer tahsilat satırı doluysa veritabanına kaydet
                    if aciklama1 or aciklama2 or giris or cikis:
                        Kasa.objects.create(  # Burada model kaydı yapıyoruz
                            Tarih=tarih,
                            Plaka=plaka,
                            Fisno=fisno,
                            Sofor=sofor,
                            Aciklama1=aciklama1,
                            Aciklama2=aciklama2,
                            Giris=giris,  # Eğer giriş boşsa varsayılan 0.00 olarak kaydediyoruz
                            Cikis=cikis,   # Eğer çıkış boşsa varsayılan 0.00 olarak kaydediyoruz
                        )
            return redirect('kasaurl')  # İşlem tamamlanınca listeleme sayfasına yönlendiriyoruz

    else:
        # GET isteğinde formları boş bir şekilde oluştur
        kasa_form = KasaForm()
        tahsilat_forms = [TahsilatForm(prefix=str(i)) for i in range(1)]
        sonkayit = Kasa.objects.all()[:1].get()

    return render(request, 'malihes/kasa.html', {'kasa_form': kasa_form, 'tahsilat_forms': tahsilat_forms, 'kullanici_adi': kullanici_adi, 'sonkayit': sonkayit})

@login_required(login_url='/giris/')
def kasadetay(request, pk):
    kullanici_adi = request.user.username
    kasa_instance = get_object_or_404(Kasa, pk=pk)

    if request.method == 'POST':
        kasa_form = KasaForm(request.POST, instance=kasa_instance)
        tahsilat_form = TahsilatForm(request.POST, instance=kasa_instance)

        if kasa_form.is_valid() and tahsilat_form.is_valid():
            # Formdan gelen verileri kaydet
            kasa_form.save()
            tahsilat_form.save()
            messages.success(request, "Kayıt başarıyla güncellendi.")
            return redirect('kasalisteurl')  # Liste sayfasına yönlendirin
        else:
            messages.error(request, "Formda hatalar var. Lütfen kontrol edin.")

    else:
        # Tarihi biçimlendirmek için strftime kullanıyoruz
        formatted_date = kasa_instance.Tarih.strftime('%d.%m.%Y') if kasa_instance.Tarih else ''
        # GET isteğinde formları mevcut kayıtla doldur
        kasa_form = KasaForm(initial={
            'Tarih': formatted_date,
            'Plaka': kasa_instance.Plaka,
            'Fisno': kasa_instance.Fisno,
            'Sofor': kasa_instance.Sofor
        })
        tahsilat_form = TahsilatForm(instance=kasa_instance)

    return render(request, 'malihes/kasadetay.html', {'kasa_form': kasa_form, 'tahsilat_form': tahsilat_form, 'kullanici_adi': kullanici_adi, 'pk': pk})

@login_required(login_url='/giris/')
def kasasil(request, pk):
    kasa_instance = get_object_or_404(Kasa, pk=pk)
    kasa_instance.delete()
    messages.success(request, "Kayıt başarıyla silindi.")
    return redirect('kasalisteurl')

@login_required(login_url='/giris/')
def aracekle(request):
    kullanici_adi = request.user.username
    
    if request.method == 'POST':
        form = AraclarForm(request.POST)
        if form.is_valid():
            plaka = form.cleaned_data['Plaka']
            kontrol = Araclar.objects.filter(Plaka=plaka).count()
            if kontrol < 1:
                post = form.save(commit=False)
                post.save1()  # Verileri doğrudan modelle ilişkilendir ve kaydet
                return redirect('araclisteurl')  # Başka bir sayfaya yönlendirme yapabilirsiniz
            else:
                form.add_error('Plaka', 'Bu plaka kayıtlıdır!')
    else:
        form = AraclarForm()

    return render(request, 'malihes/aracekle.html', {'kullanici_adi': kullanici_adi, 'form': form})

@login_required(login_url='/giris/')
def aracliste(request):
    kullanici_adi = request.user.username
    aracliste = Araclar.objects.all()
    toplam_sigorta = aracliste.aggregate(Sigtutari_sum=Sum('Sigtutari'))['Sigtutari_sum'] or 0
    toplam_kasko = aracliste.aggregate(Kastutari_sum=Sum('Kastutari'))['Kastutari_sum'] or 0
    toplam = aracliste.aggregate(Toplamtutar_sum=Sum('Toplamtutar'))['Toplamtutar_sum'] or 0
    
    return render(request, 'malihes/aracliste.html', {'aracliste': aracliste, 'kullanici_adi': kullanici_adi, 'ts': toplam_sigorta, 'tk': toplam_kasko, 'toplam': toplam})

@login_required(login_url='/giris/')
def aracdetay(request, pk):
    kullanici_adi = request.user.username
    arac_instance = get_object_or_404(Araclar, pk=pk)

    if request.method == 'POST':
        arac_form = AraclarForm(request.POST, instance=arac_instance)
        if arac_form.is_valid():
            # Formdan gelen verileri kaydet
            post = arac_form.save()
            post.save()
            messages.success(request, "Kayıt başarıyla güncellendi.")
            return redirect('araclisteurl')  # Liste sayfasına yönlendirin
        else:
            messages.error(request, "Formda hatalar var. Lütfen kontrol edin.")

    else:
        # Tarihi biçimlendirmek için strftime kullanıyoruz
        formatted_date1 = arac_instance.Sigbastarihi.strftime('%d.%m.%Y') if arac_instance.Sigbastarihi else ''
        formatted_date2 = arac_instance.Sigbittarihi.strftime('%d.%m.%Y') if arac_instance.Sigbittarihi else ''
        formatted_date3 = arac_instance.Kasbastarihi.strftime('%d.%m.%Y') if arac_instance.Kasbastarihi else ''
        formatted_date4 = arac_instance.Kasbittarihi.strftime('%d.%m.%Y') if arac_instance.Kasbittarihi else ''
        # GET isteğinde formları mevcut kayıtla doldur
        arac_form = AraclarForm(initial={
            'Plaka': arac_instance.Plaka,
            'Firma': arac_instance.Firma,
            'Tür': arac_instance.Tür,
            'Marka': arac_instance.Marka,
            'Model': arac_instance.Model,
            'Sigbastarihi': formatted_date1,
            'Sigbittarihi': formatted_date2,
            'Sigtutari': arac_instance.Sigtutari,
            'Kasbastarihi': formatted_date3,
            'Kasbittarihi': formatted_date4,
            'Kastutari': arac_instance.Kastutari,
            'Toplamtutar': arac_instance.Toplamtutar,
            'Ayliktutar': arac_instance.Ayliktutar
        })

    return render(request, 'malihes/aracdetay.html', {'arac_form': arac_form, 'kullanici_adi': kullanici_adi, 'pk': pk})

@login_required(login_url='/giris/')
def aracsil(request, pk):
    arac_instance = get_object_or_404(Araclar, pk=pk)
    arac_instance.delete()
    messages.success(request, "Kayıt başarıyla silindi.")
    return redirect('araclisteurl')

@login_required(login_url='/giris/')
def aracexceli(request):
    kullanici_adi = request.user.username
    if request.method == "POST":
        if 'excel_file' in request.FILES:
            excel_file = request.FILES['excel_file']
            
            # Excel dosyasını okurken tarihleri otomatik tanı
            df = pd.read_excel(excel_file, dtype={'Sig. Baş. Tarihi': str, 'Sig. Bit. Tarihi': str, 
                                                  'Kas. Baş. Tarihi': str, 'Kas. Bit. Tarihi': str})

            # NaN değerlerini None ile değiştir
            df = df.where(pd.notnull(df), None)

            for index, row in df.iterrows():
                # Tarih alanlarını kontrol edip None ya da datetime.date olarak ayarla
                def parse_date(value):
                    if value is None or value == '':
                        return None  # Boş ise None kaydediyoruz
                    try:
                        return pd.to_datetime(value, dayfirst=True).date()
                    except:
                        return None  # Hatalı tarih varsa yine None

                # Sigorta ve Kasko tutarları boşsa 0 olarak ayarlanıyor
                sigtutari = row['Sigorta Tutarı'] if row['Sigorta Tutarı'] else 0
                kastutari = row['Kasko Tutarı'] if row['Kasko Tutarı'] else 0

                # Araclar modeline verileri kaydetme
                arac = Araclar(
                    Plaka=row['Plaka'],
                    Firma=row['Firma'],
                    Tür=row['Tür'],
                    Marka=row['Marka'],
                    Model=row['Model'],
                    Sigbastarihi=parse_date(row['Sig. Baş. Tarihi']),
                    Sigbittarihi=parse_date(row['Sig. Bit. Tarihi']),
                    Sigtutari=sigtutari,
                    Kasbastarihi=parse_date(row['Kas. Baş. Tarihi']),
                    Kasbittarihi=parse_date(row['Kas. Bit. Tarihi']),
                    Kastutari=kastutari,
                )
                arac.save1()  # Hesaplamaların yapılması için save1 kullanıyoruz

            return redirect('araclisteurl')

    return render(request, 'malihes/aracexceli.html', {'kullanici_adi': kullanici_adi})

@login_required(login_url='/giris/')
def aracexceliindir(request):
    # Araclar modelinden tüm verileri al
    araclar = Araclar.objects.all()

    # Araclar verilerini bir DataFrame'e dönüştür
    data = {
        'Plaka': [arac.Plaka for arac in araclar],
        'Firma': [arac.Firma for arac in araclar],
        'Tür': [arac.Tür for arac in araclar],
        'Marka': [arac.Marka for arac in araclar],
        'Model': [arac.Model for arac in araclar],
        'Sig. Baş. Tarihi': [arac.Sigbastarihi if arac.Sigbastarihi else '' for arac in araclar],
        'Sig. Bit. Tarihi': [arac.Sigbittarihi if arac.Sigbittarihi else '' for arac in araclar],
        'Sigorta Tutarı': [float(arac.Sigtutari) for arac in araclar],
        'Kas. Baş. Tarihi': [arac.Kasbastarihi if arac.Kasbastarihi else '' for arac in araclar],
        'Kas. Bit. Tarihi': [arac.Kasbittarihi if arac.Kasbittarihi else '' for arac in araclar],
        'Kasko Tutarı': [float(arac.Kastutari) for arac in araclar],
        'Toplam Tutar': [float(arac.Toplamtutar) for arac in araclar],
    }
    df = pd.DataFrame(data)

    # DataFrame'i Excel dosyasına dönüştür
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Araçlar')
        workbook = writer.book
        worksheet = writer.sheets['Araçlar']
        
        # Sütun genişliklerini ayarlama
        for i, col in enumerate(df.columns):
            max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(i, i, max_len)

    excel_buffer.seek(0)

    response = HttpResponse(excel_buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="ural_arac_exceli.xlsx"'

    return response

@login_required(login_url='/giris/')
def kasaexceliindir(request):
    # Kasa modelinden tüm verileri al
    kasalar = Kasa.objects.all()

    # Kasa verilerini bir DataFrame'e dönüştür
    data = {
        'Tarih': [kasa.Tarih for kasa in kasalar],
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

    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Kasa')
        workbook = writer.book
        worksheet = writer.sheets['Kasa']
        
        # Sütun genişliklerini ayarlama
        for i, col in enumerate(df.columns):
            max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(i, i, max_len)
    

    excel_buffer.seek(0)  # Buffer'ın başına git

    # HTTP yanıtı olarak Excel dosyasını döndür
    response = HttpResponse(excel_buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="ural_kasa_exceli.xlsx"'

    return response