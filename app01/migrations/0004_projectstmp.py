# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_auto_20200615_2254'),
    ]

    operations = [
        migrations.CreateModel(
            name='projectstmp',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('projectName', models.CharField(max_length=64, blank=True, null=True)),
                ('projectFrom', models.CharField(max_length=64, blank=True, null=True)),
                ('developmentForm', models.CharField(max_length=64, blank=True, null=True)),
                ('achievement', models.CharField(max_length=64, blank=True, null=True)),
                ('economicGoals', models.CharField(max_length=64, blank=True, null=True)),
                ('activityType', models.CharField(max_length=64, blank=True, null=True)),
                ('startTime', models.DateTimeField(blank=True, null=True)),
                ('endTime', models.DateTimeField(blank=True, null=True)),
                ('personnel', models.CharField(max_length=64, blank=True, null=True)),
                ('time', models.CharField(max_length=64, blank=True, null=True)),
                ('stage', models.CharField(max_length=64, blank=True, null=True)),
                ('funds', models.IntegerField(blank=True, null=True)),
                ('capital', models.IntegerField(blank=True, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, to='app01.companyInfo')),
            ],
        ),
    ]
