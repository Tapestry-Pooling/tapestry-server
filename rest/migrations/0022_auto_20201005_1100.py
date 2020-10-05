# Generated by Django 3.0.8 on 2020-10-05 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0021_auto_20201003_0816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labconfiguration',
            name='machine_type',
            field=models.ManyToManyField(default=[0], to='rest.MachineType'),
        ),
        migrations.AlterField(
            model_name='labconfiguration',
            name='test_kit',
            field=models.ManyToManyField(default=[0], to='rest.TestKit'),
        ),
    ]
