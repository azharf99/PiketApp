# Generated by Django 5.1.4 on 2025-01-09 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_alter_report_report_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='report_date',
            field=models.DateField(verbose_name='Tanggal'),
        ),
    ]
