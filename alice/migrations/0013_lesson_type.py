# Generated by Django 2.1.7 on 2019-03-22 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alice', '0012_lesson_repeat'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='type',
            field=models.CharField(default='fs', max_length=10),
            preserve_default=False,
        ),
    ]
