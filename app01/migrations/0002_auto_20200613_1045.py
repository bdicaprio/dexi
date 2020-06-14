# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statistics',
            name='corporateGender',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='education',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
