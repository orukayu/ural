# Generated by Django 5.1.4 on 2025-01-15 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('malihes', '0009_alter_araclar_options_alter_kasa_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sefer',
            name='Tasimabedeli',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
