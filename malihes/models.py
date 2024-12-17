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
    Plaka = models.CharField(max_length=25, null=True, blank=True)
    Fisno = models.CharField(max_length=25, null=True, blank=True)
    Sofor = models.CharField(max_length=25, null=True, blank=True)
    Aciklama1 = models.CharField(max_length=25, null=True, blank=True)
    Aciklama2 = models.CharField(max_length=25, null=True, blank=True)
    Giris = models.DecimalField(max_digits=10, decimal_places=2)
    Cikis = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-Tarih',]  # Tablonun hangi başlığa göre sıralanacağını belirliyor

    def __str__(self):
        return str(self.Tarih)


class Sefer(models.Model):
    Plaka = models.CharField(max_length=25)
    Sofor = models.TextField()
    Cikisyeri = models.TextField()
    Cikistarihi = models.DateField()
    Cikiskm = models.DecimalField(max_digits=10, decimal_places=0)
    Varisyeri = models.TextField()
    Varistarihi = models.DateField()
    Variskm = models.DecimalField(max_digits=10, decimal_places=0)
    Not = models.TextField()
    Musteri = models.TextField()
    Yuk = models.TextField()
    Tasimabedeli = models.DecimalField(max_digits=10, decimal_places=2)
    Dovizkuru = models.DecimalField(max_digits=10, decimal_places=4)
    Toplamfiyat = models.DecimalField(max_digits=10, decimal_places=2)
    Istasyon = models.TextField()
    Litre = models.DecimalField(max_digits=10, decimal_places=2)
    Litrefiyati = models.DecimalField(max_digits=10, decimal_places=2)
    Toplamyakit = models.DecimalField(max_digits=10, decimal_places=2)
    Digergiderler = models.DecimalField(max_digits=10, decimal_places=2)
    Kalan = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['Plaka',]  # Tablonun hangi başlığa göre sıralanacağını belirliyor

    def __str__(self):
        return self.Plaka
