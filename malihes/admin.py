from django.contrib import admin
from .models import Soforler
from .models import Kasa

class KasaAdmin(admin.ModelAdmin):
    list_display = ('id', 'Tarih', 'Plaka', 'Fisno', 'Sofor', 'Aciklama1', 'Aciklama2', 'Giris', 'Cikis')

admin.site.register(Soforler)
admin.site.register(Kasa,KasaAdmin)
