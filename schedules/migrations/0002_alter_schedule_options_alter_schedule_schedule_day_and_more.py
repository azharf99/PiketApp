# Generated by Django 5.1.4 on 2025-01-08 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='schedule',
            options={'ordering': ['-schedule_day', 'schedule_class'], 'verbose_name': 'Schedule', 'verbose_name_plural': 'Schedules'},
        ),
        migrations.AlterField(
            model_name='schedule',
            name='schedule_day',
            field=models.CharField(blank=True, choices=[('0', 'Senin'), ('1', 'Selasa'), ('2', 'Rabu'), ('3', 'Kamis'), ('4', 'Jumat'), ('5', 'Sabtu'), ('6', 'Ahad')], max_length=10, verbose_name='Hari'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='schedule_time',
            field=models.CharField(choices=[('1', 'Jam ke-1'), ('2', 'Jam ke-2'), ('3', 'Jam ke-3'), ('4', 'Jam ke-4'), ('5', 'Jam ke-5'), ('6', 'Jam ke-6'), ('7', 'Jam ke-7'), ('8', 'Jam ke-8'), ('9', 'Jam ke-9')], max_length=20, verbose_name='Waktu'),
        ),
    ]