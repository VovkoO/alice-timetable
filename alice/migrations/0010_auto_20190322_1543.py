# Generated by Django 2.1.7 on 2019-03-22 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alice', '0009_auto_20190322_1532'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aliceusers',
            old_name='university_id',
            new_name='univerсity_id',
        ),
        migrations.RenameField(
            model_name='group',
            old_name='university_id',
            new_name='univerсity_id',
        ),
        migrations.RenameField(
            model_name='siteusers',
            old_name='university_id',
            new_name='univerсity_id',
        ),
    ]
