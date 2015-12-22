from corehq.apps.sms.models import MigrationStatus
from django.conf import settings
from django.template import Context, Template
import os


EXCEPTION_MESSAGE = Template("""
Halting migrate command because one or more messaging migrations have not
yet completed.

In order to continue, switch into your code root (and virtual environment if
you have one), and do the following:

git fetch origin
git checkout -b {{ tag_name }}-tmp {{ tag_name }}
git submodule update --init --recursive
find . -name "*.pyc" -delete
{% for command in commands %}python manage.py {{ command }}
{% endfor %}

You can then checkout the branch you were previously on (master, presumably),
update submodules, clean *.pyc files, and run python manage.py migrate normally.

NOTE: If you are seeing this on a fresh install of CommCareHQ, then you can
ignore the above. Instead, the first time you run migrate, run it with the
following command:
    env CCHQ_IS_FRESH_INSTALL=1 python manage.py migrate
""")


class MigrationInfo(object):
    def __init__(self, migration_names, tag_name, commands):
        """
        migration_names - A list of MigrationStatus.MIGRATION_* constants
                          that will be checked. If any of those migrations
                          have not run then a MigrationException with the
                          EXCEPTION_MESSAGE will be raised.
        tag_name - The name of the git tag which should be checked out to
                   run the management commands.
        commands - The list of management commands that need to be run in order
                   to complete the migrations referenced by migration_names.
        """
        self.migration_names = migration_names
        self.context = Context({
            'tag_name': tag_name,
            'commands': commands,
        })


class MigrationException(Exception):
    pass


def assert_messaging_migration_complete(info, model_class=MigrationStatus):
    migrations_have_not_run = any(
        [not model_class.has_migration_completed(name) for name in info.migration_names]
    )
    is_fresh_install = os.environ.get('CCHQ_IS_FRESH_INSTALL') == '1'
    if migrations_have_not_run and not (settings.UNIT_TESTING or is_fresh_install):
        raise MigrationException(EXCEPTION_MESSAGE.render(info.context))


def assert_backend_migration_complete(apps, schema_editor):
    assert_messaging_migration_complete(
        MigrationInfo(
            [MigrationStatus.MIGRATION_BACKEND, MigrationStatus.MIGRATION_BACKEND_MAP],
            'backend-messaging-migration',
            ['migrate_backends_to_sql', 'migrate_backend_mappings_to_sql']
        ),
        model_class=apps.get_model('sms', 'MigrationStatus')
    )
