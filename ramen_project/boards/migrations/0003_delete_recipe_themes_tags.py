# Generated by Django 4.1 on 2024-01-03 05:47

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        ('boards', '0002_recipe'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Recipe',
        ),
        migrations.AddField(
            model_name='themes',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]