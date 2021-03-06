from lcsim.components import base, gates
from lcsim.components.test import mocks

__author__ = 'jacky'

import unittest


class TestLogicGateBase(unittest.TestCase):
    def test_evaluate(self):
        """
        Make sure that the base evaluate() method throws an exception when
        inputs aren't full and doesn't when they are.
        """
        gate = gates.LogicGateBase('Test', 2)
        self.assertRaises(base.MissingInputException, gate.evaluate)

        output_gate = gates.LogicGateBase('Test2', 0)
        gate.add_input(output_gate, 0)
        self.assertRaises(base.MissingInputException, gate.evaluate)

        output_gate2 = gates.LogicGateBase('Test3', 0)
        gate.add_input(output_gate2, 1)

        gate.evaluate()


def input_11(gate):
    """
    Connect mocked components to gate so input will be 11.

    :type gate ComponentBase
    """
    ones = [mocks.ComponentMockOne('', 0), mocks.ComponentMockOne('', 0)]

    gate.add_input(ones[0], 0)
    gate.add_input(ones[1], 1)


def input_10(gate):
    """
    Connect mocked components to gate so input will be 10.

    :type gate ComponentBase
    """
    one = mocks.ComponentMockOne('', 0)
    zero = mocks.ComponentMockZero('', 0)

    gate.add_input(one, 0)
    gate.add_input(zero, 1)


def input_01(gate):
    """
    Connect mocked components to gate so input will be 01.

    :type gate ComponentBase
    """
    one = mocks.ComponentMockOne('', 0)
    zero = mocks.ComponentMockZero('', 0)

    gate.add_input(one, 1)
    gate.add_input(zero, 0)


def input_00(gate):
    """
    Connect mocked components to gate so input will be 00.
    """
    zeros = [mocks.ComponentMockZero('', 0), mocks.ComponentMockZero('', 0)]
    gate.add_input(zeros[0], 0)
    gate.add_input(zeros[1], 1)


class LogicGateTestCasesBase(unittest.TestCase):
    """
    Base TestCase for the two-input logic gates (everything except NOT). Client
    classes override setUp to specify the type of gate to test and the list
    of expected results.
    """

    def setUp(self):
        self.gate = None
        self.expected = [None] * 4

    def test_constructor(self):
        """
        Test the gate constructor.
        """
        pass

    def test_evaluate_11(self):
        """
        Evaluate with input set to 11.
        """
        if not self.gate:
            return
        input_11(self.gate)
        self.gate.evaluate()
        self.assertEqual(self.expected[0], self.gate.output_bit)

    def test_evaluate_10(self):
        """
        Evaluate with input set to 10.
        """
        if not self.gate:
            return
        input_10(self.gate)
        self.gate.evaluate()

        self.assertEqual(self.expected[1], self.gate.output_bit)

    def test_evaluate_01(self):
        """
        Evaluate with input set to 01.
        """
        if not self.gate:
            return
        input_01(self.gate)
        self.gate.evaluate()

        self.assertEqual(self.expected[2], self.gate.output_bit)

    def test_evaluate_00(self):
        """
        Evaluate with input set to 00.
        """
        if not self.gate:
            return
        input_00(self.gate)
        self.gate.evaluate()

        self.assertEqual(self.expected[3], self.gate.output_bit)


class TestANDGate(LogicGateTestCasesBase):
    def setUp(self):
        self.gate = gates.ANDGate()
        self.expected = [1, 0, 0, 0]

    def test_constructor(self):
        self.assertEqual('AND', self.gate.name)
        self.assertEqual(2, len(self.gate._input_bits))


class TestORGate(LogicGateTestCasesBase):
    def setUp(self):
        self.gate = gates.ORGate()
        self.expected = [1, 1, 1, 0]

    def test_constructor(self):
        self.assertEqual('OR', self.gate.name)
        self.assertEqual(2, len(self.gate._input_bits))


class TestXORGate(LogicGateTestCasesBase):
    def setUp(self):
        self.gate = gates.XORGate()
        self.expected = [0, 1, 1, 0]

    def test_constructor(self):
        self.assertEqual('XOR', self.gate.name)
        self.assertEqual(2, len(self.gate._input_bits))


class TestNANDGate(LogicGateTestCasesBase):
    def setUp(self):
        self.gate = gates.NANDGate()
        self.expected = [0, 1, 1, 1]

    def test_constructor(self):
        self.assertEqual('NAND', self.gate.name)
        self.assertEqual(2, len(self.gate._input_bits))


class TestNORGate(LogicGateTestCasesBase):
    def setUp(self):
        self.gate = gates.NORGate()
        self.expected = [0, 0, 0, 1]

    def test_constructor(self):
        self.assertEqual('NOR', self.gate.name)
        self.assertEqual(2, len(self.gate._input_bits))


class TestXNORGate(LogicGateTestCasesBase):
    def setUp(self):
        self.gate = gates.XNORGate()
        self.expected = [1, 0, 0, 1]

    def test_constructor(self):
        self.assertEqual('XNOR', self.gate.name)
        self.assertEqual(2, len(self.gate._input_bits))


class TestNotGate(unittest.TestCase):
    def setUp(self):
        self.zero = mocks.ComponentMockZero('', 0)
        self.one = mocks.ComponentMockOne('', 0)
        self.gate = gates.NOTGate()

    def test_constructor(self):
        self.assertEqual('NOT', self.gate.name)
        self.assertEqual(1, len(self.gate._input_bits))

    def test_evaluate_1(self):
        self.gate.add_input(self.one, 0)
        self.gate.evaluate()
        self.assertEqual(0, self.gate.output_bit)

    def test_evaluate_0(self):
        self.gate.add_input(self.zero, 0)
        self.gate.evaluate()
        self.assertEqual(1, self.gate.output_bit)
