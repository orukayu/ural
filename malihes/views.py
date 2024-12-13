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
            return redirect('seferurl')  # Ana sayfa URL'inizi buraya yazın
        else:
            messages.error(request, 'Kullanıcı adı veya şifre yanlış.')
    return render(request, 'malihes/giris.html')

def sefer(request):
    return render(request, 'malihes/sefer.html')

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

    return render(request, 'malihes/kasaliste.html', {'kasaliste': kasaliste, 'tg': tg, 'tc': tc, 'kalan': kalan})
