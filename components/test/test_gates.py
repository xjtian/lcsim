__author__ = 'jacky'

import unittest
from components import gates, base


class TestLogicGateBase(unittest.TestCase):
    def test_evaluate(self):
        gate = gates.LogicGateBase('Test', 2, 1)
        self.assertRaises(base.MissingInputException, gate.evaluate)

        output_gate = gates.LogicGateBase('Test2', 0, 1)
        gate.add_input(output_gate, {0: 0})
        self.assertRaises(base.MissingInputException, gate.evaluate)

        output_gate2 = gates.LogicGateBase('Test3', 0, 1)
        gate.add_input(output_gate2, {0: 1})

        gate.evaluate()
