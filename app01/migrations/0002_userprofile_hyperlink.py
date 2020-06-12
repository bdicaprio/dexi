# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='hyperlink',
            field=models.CharField(max_length=16, blank=True, null=True, default='点击查看详细信息'),
        ),
    ]
