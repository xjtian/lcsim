__author__ = 'Jacky'

import unittest
from circuits import circuit
from components import base


class TestCircuit(unittest.TestCase):
    def test_constructor(self):
        c = circuit.Circuit('name', 5, 3)

        self.assertEqual('name', c.name)
        self.assertEqual([None, None, None, None, None], c._inputs)
        self.assertEqual([None, None, None], c._outputs)

    def test_add_input_component(self):
        a = base.ComponentBase('gate', 2, 0)
        c = circuit.Circuit('circuit', 2, 0)

        c.add_input_component(a, {0: 0, 1: 1})
        self.assertEqual([(a, 0), (a, 1)], c._inputs)

        c = circuit.Circuit('circuit', 2, 0)
        self.assertRaises(ValueError, c.add_input_component, a, {-1: 0})
        self.assertRaises(ValueError, c.add_input_component, a, {3: 0})
        self.assertRaises(ValueError, c.add_input_component, a, {0: 4})

    def test_add_output_component(self):
        a = base.ComponentBase('gate', 0, 2)
        c = circuit.Circuit('circuit', 0, 2)

        c.add_output_component(a, {0: 0, 1: 1})
        self.assertEqual([(a, 0), (a, 1)], c._outputs)

        c = circuit.Circuit('circuit', 0, 2)
        self.assertRaises(ValueError, c.add_output_component, a, {-1: 0})
        self.assertRaises(ValueError, c.add_output_component, a, {3: 0})
        self.assertRaises(ValueError, c.add_output_component, a, {0: 4})
