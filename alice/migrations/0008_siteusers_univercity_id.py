# Generated by Django 2.1.7 on 2019-03-22 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alice', '0007_siteusers'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteusers',
            name='univercity_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='alice.Univercity'),
        ),
    ]
