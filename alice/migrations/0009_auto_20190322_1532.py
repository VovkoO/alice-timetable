# Generated by Django 2.1.7 on 2019-03-22 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alice', '0008_siteusers_univercity_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aliceusers',
            old_name='univercity_id',
            new_name='university_id',
        ),
        migrations.RenameField(
            model_name='group',
            old_name='univercity_id',
            new_name='university_id',
        ),
        migrations.RenameField(
            model_name='siteusers',
            old_name='univercity_id',
            new_name='university_id',
        ),
    ]