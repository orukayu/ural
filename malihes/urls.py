from django.urls import path
from . import views


urlpatterns = [
    path('', views.base, name='baseurl'),
    path('giris/', views.giris, name='girisurl'),
    path('anasayfa/', views.anasayfa, name='anasayfaurl'),
    path('sefer-kayit/', views.sefer, name='seferurl'),
    path('sefer-listesi/', views.seferliste, name='seferlisteurl'),
    path('kasa-kayit/', views.tahsilat_ekle, name='kasaurl'),
    path('kasa-listesi/', views.kasaliste, name='kasalisteurl'),
    path('kasa-detay/<int:pk>/', views.kasadetay, name='kasadetayurl'),
    path('kasa-exceli-yukle/', views.kasaexceli, name='kasaexceliurl'),
    path('kasa-exceli-indir/', views.kasaexceliindir, name='kasaexceliindirurl'),
]