# Generated by Django 2.1.7 on 2019-03-22 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alice', '0015_auto_20190322_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='type',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
