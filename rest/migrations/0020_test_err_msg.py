# Generated by Django 3.0.8 on 2020-10-03 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0019_auto_20201002_0715'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='err_msg',
            field=models.CharField(blank=True, default='none', max_length=255),
        ),
    ]
