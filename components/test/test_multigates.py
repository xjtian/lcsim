__author__ = 'Jacky'

import unittest
from components import multigates, base
from components.test import mocks


class TestMultiGateBase(unittest.TestCase):
    def test_constructor(self):
        gate = multigates.MultiGateBase('Test', 12, 2)

        self.assertEqual(gate.min_input, 12)
        self.assertEqual([None] * 12, gate._input_bits)

    def test_add_input(self):
        gate = multigates.MultiGateBase('Test', 1, 2)
        try:
            gate.add_input(mocks.ComponentMockOne('', 0, 10),
                           {i: i for i in xrange(0, 10)})
        except ValueError as e:
            self.fail('ValueError: %s' % e.message)

        self.assertEqual(10, len(gate._input_bits))
        gate.disconnect_inputs()

        # Even though the mapping goes up to 6, input bit 0 is unused so the
        # length of input bits should still be 5
        try:
            gate.add_input(mocks.ComponentMockOne('', 0, 5),
                           {i: i + 1 for i in xrange(0, 5)})
        except ValueError as e:
            self.fail('ValueError: %s' % e.message)

        self.assertEqual(5, len(gate._input_bits))

    def test_evaluate(self):
        gate = mocks.MultiGateAddInputMock('Test', 12, 2)
        gate.add_input(mocks.ComponentMockOne('', 0, 12),
                       {i: i for i in xrange(0, 12)})

        try:
            gate.evaluate()
        except base.MissingInputException:
            self.fail('evaluate() threw unexpected MissingInputException')

        gate = mocks.MultiGateAddInputMock('Test', 12, 2)
        gate.add_input(mocks.ComponentMockZero('', 0, 10),
                       {i: i for i in xrange(0, 10)})

        self.assertRaises(base.MissingInputException, gate.evaluate)


class TestMultiANDGate(unittest.TestCase):
    def setUp(self):
        self.gate = multigates.MultiANDGate()

    def test_constructor(self):
        self.assertEqual([None, None], self.gate._input_bits)
        self.assertEqual(1, len(self.gate.output_bits))
        self.assertEqual('mAND', self.gate.name)

    def test_evaluate(self):
        source_true = mocks.SourceMock('all_true', 0, [1, 1, 1, 1, 1, 1])
        source_false = mocks.SourceMock('', 0, [1, 1, 1, 0])

        self.gate.add_input(source_true, {i: i for i in xrange(0, 5)})
        self.gate.evaluate()
        self.assertEqual([1], self.gate.output_bits)

        self.gate.disconnect_inputs()
        self.gate.add_input(source_false, {i: i for i in xrange(0, 4)})
        self.gate.evaluate()
        self.assertEqual([0], self.gate.output_bits)


class TestMultiORGate(unittest.TestCase):
    def setUp(self):
        self.gate = multigates.MultiORGate()

    def test_constructor(self):
        self.assertEqual([None, None], self.gate._input_bits)
        self.assertEqual(1, len(self.gate.output_bits))
        self.assertEqual('mOR', self.gate.name)

    def test_evaluate(self):
        source_true = mocks.SourceMock('', 0, [0, 0, 1])
        source_false = mocks.SourceMock('', 0, [0, 0, 0])

        self.gate.add_input(source_true, {i: i for i in xrange(0, 3)})
        self.gate.evaluate()
        self.assertEqual([1], self.gate.output_bits)

        self.gate.disconnect_inputs()
        self.gate.add_input(source_false, {i: i for i in xrange(0, 3)})
        self.gate.evaluate()
        self.assertEqual([0], self.gate.output_bits)


class TestMultiNOTGate(unittest.TestCase):
    def setUp(self):
        self.gate = multigates.MultiNOTGate()

    def test_constructor(self):
        self.assertEqual([None], self.gate._input_bits)
        self.assertEqual(1, len(self.gate.output_bits))
        self.assertEqual('mNOT', self.gate.name)

    def test_evaluate(self):
        source = mocks.SourceMock('', 0, [1, 0, 0, 1])

        self.gate.add_input(source, {i: i for i in xrange(0, 4)})
        self.gate.evaluate()
        self.assertEqual([0, 1, 1, 0], self.gate.output_bits)


class TestMultiXORGate(unittest.TestCase):
    def setUp(self):
        self.gate = multigates.MultiXORGate()

    def test_constructor(self):
        self.assertEqual([None, None], self.gate._input_bits)
        self.assertEqual(1, len(self.gate.output_bits))
        self.assertEqual('mXOR', self.gate.name)

    def test_evaluate(self):
        source_true = mocks.SourceMock('', 0, [1, 1, 0, 1, 0])
        source_false = mocks.SourceMock('', 0, [0, 0, 1, 1])

        self.gate.add_input(source_true, {i: i for i in xrange(0, 5)})
        self.gate.evaluate()
        self.assertEqual([1], self.gate.output_bits)

        self.gate.disconnect_inputs()
        self.gate.add_input(source_false, {i: i for i in xrange(0, 4)})
        self.gate.evaluate()
        self.assertEqual([0], self.gate.output_bits)