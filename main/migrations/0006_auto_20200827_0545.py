# Generated by Django 3.1 on 2020-08-27 02:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20200827_0537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='Date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 27, 5, 45, 15, 335213)),
        ),
        migrations.AlterField(
            model_name='user',
            name='img',
            field=models.ImageField(default='default.png', upload_to='media'),
        ),
    ]
