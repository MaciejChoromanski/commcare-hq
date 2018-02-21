# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-01 15:00
from __future__ import unicode_literals

from django.db import migrations, models

from corehq.apps.app_manager.dbaccessors import get_app
from corehq.apps.app_manager.models import LinkedApplication
from corehq.apps.linked_domain.exceptions import DomainLinkError
from corehq.apps.linked_domain.models import RemoteLinkDetails, DomainLink
from corehq.dbaccessors.couchapps.all_docs import get_all_docs_with_doc_types
from corehq.util.soft_assert import soft_assert


def _migrate_linked_apps(apps, schema_editor):
    app_db = LinkedApplication.get_db()
    linked_apps = get_all_docs_with_doc_types(
        app_db, ['LinkedApplication', 'LinkedApplication-Deleted']
    )
    errors = []
    for app_doc in linked_apps:
        remote_details = None
        remote_url = app_doc.pop('remote_url_base', None)
        if remote_url:
            auth = app_doc.pop('remote_auth', {})
            remote_details = RemoteLinkDetails(
                remote_url,
                auth.get('username'),
                auth.get('api_key'),
            )

        master_domain = app_doc.pop('master_domain', None)
        if not master_domain and not remote_url:
            master_domain = get_app(None, app_doc['master']).domain
        try:
            DomainLink.link_domains(app_doc['domain'], master_domain, remote_details)
        except DomainLinkError as e:
            errors.append(str(e))
        else:
            app_db.save_doc(app_doc)

    _assert = soft_assert('{}@dimagi.com'.format('skelly'), exponential_backoff=False)
    _assert(not errors, 'Errors migrating linked apps to linked domain', {
        'errors': errors
    })


def noop(*args, **kwargs):
    pass


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('linked_domain', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domainlink',
            name='last_pull',
            field=models.DateTimeField(null=True),
        ),
        migrations.RunPython(_migrate_linked_apps, noop)
    ]
