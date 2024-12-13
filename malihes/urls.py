from django.urls import path
from . import views


urlpatterns = [
    path('', views.base, name='baseurl'),
    path('giris/', views.giris, name='girisurl'),
    path('sefer-kayit/', views.sefer, name='seferurl'),
    path('kasa-kayit/', views.kasa, name='kasaurl'),
    path('kasa-listesi/', views.kasaliste, name='kasalisteurl'),
]