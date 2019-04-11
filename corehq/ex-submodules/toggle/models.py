from __future__ import absolute_import
from __future__ import unicode_literals
from datetime import datetime

from couchdbkit import ResourceNotFound
from django.db import models

from corehq.apps.couch_sql_migration.fields import DocumentField
from corehq.apps.couch_sql_migration.utils import sql_save_with_resource_conflict
from corehq.util.quickcache import quickcache
from dimagi.ext.couchdbkit import (
    Document, DateTimeProperty, ListProperty, StringProperty
)


TOGGLE_ID_PREFIX = 'hqFeatureToggle'


class Toggle(Document):
    """
    A very simple implementation of a feature toggle. Just a list of items
    attached to a slug.
    """
    slug = StringProperty()
    enabled_users = ListProperty()
    last_modified = DateTimeProperty()

    def save(self, **params):
        if ('_id' not in self._doc):
            self._doc['_id'] = generate_toggle_id(self.slug)
        self.last_modified = datetime.utcnow()
        old_doc_rev = self._rev
        super(Toggle, self).save(**params)
        sql_save_with_resource_conflict(SqlToggle, self, old_doc_rev)

        self.bust_cache()

    @classmethod
    @quickcache(['cls.__name__', 'docid'], timeout=60 * 60 * 24)
    def cached_get(cls, docid):
        try:
            return cls.get(docid)
        except ResourceNotFound:
            return None

    @classmethod
    def get(cls, docid):
        if not docid.startswith(TOGGLE_ID_PREFIX):
            docid = generate_toggle_id(docid)
        return super(Toggle, cls).get(docid, rev=None, db=None, dynamic_properties=True)

    def add(self, item):
        """
        Adds an item to the toggle. Only saves if necessary.
        """
        if item not in self.enabled_users:
            self.enabled_users.append(item)
            self.save()

    def remove(self, item):
        """
        Removes an item from the toggle. Only saves if necessary.
        """
        if item in self.enabled_users:
            self.enabled_users.remove(item)
            self.save()

    def delete(self):
        SqlToggle.objects.filter(id=self._doc['_id']).delete()
        super(Toggle, self).delete()
        self.bust_cache()

    def bust_cache(self):
        self.cached_get.clear(self.__class__, self.slug)


def generate_toggle_id(slug):
    # use the slug to build the ID to avoid needing couch views
    # and to make looking up in futon easier
    return '{prefix}-{slug}'.format(prefix=TOGGLE_ID_PREFIX, slug=slug)


class SqlToggle(models.Model):
    id = models.CharField(max_length=126, primary_key=True)
    rev = models.CharField(max_length=126)
    document = DocumentField(document_class=Toggle)
