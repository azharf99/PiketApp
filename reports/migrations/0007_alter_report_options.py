# Generated by Django 5.1.4 on 2025-01-10 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0006_alter_report_report_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ['-report_date', 'schedule__schedule_class', 'schedule__schedule_time'], 'verbose_name': 'Report', 'verbose_name_plural': 'Reports'},
        ),
    ]
