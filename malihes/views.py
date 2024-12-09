from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

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

def kasakayit(request):
    return render(request, 'malihes/kasakayit.html')
