# Generated by Django 3.1 on 2020-09-05 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_widget_form_approved_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=40)),
                ('approved', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='widget_form',
            name='instructor_approved',
        ),
        migrations.RemoveField(
            model_name='widget_form',
            name='option1',
        ),
        migrations.RemoveField(
            model_name='widget_form',
            name='option2',
        ),
        migrations.RemoveField(
            model_name='widget_form',
            name='option3',
        ),
    ]
