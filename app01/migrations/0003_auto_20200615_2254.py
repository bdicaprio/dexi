# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20200613_1045'),
    ]

    operations = [
        migrations.CreateModel(
            name='companyInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('companyname', models.CharField(max_length=64, blank=True, null=True)),
                ('username', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='activities',
            name='username',
        ),
        migrations.RemoveField(
            model_name='company',
            name='username',
        ),
        migrations.RemoveField(
            model_name='economic',
            name='username',
        ),
        migrations.RemoveField(
            model_name='personnel',
            name='username',
        ),
        migrations.RemoveField(
            model_name='projects',
            name='username',
        ),
        migrations.RemoveField(
            model_name='statistics',
            name='username',
        ),
        migrations.AddField(
            model_name='activities',
            name='company',
            field=models.ForeignKey(blank=True, null=True, to='app01.companyInfo'),
        ),
        migrations.AddField(
            model_name='company',
            name='company',
            field=models.ForeignKey(blank=True, null=True, to='app01.companyInfo'),
        ),
        migrations.AddField(
            model_name='economic',
            name='company',
            field=models.ForeignKey(blank=True, null=True, to='app01.companyInfo'),
        ),
        migrations.AddField(
            model_name='personnel',
            name='company',
            field=models.ForeignKey(blank=True, null=True, to='app01.companyInfo'),
        ),
        migrations.AddField(
            model_name='projects',
            name='company',
            field=models.ForeignKey(blank=True, null=True, to='app01.companyInfo'),
        ),
        migrations.AddField(
            model_name='statistics',
            name='company',
            field=models.ForeignKey(blank=True, null=True, to='app01.companyInfo'),
        ),
    ]
