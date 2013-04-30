__author__ = 'Jacky'

import unittest

from circuits import circuit
from components import gates, sources


class TestCircuit(unittest.TestCase):
    def test_constructor(self):
        c = circuit.Circuit('circuit', [], [])
        self.assertEqual('circuit', c.name)
        self.assertEqual(0, c.input_size)
        self.assertEqual(0, c.output_size)

        self.assertEqual([], c.inputs)
        self.assertEqual([], c.outputs)

        a = gates.ANDGate()
        b = gates.ORGate()
        c = circuit.Circuit('circuit', [a], [b])

        self.assertEqual('circuit', c.name)
        self.assertEqual(2, c.input_size)
        self.assertEqual(1, c.output_size)

        self.assertEqual([a], c.inputs)
        self.assertEqual([b], c.outputs)

    def test_append_input(self):
        a = gates.ANDGate()
        b = gates.ORGate()

        c = circuit.Circuit('circuit', [a], [])
        c.append_input(b)

        self.assertEqual(4, c.input_size)
        self.assertEqual(0, c.output_size)

        self.assertEqual([a, b], c.inputs)
        self.assertEqual([], c.outputs)

    def test_prepend_input(self):
        a = gates.ANDGate()
        b = gates.ORGate()

        c = circuit.Circuit('circuit', [a], [])
        c.prepend_input(b)

        self.assertEqual(4, c.input_size)
        self.assertEqual(0, c.output_size)

        self.assertEqual([b, a], c.inputs)
        self.assertEqual([], c.outputs)

    def test_append_output(self):
        a = gates.ANDGate()
        b = gates.ORGate()

        c = circuit.Circuit('circuit', [], [a])
        c.append_output(b)

        self.assertEqual(0, c.input_size)
        self.assertEqual(2, c.output_size)

        self.assertEqual([a, b], c.outputs)
        self.assertEqual([], c.inputs)

    def test_prepend_output(self):
        a = gates.ANDGate()
        b = gates.ORGate()

        c = circuit.Circuit('circuit', [], [a])
        c.prepend_output(b)

        self.assertEqual(0, c.input_size)
        self.assertEqual(2, c.output_size)

        self.assertEqual([b, a], c.outputs)
        self.assertEqual([], c.inputs)

    def test_evaluate(self):
        # Try a semi-complex circuit (full-adder)
        xor1 = gates.XORGate()
        xor2 = gates.XORGate()
        and1 = gates.ANDGate()
        and2 = gates.ANDGate()
        or1 = gates.ORGate()
        s = sources.DigitalArbitrary([1, 1, 0])

        xor1.add_input(s, {0: 0, 1: 1})
        xor2.add_input(xor1, {0: 0})
        xor2.add_input(s, {2: 1})
        and1.add_input(xor1, {0: 0})
        and1.add_input(s, {2: 1})
        and2.add_input(s, {0: 0, 1: 1})
        or1.add_input(and1, {0: 0})
        or1.add_input(and2, {0: 1})

        c = circuit.Circuit('full_adder', [s], [xor2, or1])
        self.assertEqual([0, 1], c.evaluate())


class TestCircuitFunctions(unittest.TestCase):
    def test_connect_circuits(self):
        a = gates.ANDGate()
        b = gates.ORGate()
        c = gates.XORGate()

        c1 = circuit.Circuit('test1', [a, b], [a, b])
        c2 = circuit.Circuit('test2', [c], [c])

        circuit.connect_circuits(c1, c2, {0: 0, 1: 1})

        self.assertEqual([(a, 0), (b, 0)], c._input_bits)

    def test_stack_circuits(self):
        a = gates.ANDGate()
        b = gates.ORGate()

        c1 = circuit.Circuit('test1', [a], [a])
        c2 = circuit.Circuit('test2', [b], [b])

        c3 = circuit.stack_circuits('test3', c1, c2)

        self.assertEqual('test3', c3.name)
        self.assertEqual([a, b], c3.inputs)
        self.assertEqual([a, b], c3.outputs)

        self.assertEqual(4, c3.input_size)
        self.assertEqual(2, c3.output_size)

    def test_merge_circuits(self):
        a = gates.ANDGate()
        b = gates.ORGate()
        c = gates.XORGate()

        c1 = circuit.Circuit('test1', [a, b], [a, b])
        c2 = circuit.Circuit('test2', [c], [c])

        c3 = circuit.merge_circuits('test3', c1, c2)

        self.assertEqual([a, b], c3.inputs)
        self.assertEqual([c], c3.outputs)

        self.assertEqual(4, c3.input_size)
        self.assertEqual(1, c3.output_size)