# Generated by Django 3.0.8 on 2020-07-30 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0004_city_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='prevalence',
            field=models.FloatField(default=7),
            preserve_default=False,
        ),
    ]