# Generated by Django 3.1 on 2020-08-26 23:08

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200823_2322'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='instructor',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.instructor'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='student',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.student'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='Date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 27, 2, 8, 9, 991117)),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
