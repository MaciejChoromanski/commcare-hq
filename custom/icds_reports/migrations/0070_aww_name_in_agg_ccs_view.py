# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-11 14:13
from __future__ import unicode_literals
from __future__ import absolute_import

from django.db import migrations

from custom.icds_reports.utils.migrations import get_view_migrations


class Migration(migrations.Migration):

    dependencies = [
        ('icds_reports', '0069_valid_visits'),
    ]

    operations = [
    ]
    operations.extend(get_view_migrations())
