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
    Plakadorse = models.CharField(max_length=25, null=True, blank=True)
    Sofor = models.TextField(null=True, blank=True)
    Cikistarihi = models.DateField()
    Cikisyeri = models.TextField(null=True, blank=True)
    Cikiskm = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    Varistarihi = models.DateField(blank=True, null=True)
    Varisyeri = models.TextField(null=True, blank=True)
    Variskm = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    Musteri = models.TextField(null=True, blank=True)
    Yuk = models.TextField(null=True, blank=True)
    Yol = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Tasimabedeli = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Dovizkuru = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    Toplamfiyat = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Istasyon = models.TextField(null=True, blank=True)
    Litre = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Litrefiyati = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Toplamyakit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Not = models.TextField(null=True, blank=True)
    Digergiderler = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Kalan = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

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

class Kur(models.Model):
    tarih = models.DateField(unique=True)
    dovizalis = models.DecimalField(max_digits=10, decimal_places=4)

    class Meta:
        ordering = ['-tarih',]

    def __str__(self):
        return str(self.tarih)
