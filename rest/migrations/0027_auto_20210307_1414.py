# Generated by Django 3.0.8 on 2021-03-07 08:44

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0026_auto_20210307_0253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='genes',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]