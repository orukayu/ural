# Generated by Django 5.1.4 on 2025-01-01 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('malihes', '0006_araclar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='araclar',
            name='Kasbastarihi',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='araclar',
            name='Kasbittarihi',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='araclar',
            name='Sigbastarihi',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='araclar',
            name='Sigbittarihi',
            field=models.DateField(blank=True, null=True),
        ),
    ]