from datetime import datetime

from memoized import memoized
from sqlagg.columns import SimpleColumn
from sqlagg.filters import EQ, GTE, LTE

from corehq.apps.reports.datatables import DataTablesColumn
from corehq.apps.reports.sqlreport import DatabaseColumn
from custom.inddex.couchdata import CouchData
from custom.inddex.sqldata import FoodConsumptionDataSourceMixin


class GapsReportByItemDataMixin(FoodConsumptionDataSourceMixin):
    total_row = None
    title = None
    slug = None
    headers_in_order = []
    _NAMES = {
        'ds': [
            'food_base_term', 'food_code', 'food_name', 'food_type', 'other_tag_1', 'other_tag_2', 'other_tag_3',
            'other_tag_4', 'other_tag_5', 'other_tag_6', 'other_tag_7', 'other_tag_8', 'other_tag_9',
            'other_tag_10', 'tag_1', 'tag_2', 'tag_3', 'tag_4', 'tag_5', 'tag_6', 'tag_7',
            'tag_8', 'tag_9', 'tag_10', 'conv_method', 'conv_option',
        ],
        'not_ds': [
            'fao_who_gift_food_group_code', 'fao_who_gift_food_group_description', 'external_id', 'fct_gap_code',
            'fct_gap_desc', 'conv_factor_gap_code', 'conv_factor_gap_desc', 'report_data_type',
            'conv_factor_food_code', 'conv_factor_parent_food_code',
        ]
    }

    @property
    def couch_db(self):
        return CouchData(domain=self.config['domain'], tables=('conv_factors', 'food_composition_table'))

    @property
    def filters(self):
        filters = [GTE('opened_date', 'startdate'), LTE('opened_date', 'enddate')]
        for slug in ['food_code', 'food_type', 'recall_status']:
            if self.config[slug]:
                filters.append(EQ(slug, slug))

        return filters

    @property
    def additional_filters(self):
        return {}

    @property
    def headers(self):
        raw_headers = {
            'ds': self._NAMES['ds'] + self.additional_headers['ds'],
            'not_ds': self._NAMES['not_ds'] + self.additional_headers['not_ds']
        }

        if not self.headers_in_order:
            return [DataTablesColumn(value) for key, values in raw_headers.items() for value in values]
        else:
            return [DataTablesColumn(header) for header in self.headers_in_order]

    @property
    def additional_headers(self):
        return {'ds': [], 'not_ds': []}

    @property
    def columns(self):
        return [
            DatabaseColumn(self._normalize_text(x), SimpleColumn(x))
            for x in self._NAMES['ds'] + self.additional_columns
        ]

    @property
    def additional_columns(self):
        return ['doc_id', 'reference_food_code']

    @property
    def group_by(self):
        return [x for x in self._NAMES['ds'] + self.additional_columns]

    @property
    def raw_rows(self):
        all_data_raw = self._prepare_raw_data()
        self._append_fao_data(all_data_raw)
        self._append_conv_factor_data(all_data_raw)
        self._append_conv_factor_gap_data(all_data_raw)
        self._append_fct_gap_data(all_data_raw)

        return all_data_raw

    @property
    def default_values(self):
        return {}

    @staticmethod
    def _normalize_text(text):
        return text.replace('_', ' ', text.count('_')).capitalize()

    def _append_fao_data(self, all_rows):
        food_codes = all_rows['food_code']
        parent_food_codes = all_rows['reference_food_code']
        fao_who_gift_food_group = self._get_fao_who_gift_food_group(food_codes, parent_food_codes)
        for x in fao_who_gift_food_group:
            for key in ['fao_who_gift_food_group_code', 'fao_who_gift_food_group_description']:
                all_rows[key].append((x[0], x[1][key]))

    def _get_fao_who_gift_food_group(self, food_codes, parent_food_codes):
        valid_food_codes = tuple(x[1] if x[1] else parent_food_codes[food_codes.index(x)][1] for x in food_codes)
        valid_food_codes = tuple(x for x in valid_food_codes if x)
        positions = set(x[0] for x in food_codes + parent_food_codes if x[1] in valid_food_codes)
        positions_dict = {x: y for x, y in list(zip(positions, valid_food_codes))}
        fao_who_gift_food_group = self.couch_db.as_dict(
            table_name='food_composition_table', values=(('food_code', valid_food_codes),)
        )
        fao_who_gift_food_group_dict = {x[0]: x for x in fao_who_gift_food_group}
        to_return = []

        for position, code in positions_dict.items():
            fao = fao_who_gift_food_group_dict.get(code)
            if fao:
                to_return.append((position, {
                    'food_code': fao[0],
                    'fao_who_gift_food_group_code': fao[1]['fao_who_gift_food_group_code'],
                    'fao_who_gift_food_group_description': fao[1]['fao_who_gift_food_group_description']
                }))

        return tuple(to_return)

    def _prepare_raw_data(self):
        all_data_raw = {}
        raw_data = self.get_data()
        for i, dict_ in enumerate(raw_data):
            for key, value in dict_.items():
                if all_data_raw.get(key):
                    all_data_raw[key].append((i, value))
                else:
                    all_data_raw[key] = [(i, value)]

        for header in self._NAMES['not_ds'] + self.additional_headers['not_ds']:
            all_data_raw[header] = []

        return all_data_raw

    @staticmethod
    def _append_report_data_type(all_rows, report_type):
        for r in range(len(all_rows['food_code'])):
            all_rows['report_data_type'].append((r, report_type))

    def _append_conv_factor_data(self, all_rows):
        keys = {
            1: 'food_code',
            2: 'reference_food_code'
        }
        conv_factor_keys = {
            1: 'conv_factor_food_code',
            2: 'conv_factor_parent_food_code'
        }

        for r in range(1, 3):
            key = keys[r]
            conv_factor_key = conv_factor_keys[r]
            positions = all_rows[key].copy()
            if not all_rows.get('conv_factor'):
                conv_factor = self._get_conv_factor(all_rows)
                all_rows['conv_factor_food_code'] = list(conv_factor)
            else:
                conv_factor = self._get_conv_factor(
                    all_rows, food_codes_used=tuple(x[0] for x in all_rows['conv_factor'])
                )
                all_rows['conv_factor_parent_food_code'] = list(conv_factor)
            data_codes = [x[0] for x in conv_factor]
            for i in range(len(positions)):
                code = positions[i][1]
                if code in data_codes:
                    all_rows[conv_factor_key].append(
                        (positions[i][0], conv_factor[data_codes.index(code)][1]['conv_factor'])
                    )

    def _get_conv_factor(self, raw_rows, food_codes_used=tuple()):
        positions, food_codes, conv_methods, conv_options = self._prepare_data_for_conv_factor_calcs(
            raw_rows, food_codes_used=food_codes_used
        )
        values = (
            ('food_code', food_codes),
            ('conv_method', conv_methods),
            ('conv_option', conv_options)
        )
        conv_factor_food_code = self.couch_db.as_dict(
            table_name='conv_factors', key_field='food_code',
            additional_fields=('conv_method', 'conv_option'),
            values=values
        )
        positions = [x for x in positions if food_codes[positions.index(x)] in [c[0] for c in conv_factor_food_code]]

        return tuple(
            (y, {
                'food_code': x[0],
                'conv_factor': x[1]['conv_factor']
            }) for y, x in list(zip(positions, conv_factor_food_code))
        )

    @staticmethod
    def _prepare_data_for_conv_factor_calcs(raw_rows, food_codes_used):
        if food_codes_used:
            tmp_data = [
                (x[0], x[1], y[1], z[1])
                for x, y, z in
                list(zip(raw_rows['reference_food_code'], raw_rows['conv_method'], raw_rows['conv_option']))
                if (raw_rows['food_type'][raw_rows['reference_food_code'].index(x)][1] == 'food_item' or
                    raw_rows['food_type'][raw_rows['reference_food_code'].index(x)][1] == 'std_recipe') and
                raw_rows['food_code'][raw_rows['reference_food_code'].index(x)][1] not in food_codes_used
            ]
        else:
            tmp_data = [
                (x[0], x[1], y[1], z[1])
                for x, y, z in list(zip(raw_rows['food_code'], raw_rows['conv_method'], raw_rows['conv_option']))
                if raw_rows['food_type'][raw_rows['food_code'].index(x)][1] == 'food_item' or
                raw_rows['food_type'][raw_rows['food_code'].index(x)][1] == 'std_recipe'
            ]

        positions, food_codes, conv_methods, conv_options = [], [], [], []
        for x in tmp_data:
            positions.append(x[0])
            food_codes.append(x[1])
            conv_methods.append(x[2])
            conv_options.append(x[3])

        return tuple(positions), tuple(food_codes), tuple(conv_methods), tuple(conv_options)

    def _append_conv_factor_gap_data(self, all_rows):
        main_keys = ['conv_factor_gap_code', 'conv_factor_gap_desc']
        additional_keys = {
            'conv_factor_food_code_exists': '1',
            'conv_factor_parent_food_code_exists': '2',
            'conv_factor_food_code_not_available': '3',
            'not_applicable': '9'
        }
        descriptions = {
            '1': 'conv factor available',
            '2': 'using conversion factor from the reference food code',
            '3': 'no conversion factor available',
            '9': 'not applicable',
        }

        self._append_gap_data_help_function(
            all_rows, self._get_conv_factor_data, main_keys, additional_keys, descriptions
        )

    def _get_conv_factor_data(self, all_rows):
        entries = self._get_conv_factor(all_rows)

        return self._get_data_help_function(all_rows, entries, [
            'conv_factor_food_code_exists', 'conv_factor_parent_food_code_exists',
            'conv_factor_food_code_not_available', 'not_applicable'
        ])

    def _append_fct_gap_data(self, all_rows):
        main_keys = ['fct_gap_code', 'fct_gap_desc']
        additional_keys = {
            'fct_food_code_exists': '1',
            'fct_parent_food_code_exists': '2',
            'fct_food_code_not_available': '3',
            'not_applicable': '9'
        }
        descriptions = {
            '1': 'fct data available',
            '2': 'using fct data from the reference food code',
            '3': 'no fct data available',
            '4': 'ingredient(s) missing fct data',
            '9': 'not applicable',
        }

        self._append_gap_data_help_function(
            all_rows, self._get_fct_data, main_keys, additional_keys, descriptions
        )

    def _get_fct_data(self, all_rows):
        food_codes, parent_food_codes, correct_positions = self._get_codes(all_rows)
        entries = self._get_fao_who_gift_food_group(food_codes=food_codes, parent_food_codes=parent_food_codes)

        return self._get_data_help_function(all_rows, entries, [
            'fct_food_code_exists', 'fct_parent_food_code_exists',
            'fct_food_code_not_available', 'not_applicable'
        ])

    def _get_ordered_rows(self, all_rows):

        def add_row(rows):
            for header in self.headers_in_order:
                default = self.default_values.get(header)
                if header == 'parent_food_code':
                    header = 'reference_food_code'
                list_ = all_rows.get(header)
                if not list_:
                    all_rows[header] = [(x, default) for x in range(definitive_length)]
                position, value = all_rows[header][0]
                if position == r:
                    rows[-1].append(value)
                    all_rows[header].pop(0)
                else:
                    rows[-1].append(default)

        if not self.headers_in_order:
            return all_rows
        else:
            ordered_rows = []
            for key in all_rows:
                all_rows[key] = sorted(all_rows[key], key=lambda x: x[0])
            definitive_length = len(all_rows['food_code'])
            for r in range(definitive_length):
                ordered_rows.append([])
                add_row(ordered_rows)

            return ordered_rows

    @staticmethod
    def _get_codes(all_rows):
        food_codes = [
            x for x in all_rows['food_code']
            if all_rows['food_type'][all_rows['food_code'].index(x)][1] == 'food_item' or
            all_rows['food_type'][all_rows['food_code'].index(x)][1] == 'std_recipe'
        ]
        positions = [x[0] for x in food_codes]
        parent_food_codes = [
            x for x in all_rows['reference_food_code']
            if x[0] in positions
        ]

        return food_codes, parent_food_codes, positions

    def _get_data_help_function(self, all_rows, entries, keys):
        food_codes, parent_food_codes, correct_positions = self._get_codes(all_rows)
        food_codes = [x[1] for x in food_codes]
        parent_food_codes = [x[1] for x in parent_food_codes]
        to_return = {x: set() for x in keys}

        positions = set()
        for entry in entries:
            position = entry[0]
            code = entry[1]['food_code']
            if code in food_codes:
                to_return[keys[0]].add((position, 'yes'))
            elif code in parent_food_codes:
                to_return[keys[1]].add((position, 'yes'))
            positions.add(position)

        codes = set(food_codes + parent_food_codes)
        for x in set(all_rows['food_code'] + all_rows['reference_food_code']):
            position, code = x
            if position in correct_positions and code in codes and position not in positions:
                to_return[keys[2]].add((position,))
                positions.add(position)
            elif position not in correct_positions:
                to_return[keys[3]].add((position,))

        return to_return

    @staticmethod
    def _append_gap_data_help_function(all_rows, get_data_function, main_keys, additional_keys, descriptions):

        def add_gap_code(key, code):
            for value in gap_data[key]:
                all_rows[main_keys[0]].append((value[0], code))

        gap_data = get_data_function(all_rows)
        for key in additional_keys:
            add_gap_code(key, additional_keys[key])

        all_rows[main_keys[0]] = sorted(all_rows[main_keys[0]], key=lambda x: x[0])
        for tuple_ in all_rows[main_keys[0]]:
            all_rows[main_keys[1]].append((tuple_[0], descriptions[tuple_[1]]))

    def _get_filtered_rows(self, ordered_rows, additional_filters_indexes_dict):

        def check_if_tuple_valid(r, k, i):
            if not self.additional_filters.get(k[0]) and not self.additional_filters.get(k[1]):
                return True
            if r[i[0]] != self.additional_filters.get(k[0]) and r[i[1]] != self.additional_filters.get(k[1]):
                return False

        def check_if_not_tuple_valid(r, k, i):
            if not self.additional_filters.get(k):
                return True
            if r[i] != self.additional_filters.get(k):
                return False

        filtered_rows = []
        for row in ordered_rows:
            valids = []
            for key, index in additional_filters_indexes_dict.items():
                if isinstance(key, tuple):
                    valids.append(check_if_tuple_valid(row, key, index))
                else:
                    valids.append(check_if_not_tuple_valid(row, key, index))

            if False not in valids:
                filtered_rows.append(row)

        return filtered_rows


class GapsReportByItemSummaryData(GapsReportByItemDataMixin):
    total_row = None
    title = 'Gaps Report By Item - Summary'
    slug = 'gaps_report_by_item_summary'
    headers_in_order = [
        'food_code', 'food_name', 'fao_who_gift_food_group_code', 'fao_who_gift_food_group_des', 'food_type',
        'number_of_occurrences', 'conv_factor_gap_code', 'conv_factor_gap_desc', 'fct_gap_code', 'fct_gap_desc',
        'food_base_term', 'tag_1', 'other_tag_1', 'tag_2', 'other_tag_2', 'tag_3', 'other_tag_3', 'tag_4',
        'other_tag_4', 'tag_5', 'other_tag_5', 'tag_6', 'other_tag_6', 'tag_7', 'other_tag_7', 'tag_8', 'other_tag_8',
        'tag_9', 'other_tag_9', 'tag_10', 'other_tag_10', 'report_data_type', 'external_id'
    ]

    def __init__(self, config):
        super(GapsReportByItemSummaryData, self).__init__()
        self.config = config

    @property
    def additional_filters(self):
        return {
            'fct_gap_desc': self.config['gap_description'],
            'conv_factor_gap_desc': self.config['gap_description'],
        }

    @property
    def additional_headers(self):
        return {
            'ds': [],
            'not_ds': ['number_of_occurrences']
        }

    @property
    def rows(self):
        raw_rows = super(GapsReportByItemSummaryData, self).raw_rows
        self._append_number_of_occurrences(raw_rows)
        self._append_report_data_type(raw_rows, 'gap_by_item_summary')

        return self._get_filtered_rows(self._get_ordered_rows(raw_rows), {
            ('fct_gap_desc', 'conv_factor_gap_desc'): (9, 7)
        })

    @property
    def default_values(self):
        return {
            'number_of_occurrences': '1'
        }

    @staticmethod
    def _get_number_of_occurrences(food_codes, parent_food_codes):
        number_of_occurrences = {}
        positions = {}
        for tuple_ in food_codes:
            position, code = tuple_
            if code is None:
                parent_food_code = parent_food_codes[food_codes.index(tuple_)][1]
                if parent_food_code:
                    code = parent_food_code
                else:
                    continue
            if not number_of_occurrences.get(code):
                number_of_occurrences[code] = 1
                positions[code] = position
            else:
                number_of_occurrences[code] += 1

        return positions, number_of_occurrences

    def _append_number_of_occurrences(self, all_rows):
        food_codes = all_rows['food_code']
        parent_food_codes = all_rows['reference_food_code']
        positions, number_of_occurrences = self._get_number_of_occurrences(food_codes, parent_food_codes)
        for position, code in list(zip(list(positions.values()), list(number_of_occurrences.values()))):
            all_rows['number_of_occurrences'].append((position, code))


class GapsReportByItemDetailsData(GapsReportByItemDataMixin):
    total_row = None
    title = 'Gaps Report By Item - Details'
    slug = 'gaps_report_by_item_details'
    headers_in_order = [
        'gap_type', 'gap_code', 'gap_desc', 'food_case_id', 'respondent_case_id', 'opened_by_username', 'owner_name',
        'respondent_unique_id', 'recall_date', 'food_code', 'short_name', 'food_name', 'food_type', 'time_of_day',
        'time_block', 'fao_who_gift_food_group_code', 'fao_who_gift_food_group_description',
        'user_food_group_description', 'food_base_term', 'tag_1', 'other_tag_1', 'tag_2', 'other_tag_2', 'tag_3',
        'other_tag_3', 'tag_4', 'other_tag_4', 'tag_5', 'other_tag_5', 'tag_6', 'other_tag_6', 'tag_7', 'other_tag_7',
        'tag_8', 'other_tag_8', 'tag_9', 'other_tag_9', 'tag_10', 'other_tag_10', 'conv_method', 'conv_method_desc',
        'conv_option', 'conv_option_desc', 'conv_size', 'conv_units', 'quantity', 'conv_factor_used',
        'conv_factor_food_code', 'conv_factor_parent_food_code', 'fct_used', 'fct_food_code_exists',
        'fct_parent_food_code_exists', 'parent_food_code', 'nsr_conv_method_post_cooking',
        'nsr_conv_method_desc_post_cooking', 'nsr_conv_option_post_cooking', 'nsr_conv_option_desc_post_cooking',
        'nsr_conv_size_post_cooking', 'nsr_same_conv_method', 'nsr_consumed_cooked_ratio',
        'report_data_type', 'external_id',
    ]
    ADDITIONAL_NAMES = [
        'conv_method_desc', 'conv_option_desc', 'conv_size', 'conv_units',
        'opened_by_username', 'owner_name', 'quantity', 'recall_date', 'short_name', 'time_block',
        'unique_respondent_id', 'recall_case_id',
        'nsr_consumed_cooked_ratio', 'nsr_conv_method_desc_post_cooking', 'nsr_conv_method_post_cooking',
        'nsr_conv_option_desc_post_cooking', 'nsr_conv_option_post_cooking', 'nsr_conv_size_post_cooking',
        'nsr_same_conv_method',
    ]

    def __init__(self, config):
        super(GapsReportByItemDetailsData, self).__init__()
        self.config = config

    @property
    def additional_headers(self):
        return {
            'ds': self.ADDITIONAL_NAMES,
            'not_ds': [
                'conv_factor_used', 'fct_food_code_exists',
                'fct_parent_food_code_exists', 'fct_used', 'gap_type', 'gap_code', 'gap_desc',
                'time_of_day', 'user_food_group_description'
            ]
        }

    @property
    def additional_columns(self):
        return self.ADDITIONAL_NAMES + super(GapsReportByItemDetailsData, self).additional_columns

    @property
    @memoized
    def rows(self):
        raw_rows = super(GapsReportByItemDetailsData, self).raw_rows
        self._append_conv_factor_used(
            raw_rows['conv_factor_food_code'], raw_rows['conv_factor_parent_food_code'], raw_rows
        )
        self._append_fct_related_data(self._get_fct_data(raw_rows), raw_rows)

        return self._get_ordered_rows(raw_rows)

    @staticmethod
    def _append_conv_factor_used(conv_factor_food_code, conv_factor_parent_food_code, rows):
        conv_factor_used_food_code = [x[0] for x in conv_factor_food_code]
        conv_factor_used_parent_food_code = [x[0] for x in conv_factor_parent_food_code]
        added_codes = set()

        for x in [rows['food_code'], rows['reference_food_code']]:
            for tuple_ in x:
                position, code = tuple_
                if code not in added_codes:
                    if code in conv_factor_used_food_code:
                        rows['conv_factor_used'].append((position, 'food_code'))
                    elif code in conv_factor_used_parent_food_code:
                        rows['conv_factor_used'].append((position, 'reference_food_code'))
                    else:
                        rows['conv_factor_used'].append((position, None))
                    added_codes.add(code)

    @staticmethod
    def _append_fct_related_data(fct_existence, all_rows):
        for key, values in fct_existence.items():
            if key not in ['fct_food_code_exists', 'fct_parent_food_code_exists']:
                continue
            all_rows[key] += fct_existence[key]
            for value in values:
                if 'parent' in key:
                    fct_used = 'reference_food_code'
                else:
                    fct_used = 'food_code'
                all_rows['fct_used'].append((value[0], fct_used))
