# Generated by Django 5.0.1 on 2024-02-04 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_users_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='picture',
            field=models.FileField(blank=True, null=True, upload_to='picture/'),
        ),
    ]