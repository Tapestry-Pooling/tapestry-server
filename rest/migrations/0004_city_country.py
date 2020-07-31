# Generated by Django 3.0.8 on 2020-07-30 05:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0003_auto_20200729_1459'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('calling_codes', models.CharField(blank=True, max_length=5, null=True, verbose_name='calling_codes')),
                ('alpha_2_code', models.CharField(blank=True, max_length=2, verbose_name='alpha_2_code')),
                ('alpha_3_code', models.CharField(blank=True, max_length=3, verbose_name='alpha_3_code')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest.Country')),
            ],
        ),
    ]