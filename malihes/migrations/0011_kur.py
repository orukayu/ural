# Generated by Django 5.1.4 on 2025-01-17 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('malihes', '0010_alter_sefer_tasimabedeli'),
    ]

    operations = [
        migrations.CreateModel(
            name='Kur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tarih', models.DateField(unique=True)),
                ('dovizalis', models.DecimalField(decimal_places=4, max_digits=10)),
            ],
        ),
    ]
