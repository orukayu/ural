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
    Sofor = models.CharField(max_length=35, null=True, blank=True)
    Aciklama1 = models.CharField(max_length=50, null=True, blank=True)
    Aciklama2 = models.CharField(max_length=50, null=True, blank=True)
    Giris = models.DecimalField(max_digits=10, decimal_places=2)
    Cikis = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-Tarih', '-id']  # Tablonun hangi başlığa göre sıralanacağını belirliyor

    def __str__(self):
        return str(self.Tarih)


class Sefer(models.Model):
    Plakacekici = models.CharField(max_length=25)
    Plakadorse = models.CharField(max_length=25, null=True)
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
    Yol = models.DecimalField(max_digits=10, decimal_places=2, null=True)
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
        ordering = ['Plakacekici',]  # Tablonun hangi başlığa göre sıralanacağını belirliyor

    def __str__(self):
        return self.Plakacekici


class Araclar(models.Model):
    Plaka = models.CharField(max_length=25)
    Firma = models.CharField(max_length=25, null=True, blank=True)
    Tür = models.CharField(max_length=25, null=True, blank=True)
    Marka = models.CharField(max_length=25, null=True, blank=True)
    Model = models.CharField(max_length=25, null=True, blank=True)
    Sigbastarihi = models.DateField(blank=True, null=True)
    Sigbittarihi = models.DateField(blank=True, null=True)
    Sigtutari = models.DecimalField(max_digits=10, decimal_places=2)
    Kasbastarihi = models.DateField(blank=True, null=True)
    Kasbittarihi = models.DateField(blank=True, null=True)
    Kastutari = models.DecimalField(max_digits=10, decimal_places=2)
    Toplamtutar = models.DecimalField(max_digits=10, decimal_places=2)
    Ayliktutar = models.DecimalField(max_digits=10, decimal_places=2)

    def save1(self, *args, **kwargs):
        self.Toplamtutar = self.Sigtutari + self.Kastutari
        self.Ayliktutar = self.Toplamtutar / 12
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['Firma', '-Tür', 'Plaka']  # Tablonun hangi başlığa göre sıralanacağını belirliyor

    def __str__(self):
        return self.Plaka
