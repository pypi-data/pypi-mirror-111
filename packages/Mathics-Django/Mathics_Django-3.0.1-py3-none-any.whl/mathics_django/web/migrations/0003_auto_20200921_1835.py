# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-09-21 18:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0002_auto_20200917_2354"),
    ]

    operations = [
        migrations.AlterField(
            model_name="worksheet",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="worksheets",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
