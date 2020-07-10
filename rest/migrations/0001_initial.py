# Generated by Django 3.0.8 on 2020-07-08 06:25

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Lab Name')),
                ('city', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='LabMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('designation', models.CharField(choices=[('LMN', 'Lab Manager'), ('LMB', 'Lab Member')], max_length=3)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('email', models.EmailField(max_length=254)),
                ('lab_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest.Lab')),
            ],
        ),
        migrations.CreateModel(
            name='MachineType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='PCR machine', max_length=60)),
                ('no_of_wells', models.SmallIntegerField()),
                ('plate_x', models.SmallIntegerField(default=12)),
                ('plate_y', models.SmallIntegerField(default=8)),
            ],
        ),
        migrations.CreateModel(
            name='TestKit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='LabConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lab_id', models.SmallIntegerField()),
                ('machine_type', models.ManyToManyField(to='rest.MachineType')),
                ('test_kit', models.ManyToManyField(to='rest.TestKit')),
            ],
        ),
    ]
