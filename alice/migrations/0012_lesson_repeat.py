# Generated by Django 2.1.7 on 2019-03-22 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alice', '0011_lesson_day_of_week'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='repeat',
            field=models.IntegerField(default=1),
        ),
    ]