from django.conf import settings
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Soforler(models.Model):
    Isim = models.CharField(max_length=50)
    Telefon = PhoneNumberField(blank=True)


    class Meta:
        ordering = ['Isim',]  # Tablonun hangi başlığa göre sıralanacağını belirliyor

    def __str__(self):
        return self.Isim

class Kasa(models.Model):
    Tarih = models.DateField(blank=False)
    Plaka = models.CharField(max_length=25)
    Fisno = models.CharField(max_length=25)
    Sofor = models.CharField(max_length=25)
    Aciklama1 = models.CharField(max_length=25)
    Aciklama2 = models.CharField(max_length=25)
    Giris = models.DecimalField(max_digits=10, decimal_places=2)
    Cikis = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['Tarih',]  # Tablonun hangi başlığa göre sıralanacağını belirliyor

    def __str__(self):
        return str(self.Tarih)
