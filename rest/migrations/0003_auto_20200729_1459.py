# Generated by Django 3.0.8 on 2020-07-29 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0002_auto_20200716_2056'),
    ]

    operations = [
        migrations.AddField(
            model_name='machinetype',
            name='capacity',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='machinetype',
            name='machine_maker',
            field=models.CharField(default='', max_length=50),
        ),
    ]
