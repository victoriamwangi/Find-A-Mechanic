# Generated by Django 4.0.5 on 2022-06-23 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('amechanic', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='name',
            new_name='location_name',
        ),
    ]
