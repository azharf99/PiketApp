# Generated by Django 5.1.4 on 2025-01-08 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='class_name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Nama Kelas'),
        ),
    ]