DOMAIN_INDEX = "hqdomains_20150909_1150"
DOMAIN_MAPPING = {'_meta': {'comment': 'jenny modified on 9/9/2015',
                            'created': None},
 'date_detection': False,
 'date_formats': ['yyyy-MM-dd',
                  "yyyy-MM-dd'T'HH:mm:ssZZ",
                  "yyyy-MM-dd'T'HH:mm:ss.SSSSSS",
                  "yyyy-MM-dd'T'HH:mm:ss.SSSSSS'Z'",
                  "yyyy-MM-dd'T'HH:mm:ss'Z'",
                  "yyyy-MM-dd'T'HH:mm:ssZ",
                  "yyyy-MM-dd'T'HH:mm:ssZZ'Z'",
                  "yyyy-MM-dd'T'HH:mm:ss.SSSZZ",
                  "yyyy-MM-dd'T'HH:mm:ss",
                  "yyyy-MM-dd' 'HH:mm:ss",
                  "yyyy-MM-dd' 'HH:mm:ss.SSSSSS",
                  "mm/dd/yy' 'HH:mm:ss"],
 'dynamic': False,
 'properties': {'area': {'type': 'string'},
                'attribution_notes': {'type': 'string'},
                'author': {'fields': {'author': {'index': 'analyzed',
                                                 'type': 'string'},
                                      'exact': {'index': 'not_analyzed',
                                                'type': 'string'}},
                           'type': 'multi_field'},
                'cached_properties': {'dynamic': False, 'type': 'object'},
                'call_center_config': {'dynamic': False,
                                       'properties': {'case_owner_id': {'type': 'string'},
                                                      'use_fixtures': {'type': 'boolean'},
                                                      'case_type': {'type': 'string'},
                                                      'doc_type': {'index': 'not_analyzed',
                                                                   'type': 'string'},
                                                      'enabled': {'type': 'boolean'}},
                                       'type': 'object'},
                'case_display': {'dynamic': False,
                                 'properties': {'case_details': {'dynamic': False,
                                                                 'type': 'object'},
                                                'doc_type': {'index': 'not_analyzed',
                                                             'type': 'string'},
                                                'form_details': {'dynamic': False,
                                                                 'type': 'object'}},
                                 'type': 'object'},
                'case_sharing': {'type': 'boolean'},
                'cda': {'dynamic': False,
                        'properties': {'date': {'format': "yyyy-MM-dd||yyyy-MM-dd'T'HH:mm:ssZZ||yyyy-MM-dd'T'HH:mm:ss.SSSSSS||yyyy-MM-dd'T'HH:mm:ss.SSSSSS'Z'||yyyy-MM-dd'T'HH:mm:ss'Z'||yyyy-MM-dd'T'HH:mm:ssZ||yyyy-MM-dd'T'HH:mm:ssZZ'Z'||yyyy-MM-dd'T'HH:mm:ss.SSSZZ||yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss.SSSSSS||mm/dd/yy' 'HH:mm:ss",
                                                'type': 'date'},
                                       'doc_type': {'index': 'not_analyzed',
                                                    'type': 'string'},
                                       'signed': {'type': 'boolean'},
                                       'type': {'index': 'not_analyzed',
                                                'type': 'string'},
                                       'user_id': {'type': 'string'},
                                       'user_ip': {'type': 'string'},
                                       'version': {'type': 'string'}},
                        'type': 'object'},
                'commconnect_enabled': {'type': 'boolean'},
                'commtrack_enabled': {'type': 'boolean'},
                'copy_history': {'type': 'string'},
                'cp_first_form': {'format': "yyyy-MM-dd||yyyy-MM-dd'T'HH:mm:ssZZ||yyyy-MM-dd'T'HH:mm:ss.SSSSSS||yyyy-MM-dd'T'HH:mm:ss.SSSSSS'Z'||yyyy-MM-dd'T'HH:mm:ss'Z'||yyyy-MM-dd'T'HH:mm:ssZ||yyyy-MM-dd'T'HH:mm:ssZZ'Z'||yyyy-MM-dd'T'HH:mm:ss.SSSZZ||yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss.SSSSSS||mm/dd/yy' 'HH:mm:ss",
                                  'type': 'date'},
                'cp_has_app': {'type': 'boolean'},
                'cp_is_active': {'type': 'boolean'},
                'cp_last_form': {'format': "yyyy-MM-dd||yyyy-MM-dd'T'HH:mm:ssZZ||yyyy-MM-dd'T'HH:mm:ss.SSSSSS||yyyy-MM-dd'T'HH:mm:ss.SSSSSS'Z'||yyyy-MM-dd'T'HH:mm:ss'Z'||yyyy-MM-dd'T'HH:mm:ssZ||yyyy-MM-dd'T'HH:mm:ssZZ'Z'||yyyy-MM-dd'T'HH:mm:ss.SSSZZ||yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss.SSSSSS||mm/dd/yy' 'HH:mm:ss",
                                 'type': 'date'},
                'cp_n_60_day_cases': {'type': 'long'},
                'cp_n_active_cases': {'type': 'long'},
                'cp_n_active_cc_users': {'type': 'long'},
                'cp_n_cases': {'type': 'long'},
                'cp_n_cc_users': {'type': 'long'},
                'cp_n_forms': {'type': 'long'},
                'cp_n_inactive_cases': {'type': 'long'},
                'cp_n_users_submitted_form': {'type': 'long'},
                'cp_n_web_users': {'type': 'long'},
                'cp_n_out_sms': {'type': 'long'},
                'cp_n_in_sms': {'type': 'long'},
                'cp_n_sms_ever': {'type': 'long'},
                'cp_n_sms_30_d': {'type': 'long'},
                'cp_n_sms_in_30_d': {'type': 'long'},
                'cp_n_sms_out_30_d': {'type': 'long'},
                'cp_sms_ever': {'type': 'boolean'},
                'cp_sms_30_d': {'type': 'boolean'},
                'cp_last_updated': {'format': "yyyy-MM-dd||yyyy-MM-dd'T'HH:mm:ssZZ||yyyy-MM-dd'T'HH:mm:ss.SSSSSS||yyyy-MM-dd'T'HH:mm:ss.SSSSSS'Z'||yyyy-MM-dd'T'HH:mm:ss'Z'||yyyy-MM-dd'T'HH:mm:ssZ||yyyy-MM-dd'T'HH:mm:ssZZ'Z'||yyyy-MM-dd'T'HH:mm:ss.SSSZZ||yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss.SSSSSS||mm/dd/yy' 'HH:mm:ss",
                                    'type': 'date'},
                'creating_user': {'type': 'string'},
                'customer_type': {'type': 'string'},
                'date_created': {'format': "yyyy-MM-dd||yyyy-MM-dd'T'HH:mm:ssZZ||yyyy-MM-dd'T'HH:mm:ss.SSSSSS||yyyy-MM-dd'T'HH:mm:ss.SSSSSS'Z'||yyyy-MM-dd'T'HH:mm:ss'Z'||yyyy-MM-dd'T'HH:mm:ssZ||yyyy-MM-dd'T'HH:mm:ssZZ'Z'||yyyy-MM-dd'T'HH:mm:ss.SSSZZ||yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss.SSSSSS||mm/dd/yy' 'HH:mm:ss",
                                 'type': 'date'},
                'default_sms_backend_id': {'type': 'string'},
                'default_timezone': {'type': 'string'},
                'deployment': {'dynamic': False,
                               'properties': {'city': {'fields': {'city': {'index': 'analyzed',
                                                                           'type': 'string'},
                                                                  'exact': {'index': 'not_analyzed',
                                                                            'type': 'string'}},
                                                       'type': 'multi_field'},
                                              'countries': {'fields':
                                                               {'countries': {'index': 'not_analyzed',
                                                                              'type': 'string'},
                                                                'exact': {'index': 'not_analyzed',
                                                                          'type': 'string'}},
                                                            'type': 'multi_field'},
                                              'date': {'format': "yyyy-MM-dd||yyyy-MM-dd'T'HH:mm:ssZZ||yyyy-MM-dd'T'HH:mm:ss.SSSSSS||yyyy-MM-dd'T'HH:mm:ss.SSSSSS'Z'||yyyy-MM-dd'T'HH:mm:ss'Z'||yyyy-MM-dd'T'HH:mm:ssZ||yyyy-MM-dd'T'HH:mm:ssZZ'Z'||yyyy-MM-dd'T'HH:mm:ss.SSSZZ||yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss.SSSSSS||mm/dd/yy' 'HH:mm:ss",
                                                       'type': 'date'},
                                              'description': {'fields': {'description': {'index': 'analyzed',
                                                                                         'type': 'string'},
                                                                         'exact': {'index': 'not_analyzed',
                                                                                   'type': 'string'}},
                                                              'type': 'multi_field'},
                                              'doc_type': {'index': 'not_analyzed',
                                                           'type': 'string'},
                                              'public': {'type': 'boolean'},
                                              'region': {'fields': {'exact': {'index': 'not_analyzed',
                                                                              'type': 'string'},
                                                                    'region': {'index': 'analyzed',
                                                                               'type': 'string'}},
                                                         'type': 'multi_field'}},
                               'type': 'object'},
                'description': {'type': 'string'},
                'doc_type': {'index': 'not_analyzed', 'type': 'string'},
                'downloads': {'type': 'long'},
                'dynamic_reports': {'dynamic': False,
                                    'properties': {'doc_type': {'index': 'not_analyzed',
                                                                'type': 'string'},
                                                   'reports': {'dynamic': False,
                                                               'properties': {'doc_type': {'index': 'not_analyzed',
                                                                                           'type': 'string'},
                                                                              'kwargs': {'dynamic': False,
                                                                                         'type': 'object'},
                                                                              'name': {'type': 'string'},
                                                                              'report': {'type': 'string'}},
                                                               'type': 'object'},
                                                   'section_title': {'type': 'string'}},
                                    'type': 'object'},
                'full_downloads': {'type': 'long'},
                'hr_name': {'type': 'string'},
                'image_path': {'type': 'string'},
                'image_type': {'type': 'string'},
                'internal': {'dynamic': False,
                             'properties': {'area': {'fields': {'area': {'index': 'analyzed',
                                                                         'type': 'string'},
                                                                'exact': {'index': 'not_analyzed',
                                                                          'type': 'string'}},
                                                     'type': 'multi_field'},
                                            'can_use_data': {'type': 'boolean'},
                                            'commcare_edition': {'type': 'string'},
                                            'custom_eula': {'type': 'boolean'},
                                            'doc_type': {'index': 'not_analyzed',
                                                         'type': 'string'},
                                            'goal_time_period': {'type': 'long'},
                                            'goal_followup_rate': {'type': 'double'},
                                            'commconnect_domain': {'type': 'boolean'},
                                            'commtrack_domain': {'type': 'boolean'},
                                            'initiative': {'fields': {'exact': {'index': 'not_analyzed',
                                                                                'type': 'string'},
                                                                      'initiative': {'index': 'analyzed',
                                                                                     'type': 'string'}},
                                                           'type': 'multi_field'},
                                            'workshop_region': {'fields': {'exact': {'index': 'not_analyzed',
                                                                           'type': 'string'},
                                                                'workshop_region': {'index': 'analyzed',
                                                                           'type': 'string'}},
                                                           'type': 'multi_field'},
                                            'notes': {'type': 'string'},
                                            'organization_name': {'fields': {'exact': {'index': 'not_analyzed',
                                                                                       'type': 'string'},
                                                                             'organization_name': {'index': 'analyzed',
                                                                                                   'type': 'string'}},
                                                                  'type': 'multi_field'},
                                            'phone_model': {'fields': {'exact': {'index': 'not_analyzed',
                                                                                 'type': 'string'},
                                                                       'phone_model': {'index': 'analyzed',
                                                                                       'type': 'string'}},
                                                            'type': 'multi_field'},
                                            'platform': {'type': 'string'},
                                            'project_manager': {'type': 'string'},
                                            'project_state': {'type': 'string'},
                                            'self_started': {'type': 'boolean'},
                                            'services': {'type': 'string'},
                                            'sf_account_id': {'type': 'string'},
                                            'sf_contract_id': {'type': 'string'},
                                            'sub_area': {'fields': {'exact': {'index': 'not_analyzed',
                                                                              'type': 'string'},
                                                                    'sub_area': {'index': 'analyzed',
                                                                                 'type': 'string'}},
                                                         'type': 'multi_field'},
                                            'using_adm': {'type': 'boolean'},
                                            'using_call_center': {'type': 'boolean'}},
                             'type': 'object'},
                'is_active': {'type': 'boolean'},
                'is_approved': {'type': 'boolean'},
                'is_public': {'type': 'boolean'},
                'is_shared': {'type': 'boolean'},
                'is_sms_billable': {'type': 'boolean'},
                'is_snapshot': {'type': 'boolean'},
                'is_test': {'type': 'string'},
                'is_starter_app': {'type': 'boolean'},
                'last_modified': {'format': "yyyy-MM-dd||yyyy-MM-dd'T'HH:mm:ssZZ||yyyy-MM-dd'T'HH:mm:ss.SSSSSS||yyyy-MM-dd'T'HH:mm:ss.SSSSSS'Z'||yyyy-MM-dd'T'HH:mm:ss'Z'||yyyy-MM-dd'T'HH:mm:ssZ||yyyy-MM-dd'T'HH:mm:ssZZ'Z'||yyyy-MM-dd'T'HH:mm:ss.SSSZZ||yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss.SSSSSS||mm/dd/yy' 'HH:mm:ss",
                                  'type': 'date'},
                'license': {'type': 'string'},
                'migrations': {'dynamic': False,
                               'properties': {'doc_type': {'index': 'not_analyzed',
                                                           'type': 'string'},
                                              'has_migrated_permissions': {'type': 'boolean'}},
                               'type': 'object'},
                'multimedia_included': {'type': 'boolean'},
                'name': {'fields': {'exact': {'index': 'not_analyzed',
                                              'type': 'string'},
                                    'name': {'index': 'analyzed',
                                             'type': 'string'}},
                         'type': 'multi_field'},
                'organization': {'type': 'string'},
                'phone_model': {'type': 'string'},
                'project_type': {'analyzer': 'comma', 'type': 'string'},
                'published': {'type': 'boolean'},
                'publisher': {'type': 'string'},
                'allow_domain_requests': {'type': 'boolean'},
                'restrict_superusers': {'type': 'boolean'},
                'secure_submissions': {'type': 'boolean'},
                'short_description': {'fields': {'exact': {'index': 'not_analyzed',
                                                           'type': 'string'},
                                                 'short_description': {'index': 'analyzed',
                                                                       'type': 'string'}},
                                      'type': 'multi_field'},
                'sms_case_registration_enabled': {'type': 'boolean'},
                'sms_case_registration_owner_id': {'type': 'string'},
                'sms_case_registration_type': {'type': 'string'},
                'sms_case_registration_user_id': {'type': 'string'},
                'sms_mobile_worker_registration_enabled': {'type': 'boolean'},
                'snapshot_time': {'format': "yyyy-MM-dd||yyyy-MM-dd'T'HH:mm:ssZZ||yyyy-MM-dd'T'HH:mm:ss.SSSSSS||yyyy-MM-dd'T'HH:mm:ss.SSSSSS'Z'||yyyy-MM-dd'T'HH:mm:ss'Z'||yyyy-MM-dd'T'HH:mm:ssZ||yyyy-MM-dd'T'HH:mm:ssZZ'Z'||yyyy-MM-dd'T'HH:mm:ss.SSSZZ||yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss||yyyy-MM-dd' 'HH:mm:ss.SSSSSS||mm/dd/yy' 'HH:mm:ss",
                                  'type': 'date'},
                'sub_area': {'type': 'string'},
                'subscription': {'type': 'string'},
                'survey_management_enabled': {'type': 'boolean'},
                'tags': {'type': 'string'},
                'title': {'fields': {'exact': {'index': 'not_analyzed',
                                               'type': 'string'},
                                     'title': {'index': 'analyzed',
                                               'type': 'string'}},
                          'type': 'multi_field'},
                'yt_id': {'type': 'string'}}}
