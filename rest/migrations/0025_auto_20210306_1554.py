# Generated by Django 3.0.8 on 2021-03-06 10:24

import django.contrib.postgres.fields
from django.db import migrations, models
import rest.models.test


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0024_test_genes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='genes',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=10), default=rest.models.test.get_genes_default, size=6),
        ),
    ]
