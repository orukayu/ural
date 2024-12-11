from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.db.models import Sum

from .forms import KasaForm

from .models import Kasa

def base(request):
    return redirect('girisurl')

def giris(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('anasayfaurl')  # Ana sayfa URL'inizi buraya yazın
        else:
            messages.error(request, 'Kullanıcı adı veya şifre yanlış.')
    return render(request, 'malihes/giris.html')

def anasayfa(request):
    return render(request, 'malihes/anasayfa.html')

def kasa(request):
    if request.method == 'POST':
        form = KasaForm(request.POST)
        if form.is_valid():
            form.save()  # Verileri doğrudan modelle ilişkilendir ve kaydet
            return redirect('kasaurl')  # Başka bir sayfaya yönlendirme yapabilirsiniz
    else:
        form = KasaForm()
    
    return render(request, 'malihes/kasa.html', {'form': form})

def kasaliste(request):
    kasaliste = Kasa.objects.all()
    tg = Kasa.objects.filter(Giris__gt=0).aggregate(Sum('Giris'))["Giris__sum"]
    tc = Kasa.objects.filter(Cikis__gt=0).aggregate(Sum('Cikis'))["Cikis__sum"]

    if tg is None:
        kalan = 0
    else:
        kalan = tg - tc

    return render(request, 'malihes/kasaliste.html', {'kasaliste': kasaliste, 'tg': tg, 'tc': tc, 'kalan': kalan})
