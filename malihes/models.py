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
