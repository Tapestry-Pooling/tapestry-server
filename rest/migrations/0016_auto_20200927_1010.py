# Generated by Django 3.0.8 on 2020-09-27 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0015_auto_20200907_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='status',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='rest.Status'),
        ),
    ]
