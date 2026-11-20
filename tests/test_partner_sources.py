import json
from pathlib import Path
import unittest


RECORDS = Path(__file__).resolve().parents[1] / 'records'
SCHEMAS = {'catalog.json': 'dict', 'cohorts.json': 'list', 'registrar.json': 'dict',
           'followup_exchange.json': 'dict'}


class PartnerSourceTests(unittest.TestCase):
    def test_format(self):
        self.assertEqual({path.name for path in RECORDS.iterdir()}, set(SCHEMAS))
        for name, shape in SCHEMAS.items():
            with self.subTest(name=name), (RECORDS / name).open(encoding='utf-8', newline='') as source:
                records = json.load(source)
                self.assertIsInstance(records, list if shape == 'list' else dict)
                self.assertTrue(records)

    def test_followup_exchange_references(self):
        def read(name):
            return json.loads((RECORDS / name).read_text(encoding='utf-8'))

        exchange = read('followup_exchange.json')
        registrar = read('registrar.json')
        catalog = read('catalog.json')
        attempts = {row['attempt']: row for row in registrar['transcripts']}
        applications = {row['id']: row for row in registrar['applications']}
        subjects = {row['person'] for row in registrar['applications']}
        observations = {row['checkpoint']['observation']: row for row in exchange['cohorts']}
        self.assertEqual(len(observations), len(exchange['cohorts']))
        self.assertTrue(all(row['person'] in subjects for row in exchange['profiles']))
        for row in exchange['cohorts']:
            self.assertTrue(all(event['activity'] in catalog['activities'] for event in row['events']))
            last_event = max(event['at'] for event in row['events'])
            self.assertLess(last_event, row['checkpoint']['available_after'])
        for notice in exchange['corrections']:
            observed = observations[notice['observation']]
            self.assertIn(notice['changes']['evidence'], {event['task_id'] for event in observed['events']})
            self.assertLessEqual(notice['effective_archive_day'], notice['recv_at'] + exchange['archive_day_offset'])
        for event in registrar['events']:
            if 'support_observation' not in event:
                continue
            application = applications[event['application']]
            self.assertTrue(all(attempts[key]['person'] == application['person'] for key in event['attempt']))
            for key in event['support_observation']:
                self.assertLessEqual(observations[key]['checkpoint']['available_after'],
                                     event['recv_at'] + exchange['archive_day_offset'])
