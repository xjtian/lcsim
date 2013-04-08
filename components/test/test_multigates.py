__author__ = 'Jacky'

import unittest
from components import multigates, base
from components.test import mocks


class MultiGateAddInputMock(multigates.MultiGateBase):
    def __init__(self, name, minimum_input, output_bits):
        super(MultiGateAddInputMock, self).__init__(name, minimum_input, output_bits)

    def add_input(self, component, mapping):
        super(MultiGateAddInputMock, self).add_input(component, mapping)


class TestMultiGateBase(unittest.TestCase):
    def test_constructor(self):
        gate = multigates.MultiGateBase('Test', 12, 2)

        self.assertEqual(gate.min_input, 12)
        self.assertEqual([None] * 12, gate._input_bits)

    def test_add_input(self):
        gate = multigates.MultiGateBase('Test', 1, 2)
        try:
            gate.add_input(mocks.ComponentMockOne('', 0, 10), {i: i for i in xrange(0, 10)})
        except ValueError as e:
            self.fail('ValueError: %s' % e.message)

        self.assertEqual(10, len(gate._input_bits))
        gate.disconnect_inputs()

        try:
            gate.add_input(mocks.ComponentMockOne('', 0, 5), {i: i for i in xrange(0, 5)})
        except ValueError as e:
            self.fail('ValueError: %s' % e.message)

        self.assertEqual(5, len(gate._input_bits))

    def test_evaluate(self):
        gate = mocks.MultiGateAddInputMock('Test', 12, 2)
        gate.add_input(mocks.ComponentMockOne('', 0, 12), {i: i for i in xrange(0, 12)})

        try:
            gate.evaluate()
        except base.MissingInputException:
            self.fail('evaluate() threw unexpected MissingInputException')

        gate = mocks.MultiGateAddInputMock('Test', 12, 2)
        gate.add_input(mocks.ComponentMockZero('', 0, 10), {i: i for i in xrange(0, 10)})

        self.assertRaises(base.MissingInputException, gate.evaluate)
