__author__ = 'jacky'

import unittest
from circuits.components import ComponentBase


class TestComponentBase(unittest.TestCase):
    def test_constructor(self):
        name = 'name'
        inputs = 1
        outputs = 2
        base = ComponentBase(name, inputs, outputs)

        self.assertEqual(name, base.name)
        self.assertEqual(outputs, len(base._output_bits))
        self.assertEqual(inputs, len(base._input_bits))

    def test_add_input_single(self):
        """
        Test add_input with single-bit input and output components.
        """
        in_com = ComponentBase('', 1, 0)
        out_com = ComponentBase('', 0, 1)

        in_com.add_input(out_com, {0: 0})
        self.assertEqual(0, in_com._input_bits[0][1])
        self.assertIs(out_com, in_com._input_bits[0][0])

        self.assert_(out_com._output_bits[0][1])

    def test_add_input_graph(self):
        """
        Test add_input properly puts components in children and parent lists (representing edges).
        """
        in_com = ComponentBase('', 1, 0)
        out_com = ComponentBase('', 0, 1)

        in_com.add_input(out_com, {0: 0})
        self.assertIn(out_com, in_com.parents)
        self.assertIn(in_com, out_com.children)

        self.assertEqual(1, len(in_com.parents))
        self.assertEqual(1, len(out_com.children))

    def test_add_input_multiple(self):
        """
        Test add_input with multi-bit input and output components.
        """
        in_com = ComponentBase('', 5, 0)
        out_com = ComponentBase('', 0, 5)

        # TODO: incomplete

    def test_remove_input(self):
        self.fail('Not implemented yet.')

    def test_disconnect_inputs(self):
        self.fail('Not implemented yet.')

    def test_disconnect_outputs(self):
        self.fail('Not implemented yet.')
