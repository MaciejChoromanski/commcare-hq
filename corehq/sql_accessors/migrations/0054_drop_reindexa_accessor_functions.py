# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-06 21:18
from __future__ import unicode_literals

from __future__ import absolute_import
from django.db import migrations




class Migration(migrations.Migration):

    dependencies = [
        ('sql_accessors', '0053_drop_unused_sql'),
    ]

    operations = [
        migrations.RunSQL("DROP FUNCTION IF EXISTS get_all_cases_modified_since(timestamp with time zone, INTEGER, INTEGER)"),
        migrations.RunSQL("DROP FUNCTION IF EXISTS get_all_forms_received_since(timestamp with time zone, INTEGER, INTEGER)"),
        migrations.RunSQL("DROP FUNCTION IF EXISTS get_all_ledger_values_modified_since(timestamp with time zone, INTEGER, INTEGER)"),
    ]
