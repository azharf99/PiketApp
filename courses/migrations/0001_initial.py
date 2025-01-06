# Generated by Django 5.1.4 on 2025-01-06 18:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=50, verbose_name='Nama Pelajaran')),
                ('course_code', models.CharField(max_length=20, verbose_name='Kode Pelajaran')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Guru')),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
                'db_table': 'courses',
                'ordering': ['course_name'],
                'indexes': [models.Index(fields=['id', 'course_name'], name='courses_id_ce70a8_idx')],
            },
        ),
    ]