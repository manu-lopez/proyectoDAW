# Generated by Django 3.0.5 on 2020-06-14 23:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blr', '0003_auto_20200615_0120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='resources',
        ),
    ]
