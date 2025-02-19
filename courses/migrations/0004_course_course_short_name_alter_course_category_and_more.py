# Generated by Django 5.1.4 on 2025-01-11 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_alter_course_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_short_name',
            field=models.CharField(default='', max_length=30, verbose_name='Nama Singkat'),
        ),
        migrations.AlterField(
            model_name='course',
            name='category',
            field=models.CharField(choices=[(None, '----Pilih Kategori----'), ("Syar'i", "Syar'i"), ('Ashri', 'Ashri')], default="Syar'i", max_length=20, verbose_name='Kategori'),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_code',
            field=models.CharField(blank=True, max_length=20, verbose_name='Kode Pelajaran'),
        ),
    ]
