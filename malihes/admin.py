from django.contrib import admin
from .models import Soforler
from .models import Kasa
from .models import Sefer
from .models import Araclar
from .models import Kur

class KasaAdmin(admin.ModelAdmin):
    list_display = ('id', 'Tarih', 'Plaka', 'Fisno', 'Sofor', 'Aciklama1', 'Aciklama2', 'Giris', 'Cikis')

class SeferAdmin(admin.ModelAdmin):
    list_display = ('id', 'Cikistarihi', 'Cikisyeri', 'Varistarihi', 'Varisyeri', 'Plakacekici', 'Plakadorse', 'Sofor', 'Musteri', 'Yuk', 'Toplamfiyat', 'Istasyon', 'Litre', 'Litrefiyati', 'Toplamyakit', 'Digergiderler', 'Kalan')

class AraclarAdmin(admin.ModelAdmin):
    list_display = ('id', 'Plaka', 'Firma', 'Tür', 'Marka', 'Model', 'Sigbastarihi', 'Sigbittarihi', 'Sigtutari', 'Kasbastarihi', 'Kasbittarihi', 'Kastutari', 'Toplamtutar', 'Ayliktutar')

class KurAdmin(admin.ModelAdmin):
    list_display = ('id', 'tarih', 'dovizalis')

admin.site.register(Soforler)
admin.site.register(Kasa,KasaAdmin)
admin.site.register(Sefer,SeferAdmin)
admin.site.register(Araclar,AraclarAdmin)
admin.site.register(Kur,KurAdmin)