# Generated by Django 3.1 on 2020-08-19 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_total_delete'),
    ]

    operations = [
        migrations.RenameField(
            model_name='total',
            old_name='reportUrl',
            new_name='committerUrl',
        ),
    ]