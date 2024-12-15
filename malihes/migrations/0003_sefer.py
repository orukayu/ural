# Generated by Django 5.1.4 on 2024-12-15 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('malihes', '0002_kasa'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sefer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Plaka', models.CharField(max_length=25)),
                ('Sofor', models.TextField()),
                ('Cikisyeri', models.TextField()),
                ('Cikistarihi', models.DateField()),
                ('Cikiskm', models.DecimalField(decimal_places=0, max_digits=10)),
                ('Varisyeri', models.TextField()),
                ('Varistarihi', models.DateField()),
                ('Variskm', models.DecimalField(decimal_places=0, max_digits=10)),
                ('Not', models.TextField()),
                ('Musteri', models.TextField()),
                ('Yuk', models.TextField()),
                ('Tasimabedeli', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Dovizkuru', models.DecimalField(decimal_places=4, max_digits=10)),
                ('Toplamfiyat', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Istasyon', models.TextField()),
                ('Litre', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Litrefiyati', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Toplamyakit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Digergiderler', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Kalan', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'ordering': ['Plaka'],
            },
        ),
    ]
