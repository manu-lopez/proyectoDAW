# Generated by Django 3.0.5 on 2020-06-15 00:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blr', '0006_remove_profile_resources'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='post_author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
