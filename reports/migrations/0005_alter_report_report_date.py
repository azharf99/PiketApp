# Generated by Django 5.1.4 on 2025-01-09 20:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_alter_report_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='report_date',
            field=models.DateField(default=datetime.date(2025, 1, 10), verbose_name='Tanggal'),
        ),
    ]
