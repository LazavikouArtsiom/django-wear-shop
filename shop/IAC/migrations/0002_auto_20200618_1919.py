# Generated by Django 3.0.7 on 2020-06-18 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IAC', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'ordering': ('time_posted',), 'verbose_name': 'message', 'verbose_name_plural': 'messages'},
        ),
    ]
