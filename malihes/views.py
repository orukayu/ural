from django.shortcuts import render

def anasayfa(request):
    return render(request, 'malihes/anasayfa.html', {})
