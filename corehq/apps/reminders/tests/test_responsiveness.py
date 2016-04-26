from corehq.apps.hqcase.utils import update_case
from corehq.apps.reminders.models import (CaseReminderHandler, CaseReminder, MATCH_EXACT,
    REPEAT_SCHEDULE_INDEFINITELY)
from corehq.form_processor.tests.utils import run_with_all_backends
from corehq.util.test_utils import create_test_case
from datetime import datetime, date, time
from django.test import TestCase
from mock import patch


class ReminderResponsivenessTest(TestCase):
    def setUp(self):
        self.domain = 'reminder-responsiveness-test'

    def get_reminders(self):
        return CaseReminder.view('reminders/by_domain_handler_case',
            start_key=[self.domain],
            end_key=[self.domain, {}],
            include_docs=True).all()

    @run_with_all_backends
    def test_case_property_match_equal(self):
        reminder = (CaseReminderHandler
            .create(self.domain, 'test')
            .set_case_criteria_start_condition('participant', 'status', MATCH_EXACT, 'green')
            .set_case_criteria_start_date()
            .set_case_recipient()
            .set_sms_content_type('en')
            .set_daily_schedule(fire_time=time(12, 0), message={'en': 'Hello {case.name}, your test result was normal.'})
            .set_stop_condition(max_iteration_count=REPEAT_SCHEDULE_INDEFINITELY))
        reminder.save()

        self.assertEqual(self.get_reminders(), [])

        with create_test_case(self.domain, 'participant', 'bob', drop_signals=False) as case, \
                patch('corehq.apps.reminders.models.CaseReminderHandler.get_now') as now_mock:
            self.assertEqual(self.get_reminders(), [])

            now_mock.return_value = datetime(2016, 1, 1, 10, 0)
            update_case(self.domain, case.case_id, case_properties={'status': 'green'})

            reminder_instances = self.get_reminders()
            self.assertEqual(len(reminder_instances), 1)
            reminder_instance = reminder_instances[0]

            self.assertEqual(reminder_instance.domain, self.domain)
            self.assertEqual(reminder_instance.handler_id, reminder.get_id)
            self.assertTrue(reminder_instance.active)
            self.assertEqual(reminder_instance.start_date, date(2016, 1, 1))
            self.assertIsNone(reminder_instance.start_condition_datetime)
            self.assertEqual(reminder_instance.next_fire, datetime(2016, 1, 1, 12, 0))
            self.assertEqual(reminder_instance.case_id, case.case_id)
            self.assertEqual(reminder_instance.schedule_iteration_num, 1)
            self.assertEqual(reminder_instance.current_event_sequence_num, 0)

            update_case(self.domain, case.case_id, case_properties={'status': 'red'})
            self.assertEqual(self.get_reminders(), [])

    def tearDown(self):
        for reminder in CaseReminderHandler.get_handlers(self.domain):
            for reminder_instance in reminder.get_reminders():
                reminder_instance.delete()
            reminder.delete()
