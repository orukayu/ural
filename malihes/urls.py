from django.urls import path
from . import views


urlpatterns = [
    path('', views.base, name='baseurl'),
    path('giris/', views.giris, name='girisurl'),
    path('anasayfa/', views.anasayfa, name='anasayfaurl'),
    path('kasa/', views.kasa, name='kasaurl'),
    path('kasa-listesi/', views.kasaliste, name='kasalisteurl'),
]