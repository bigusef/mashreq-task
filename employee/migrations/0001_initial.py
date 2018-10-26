# Generated by Django 2.1.2 on 2018-10-26 14:04

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('middle_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('age', models.IntegerField()),
                ('identifier', models.CharField(max_length=16)),
                ('position', models.CharField(max_length=50)),
                ('birth_date', models.DateField()),
                ('birth_place', models.CharField(max_length=100)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('nationality', django_countries.fields.CountryField(max_length=2)),
                ('marital_status', models.CharField(choices=[('m', 'Married'), ('w', 'Widowed'), ('p', 'Separated'), ('d', 'Divorced'), ('s', 'Single')], max_length=1)),
                ('gender', models.CharField(choices=[('m', 'Male'), ('f', 'Female')], max_length=1)),
            ],
        ),
    ]
