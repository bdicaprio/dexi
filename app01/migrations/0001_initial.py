# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='companyProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, blank=True, null=True)),
                ('code', models.CharField(max_length=16, blank=True, null=True)),
                ('content', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='economicOverview',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, blank=True, null=True)),
                ('unit', models.CharField(max_length=8, blank=True, null=True)),
                ('code', models.CharField(max_length=16, blank=True, null=True)),
                ('number', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='enterpriseStatistics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('organizationCode', models.CharField(max_length=16, blank=True, null=True)),
                ('areaNumber', models.CharField(max_length=16, blank=True, null=True)),
                ('enterpriseName', models.CharField(max_length=16, blank=True, null=True)),
                ('natureOfCorporation', models.CharField(max_length=16, blank=True, null=True)),
                ('corporateGender', models.BooleanField()),
                ('birthday', models.DateTimeField(blank=True, null=True)),
                ('education', models.BooleanField()),
                ('address', models.CharField(max_length=64, blank=True, null=True)),
                ('postalCode', models.IntegerField(blank=True, null=True)),
                ('registeredAddress', models.CharField(max_length=64, blank=True, null=True)),
                ('manager', models.CharField(max_length=16, blank=True, null=True)),
                ('telephone', models.IntegerField(blank=True, null=True)),
                ('fax', models.IntegerField(blank=True, null=True)),
                ('statisticalControlOfficer', models.CharField(max_length=16, blank=True, null=True)),
                ('preparedBy', models.CharField(max_length=16, blank=True, null=True)),
                ('preparedByTelephone', models.CharField(max_length=16, blank=True, null=True)),
                ('fillingTime', models.DateTimeField(blank=True, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('url', models.CharField(max_length=16, blank=True, null=True)),
                ('preparedByMobilephone', models.CharField(max_length=16, blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='personnelProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, blank=True, null=True)),
                ('unit', models.CharField(max_length=8, blank=True, null=True)),
                ('code', models.CharField(max_length=16, blank=True, null=True)),
                ('number', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='technologicalActivities',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, blank=True, null=True)),
                ('unit', models.CharField(max_length=8, blank=True, null=True)),
                ('code', models.CharField(max_length=16, blank=True, null=True)),
                ('number', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='technologyProjects',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('projectName', models.CharField(max_length=64, blank=True, null=True)),
                ('projectFrom', models.CharField(max_length=64, blank=True, null=True)),
                ('DevelopmentForm', models.CharField(max_length=64, blank=True, null=True)),
                ('AchievementDisplay', models.CharField(max_length=64, blank=True, null=True)),
                ('EconomicGoals', models.CharField(max_length=64, blank=True, null=True)),
                ('activityType', models.CharField(max_length=64, blank=True, null=True)),
                ('startTime', models.DateTimeField(blank=True, null=True)),
                ('endTime', models.DateTimeField(blank=True, null=True)),
                ('personnel', models.CharField(max_length=64, blank=True, null=True)),
                ('time', models.CharField(max_length=64, blank=True, null=True)),
                ('stage', models.CharField(max_length=64, blank=True, null=True)),
                ('funds', models.IntegerField(blank=True, null=True)),
                ('capital', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('account', models.CharField(max_length=16, blank=True, null=True)),
                ('password', models.CharField(max_length=16, blank=True, null=True)),
                ('name', models.CharField(max_length=16, blank=True, null=True)),
                ('nickname', models.CharField(max_length=16, blank=True, null=True)),
                ('sex', models.BooleanField()),
                ('telephone', models.IntegerField(blank=True, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('company', models.CharField(max_length=16, blank=True, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
