import csv
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1] / "records"


class SourceContract(unittest.TestCase):
    def test_export_shape(self):
        self.assertEqual({path.name for path in ROOT.iterdir()}, set(EXPECTED))
        for name, contract in EXPECTED.items():
            with self.subTest(source=name):
                path = ROOT / name
                if path.suffix == ".csv":
                    with path.open(encoding="utf-8", newline="") as source:
                        reader = csv.DictReader(source)
                        self.assertEqual(reader.fieldnames, contract)
                        rows = list(reader)
                    self.assertTrue(rows)
                    self.assertTrue(all(None not in row and None not in row.values() for row in rows))
                else:
                    body = json.loads(path.read_text(encoding="utf-8"))
                    self.assertIsInstance(body, list if contract == "list" else dict)
                    self.assertTrue(body)

    def test_related_export_records(self):
        for name, value in SEQUENCE.items():
            with self.subTest(source=name):
                path = ROOT / name
                if path.suffix == ".csv":
                    with path.open(encoding="utf-8", newline="") as source:
                        cells = {cell for row in csv.reader(source) for cell in row}
                else:
                    rows = json.loads(path.read_text(encoding="utf-8"))
                    cells = {item for row in rows for item in row.values() if isinstance(item, str)}
                self.assertIn(value, cells)


EXPECTED = {'pairs.csv': ['pair', 'left', 'right', 'area', 'start', 'active_until'], 'observations.csv': ['id', 'pair', 'reporter', 'kind', 'interaction', 'earliest', 'latest', 'collected'], 'permission.csv': ['day', 'person', 'pair', 'check', 'meeting', 'exit'], 'slots.csv': ['id', 'day', 'start', 'length', 'volunteer'], 'bookings.csv': ['at', 'id', 'slot', 'pair', 'person', 'kind', 'state'], 'past_actions.csv': ['action', 'type', 'region', 'lag_days', 'confirmed', 'unresolved', 'window_mature'], 'policy.json': 'dict'}
SEQUENCE = {'observations.csv': 'h4', 'permission.csv': 't1', 'bookings.csv': 'confirmed'}
