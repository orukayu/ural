from django.contrib import admin
from .models import Soforler
from .models import Kasa
from .models import Sefer

class KasaAdmin(admin.ModelAdmin):
    list_display = ('id', 'Tarih', 'Plaka', 'Fisno', 'Sofor', 'Aciklama1', 'Aciklama2', 'Giris', 'Cikis')

class SeferAdmin(admin.ModelAdmin):
    list_display = ('id', 'Cikistarihi', 'Cikisyeri', 'Varistarihi', 'Varisyeri', 'Plakacekici', 'Plakadorse', 'Sofor', 'Musteri', 'Yuk', 'Toplamfiyat', 'Istasyon', 'Litre', 'Litrefiyati', 'Toplamyakit', 'Digergiderler', 'Kalan')

admin.site.register(Soforler)
admin.site.register(Kasa,KasaAdmin)
admin.site.register(Sefer,SeferAdmin)
