# Generated by Django 5.1.4 on 2025-01-06 18:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('classes', '0001_initial'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_day', models.CharField(blank=True, choices=[(0, 'Senin'), (1, 'Selasa'), (2, 'Rabu'), (3, 'Kamis'), (4, 'Jumat'), (5, 'Sabtu'), (6, 'Ahad')], max_length=10, verbose_name='Hari')),
                ('schedule_time', models.CharField(choices=[(1, 'Jam ke-1'), (2, 'Jam ke-2'), (3, 'Jam ke-3'), (4, 'Jam ke-4'), (5, 'Jam ke-5'), (6, 'Jam ke-6'), (7, 'Jam ke-7'), (8, 'Jam ke-8'), (9, 'Jam ke-9')], max_length=20, verbose_name='Waktu')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('schedule_class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='classes.class', verbose_name='Kelas')),
                ('schedule_course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.course', verbose_name='Pelajaran')),
            ],
            options={
                'verbose_name': 'Schedule',
                'verbose_name_plural': 'Schedules',
                'db_table': 'schedules',
                'ordering': ['schedule_day'],
                'indexes': [models.Index(fields=['schedule_day'], name='schedules_schedul_045f34_idx')],
            },
        ),
    ]
