# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='economic',
            name='QC226',
            field=models.CharField(max_length=64, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='economic',
            name='QC226_1',
            field=models.CharField(max_length=64, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='economic',
            name='QC226_2',
            field=models.CharField(max_length=64, blank=True, null=True),
        ),
    ]
