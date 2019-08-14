from sqlagg.columns import SimpleColumn

from corehq.apps.locations.models import SQLLocation, LocationType
from corehq.apps.reports.sqlreport import SqlData, DatabaseColumn
from corehq.apps.userreports.util import get_table_name
from django.core.exceptions import ObjectDoesNotExist

from django.core.management.base import BaseCommand


class ChampFilter(SqlData):

    domain = 'test-pna'
    table = 'yeksi_naa_reports_consumption'
    column_names = [
        'region_id',
        'region_name',
        'district_id',
        'district_name',
        'pps_id',
        'pps_name',
    ]

    def __init__(self):
        config = {
            'domain': self.domain,
        }
        super(ChampFilter, self).__init__(config)

    @property
    def table_name(self):
        return get_table_name(self.domain, self.table)

    @property
    def group_by(self):
        return self.column_names

    @property
    def filters(self):
        return []

    @property
    def engine_id(self):
        return 'ucr'

    @property
    def columns(self):
        return [
            DatabaseColumn(column, SimpleColumn(column)) for column in self.column_names
        ]

    @property
    def data(self):
        return self.get_data()


def _create_type(name):
    try:
        LocationType.objects.create(name=name, domain='test-pna')
        print('Created location type \'{}\''.format(name))
    except Exception as err:
        print('Unhandled error: {}'.format(err.message))


def _get_parent(parent_id):
    parent = None
    try:
        parent = SQLLocation.objects.get(location_id__exact=parent_id)
    except ObjectDoesNotExist:
        if parent_id is not None:
            print('Parent with ID \'{}\' was not found'.format(parent_id))
    parent_id = parent.id if parent is not None else None

    return parent_id


def _get_dictionary(args):
    locations_data = {
        'domain': 'test-pna',
        'name': args[0],
        'location_id': args[1],
        'location_type_id': args[2],
        'site_code': args[3],
        'parent_id': args[4],
    }

    return locations_data


def _create_record(location):
    try:
        SQLLocation.objects.create(domain=location['domain'], name=location['name'],
                                   location_id=location['location_id'], parent_id=location['parent_id'],
                                   location_type_id=location['location_type_id'], site_code=location['site_code'],)
        if location['location_id'] is not None:
            print('Created location \'{}\' with ID \'{}\''.format(location['name'], location['location_id']))
    except KeyError:
        print('Location \'{}\' with ID \'{}\' already exists'.format(location['name'], location['location_id']))
    except Exception as err:
        print('Unhandled error: {}'.format(err))


class Command(BaseCommand):

    help = 'Adds locations type and locations needed for IPM based on operateur_combined table'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print('Creating location types...')
        region_type_exists = LocationType.objects.filter(name='region', domain='test-pna').exists()
        district_type_exists = LocationType.objects.filter(name='region', domain='test-pna').exists()
        pps_type_exists = LocationType.objects.filter(name='region', domain='test-pna').exists()

        if region_type_exists:
            print('Type \'region\' for domain \'test-pna\' already exists')
        else:
            _create_type('region')

        if district_type_exists:
            print('Type \'district\' for domain \'test-pna\' already exists')
        else:
            _create_type('district')

        if pps_type_exists:
            print('Type \'pps\' for domain \'test-pna\' already exists')
        else:
            _create_type('pps')

        region_type_id = LocationType.objects.get(name='region', domain='test-pna').id
        district_type_id = LocationType.objects.get(name='district', domain='test-pna').id
        pps_type_id = LocationType.objects.get(name='pps', domain='test-pna').id
        rows = ChampFilter().data
        site_code = 0

        print('Creating locations...')
        for row in rows:
            pps_id = row['pps_id']
            pps_name = row['pps_name']
            pps_exists = SQLLocation.objects.filter(location_id__exact=pps_id).exists()

            if not pps_exists:
                district_id = row['district_id']
                district_name = row['district_name']
                district_exists = SQLLocation.objects.filter(location_id__exact=district_id).exists()

                if not district_exists:
                    region_id = row['region_id']
                    region_name = row['region_name']
                    region_exists = SQLLocation.objects.filter(location_id__exact=region_id).exists()

                    if not region_exists:
                        parent_id = None
                        args = [region_name, region_id, region_type_id, site_code, parent_id]
                        locations_data = _get_dictionary(args)
                        _create_record(locations_data)
                        site_code += 1

                    parent_id = _get_parent(region_id)
                    args = [district_name, district_id, district_type_id, site_code, parent_id]
                    locations_data = _get_dictionary(args)
                    _create_record(locations_data)
                    site_code += 1

                parent_id = _get_parent(district_id)
                args = [pps_name, pps_id, pps_type_id, site_code, parent_id]
                locations_data = _get_dictionary(args)
                _create_record(locations_data)
                site_code += 1

        print('Created {} locations'.format(site_code))
