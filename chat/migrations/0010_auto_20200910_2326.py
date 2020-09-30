# Generated by Django 3.1 on 2020-09-10 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_widget_form_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='widget_form',
            name='instructor_approved',
        ),
        migrations.RemoveField(
            model_name='widget_form',
            name='instructor_ask_to_resubmit',
        ),
        migrations.RemoveField(
            model_name='widget_form',
            name='student_approved',
        ),
        migrations.RemoveField(
            model_name='widget_form',
            name='student_ask_to_resubmit',
        ),
        migrations.AlterField(
            model_name='widget_form',
            name='status',
            field=models.CharField(default='Pending', max_length=40),
        ),
    ]
