# Generated by Django 3.0.8 on 2020-08-24 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0012_auto_20200824_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='labconfiguration',
            name='max_poolsize',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='test',
            name='max_poolsize',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]
