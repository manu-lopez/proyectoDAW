# Generated by Django 3.0.5 on 2020-06-07 08:20

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('blr', '0006_auto_20200603_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='resource_tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
