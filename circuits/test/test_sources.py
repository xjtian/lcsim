__author__ = 'Jacky'

import unittest
from circuits import sources


class TestDigitalSource(unittest.TestCase):
    def test_function(self):
        c = sources.digital_source_circuit([0, 1, 1, 0, 0])

        self.assertEqual('dSrc', c.name)
        self.assertEqual([0, 1, 1, 0, 0], c.evaluate())
        self.assertEqual(0, len(c._inputs))
