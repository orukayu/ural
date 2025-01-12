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
    path('kasa-sil/<int:pk>/', views.kasasil, name='kasasilurl'),
    path('kasa-exceli-yukle/', views.kasaexceli, name='kasaexceliurl'),
    path('kasa-exceli-indir/', views.kasaexceliindir, name='kasaexceliindirurl'),

    path('arac-kayit/', views.aracekle, name='aracurl'),
    path('arac-listesi/', views.aracliste, name='araclisteurl'),
    path('arac-detay/<int:pk>/', views.aracdetay, name='aracdetayurl'),
    path('arac-sil/<int:pk>/', views.aracsil, name='aracsilurl'),
    path('arac-exceli-yukle/', views.aracexceli, name='aracexceliurl'),
    path('arac-exceli-indir/', views.aracexceliindir, name='aracexceliindirurl')
]