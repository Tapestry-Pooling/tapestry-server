# Generated by Django 3.0.8 on 2020-09-03 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0013_auto_20200824_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='report_filename',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='test',
            name='testctresults_filename',
            field=models.TextField(blank=True, unique=True),
        ),
    ]
