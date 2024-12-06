from django.shortcuts import render

def girisyap(request):
    return render(request, 'malihes/giris.html', {})
