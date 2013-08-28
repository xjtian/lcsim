__author__ = 'Jacky'

import unittest
from circuits import sources


class TestDigitalSource(unittest.TestCase):
    def test_function(self):
        c = sources.digital_source_circuit([0, 1, 1, 0, 0])

        self.assertEqual('dSrc', c.name)
        self.assertEqual([0, 1, 1, 0, 0], c.evaluate())
        self.assertEqual(0, len(c._inputs))


class TestDigitalSourceInt(unittest.TestCase):
    def test_function(self):
        c = sources.digital_source_int_circuit(0, 1)

        self.assertEqual('dSrc', c.name)
        self.assertEqual(0, len(c._inputs))

    def test_no_padding(self):
        c = sources.digital_source_int_circuit(31, 5)
        self.assertEqual([1, 1, 1, 1, 1], c.evaluate())

        c = sources.digital_source_int_circuit(63, 6)
        self.assertEqual([1, 1, 1, 1, 1, 1], c.evaluate())

        c = sources.digital_source_int_circuit(53, 6)
        self.assertEqual([1, 1, 0, 1, 0, 1], c.evaluate())

        c = sources.digital_source_int_circuit(1, 1)
        self.assertEqual([1], c.evaluate())

    def test_with_padding(self):
        c = sources.digital_source_int_circuit(128, 16)
        self.assertEqual([0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], c.evaluate())

        c = sources.digital_source_int_circuit(77, 8)
        self.assertEqual([0, 1, 0, 0, 1, 1, 0, 1], c.evaluate())

    def test_hex(self):
        c = sources.digital_source_int_circuit(0xDEAD, 16)
        self.assertEqual([1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1], c.evaluate())

        c = sources.digital_source_int_circuit(0xBEEF, 32)
        self.assertEqual([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1], c.evaluate())
