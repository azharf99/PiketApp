# Generated by Django 5.1.4 on 2025-01-09 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0003_class_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='category',
            field=models.CharField(choices=[(None, '----Pilih Kategori Kelas----'), ('Putra', 'Putra'), ('Putri', 'Putri')], default='Putra', max_length=20, verbose_name='Kode Pelajaran'),
        ),
    ]
