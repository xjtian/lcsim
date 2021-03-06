from lcsim.circuits import circuit
from lcsim.components import base

__author__ = 'Jacky'

import unittest


class TestCircuit(unittest.TestCase):
    def test_constructor(self):
        c = circuit.Circuit('name', 5, 3)

        self.assertEqual('name', c.name)
        self.assertEqual([[], [], [], [], []], c._inputs)
        self.assertEqual([None, None, None], c._outputs)

    def test_add_input_component(self):
        a = base.ComponentBase('gate', 3)
        c = circuit.Circuit('circuit', 2, 0)

        c.add_input_component(a, {0: 0, 1: 1})
        # Now try wiring the same input space to multiple gate inputs
        c.add_input_component(a, {0: 2})
        self.assertEqual([[(a, 0), (a, 2)], [(a, 1)]], c._inputs)

        c = circuit.Circuit('circuit', 2, 0)
        self.assertRaises(ValueError, c.add_input_component, a, {-1: 0})
        self.assertRaises(ValueError, c.add_input_component, a, {3: 0})
        self.assertRaises(ValueError, c.add_input_component, a, {0: 4})

    def test_add_output_component(self):
        a = base.ComponentBase('gate', 0)
        b = base.ComponentBase('gate', 0)

        c = circuit.Circuit('circuit', 0, 2)

        c.add_output_component(a, 0)
        c.add_output_component(b, 1)
        self.assertEqual([a, b], c._outputs)

        c = circuit.Circuit('circuit', 0, 2)
        self.assertRaises(ValueError, c.add_output_component, a, -1)
        self.assertRaises(ValueError, c.add_output_component, a, 2)


class TestConnectCircuits(unittest.TestCase):
    def test_one_to_one(self):
        a = base.ComponentBase('a', 0)
        b = base.ComponentBase('b', 0)
        c = base.ComponentBase('c', 1)
        d = base.ComponentBase('d', 1)

        c1 = circuit.Circuit('c1', 0, 2)
        c2 = circuit.Circuit('c2', 2, 0)

        c1._outputs = [a, b]
        c2._inputs = [[(c, 0)], [(d, 0)]]

        circuit.connect_circuits(c1, c2, {0: 0, 1: 1})
        self.assertEqual([a], c._input_bits)
        self.assertEqual([b], d._input_bits)

    def test_one_to_many(self):
        a = base.ComponentBase('a', 0)
        b = base.ComponentBase('b', 1)
        c = base.ComponentBase('c', 1)
        d = base.ComponentBase('d', 1)

        c1 = circuit.Circuit('c1', 0, 3)
        c2 = circuit.Circuit('c2', 3, 0)

        c1._outputs = [a, a, a]
        c2._inputs = [[(b, 0)], [(c, 0)], [(d, 0)]]

        circuit.connect_circuits(c1, c2, {0: 0, 1: 1, 2: 2})
        self.assertEqual([a], b._input_bits)
        self.assertEqual([a], c._input_bits)
        self.assertEqual([a], d._input_bits)

    def test_many_to_one(self):
        a = base.ComponentBase('a', 3)
        b = base.ComponentBase('b', 0)
        c = base.ComponentBase('c', 0)
        d = base.ComponentBase('d', 0)

        c1 = circuit.Circuit('c1', 0, 3)
        c2 = circuit.Circuit('c2', 3, 0)

        c1._outputs = [b, c, d]
        c2._inputs = [[(a, 0)], [(a, 1)], [(a, 2)]]

        circuit.connect_circuits(c1, c2, {0: 0, 1: 1, 2: 2})
        self.assertEqual([b, c, d], a._input_bits)

    def test_many_to_many(self):
        a = base.ComponentBase('a', 0)
        b = base.ComponentBase('b', 0)
        c = base.ComponentBase('c', 2)
        d = base.ComponentBase('d', 2)

        c1 = circuit.Circuit('c1', 0, 4)
        c2 = circuit.Circuit('c2', 4, 0)

        c1._outputs = [a, b, a, b]
        c2._inputs = [[(c, 0)], [(d, 0)], [(c, 1)], [(d, 1)]]

        circuit.connect_circuits(c1, c2, {0: 0, 1: 1, 2: 2, 3: 3})
        self.assertEqual([a, a], c._input_bits)
        self.assertEqual([b, b], d._input_bits)


class TestStackCircuits(unittest.TestCase):
    def test_function(self):
        c1 = circuit.Circuit('top', 2, 1)
        c2 = circuit.Circuit('bottom', 2, 1)

        c1._inputs = [1, 2]
        c1._outputs = [3]
        c2._inputs = [4, 5]
        c2._outputs = [6]

        c3 = circuit.stack_circuits('stacked', c1, c2)
        self.assertEqual('stacked', c3.name)
        self.assertEqual([1, 2, 4, 5], c3._inputs)
        self.assertEqual([3, 6], c3._outputs)


class TestMergeCircuits(unittest.TestCase):
    def test_function(self):
        c1 = circuit.Circuit('left', 2, 1)
        c2 = circuit.Circuit('right', 1, 2)

        c1._inputs = [1, 2]
        c1._outputs = [3]
        c2._inputs = [4]
        c2._outputs = [5, 6]

        c3 = circuit.merge_circuits('merged', c1, c2)
        self.assertEqual('merged', c3.name)
        self.assertEqual([1, 2], c3._inputs)
        self.assertEqual([5, 6], c3._outputs)
