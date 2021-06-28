# Generated by Django 3.1.3 on 2020-11-21 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('mail', models.EmailField(max_length=254)),
                ('text', models.TextField()),
                ('time_posted', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'message',
                'verbose_name_plural': 'messages',
                'ordering': ('time_posted',),
            },
        ),
    ]