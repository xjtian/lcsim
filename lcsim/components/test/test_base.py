from lcsim.components.test import mocks

__author__ = 'jacky'

import unittest
from lcsim.components.base import ComponentBase


class TestComponentBase(unittest.TestCase):
    def test_constructor(self):
        name = 'name'
        inputs = 1
        base = ComponentBase(name, inputs)

        self.assertEqual(name, base.name)
        self.assertEqual(inputs, len(base._input_bits))
        self.assertIsNone(base.output_bit)

    def test_add_input_single(self):
        """
        Test add_input with single-bit input and output components.
        """
        in_com = ComponentBase('', 1)
        out_com = ComponentBase('', 0)

        in_com.add_input(out_com, 0)
        self.assertIs(out_com, in_com._input_bits[0])

    def test_add_input_graph(self):
        """
        Test add_input properly puts components in children and parent lists
        (representing edges).
        """
        in_com = ComponentBase('', 1, 0)
        out_com = ComponentBase('', 0, 1)

        in_com.add_input(out_com, 0)
        self.assertIn(out_com, in_com.parents)
        self.assertIn(in_com, out_com.children)

        self.assertEqual(1, len(in_com.parents))
        self.assertEqual(1, len(out_com.children))

    def test_add_input_multicom(self):
        """
        Test add_input with multiple devices wired to one.
        """
        in_com = ComponentBase('', 5)
        out_coms = [ComponentBase('', 0), ComponentBase('', 0), ComponentBase('', 0),
                    ComponentBase('', 0), ComponentBase('', 0)]

        for i in xrange(0, len(out_coms)):
            in_com.add_input(out_coms[i], i)

        for i in xrange(0, len(out_coms)):
            self.assertIs(out_coms[i], in_com._input_bits[i])

    def test_add_input_failures(self):
        """
        Test add_input catches invalid operations properly.
        """
        in_com = ComponentBase('', 5)
        out_com1 = ComponentBase('', 0)
        out_com2 = ComponentBase('', 0)

        # Input bit out of range
        self.assertRaises(ValueError, in_com.add_input, out_com2, 5)
        self.assertRaises(ValueError, in_com.add_input, out_com2, -1)

        # Wiring to occupied input bit
        in_com.add_input(out_com1, 1)
        self.assertRaises(ValueError, in_com.add_input, out_com2, 1)

    def test_evaluate_inputs(self):
        """
        Test evaluate_inputs method.
        """
        in_com = ComponentBase('', 2)
        out_com1 = mocks.ComponentMockZero('', 0)
        out_com2 = mocks.ComponentMockOne('', 0)

        self.add_input_alias(in_com, out_com1, 0)
        self.add_input_alias(in_com, out_com2, 1)

        self.assertEqual([0, 1], in_com.evaluate_inputs())

    def test_remove_input(self):
        """
        Test the _remove_input helper method.
        """
        in_com = ComponentBase('', 1, 0)
        out_com = ComponentBase('', 0, 1)

        self.add_input_alias(in_com, out_com, 0)

        in_com._remove_input(out_com)
        self.assertNotIn(in_com, out_com.children)
        self.assertNotIn(out_com, in_com.parents)

        self.assertIsNone(in_com._input_bits[0])

    def test_disconnect_inputs(self):
        """
        Test the disconnect_inputs method.
        """
        in_com = ComponentBase('', 2)
        out_com1 = ComponentBase('', 0)
        out_com2 = ComponentBase('', 0)

        self.add_input_alias(in_com, out_com1, 0)
        self.add_input_alias(in_com, out_com2, 1)

        in_com.disconnect_inputs()
        self.assertEquals([None, None], in_com._input_bits)
        self.assertNotIn(in_com, out_com1.children)
        self.assertNotIn(in_com, out_com2.children)

        self.assertNotIn(out_com1, in_com.parents)
        self.assertNotIn(out_com2, in_com.parents)

    def test_disconnect_outputs(self):
        in_com1 = ComponentBase('', 1)
        in_com2 = ComponentBase('', 1)
        out_com = ComponentBase('', 0)

        self.add_input_alias(in_com1, out_com, 0)
        self.add_input_alias(in_com2, out_com, 0)

        out_com.disconnect_outputs()

        self.assertIsNone(out_com.output_bit)

        self.assertEqual(0, len(out_com.children))
        self.assertEqual(0, len(in_com1.parents))
        self.assertEqual(0, len(in_com2.parents))

        self.assertEqual([None], in_com1._input_bits)
        self.assertEqual([None], in_com2._input_bits)

    def add_input_alias(self, in_com, out_com, index):
        """
        Alters state of components like add_input should without depending on
        the method itself.
        """
        in_com._input_bits[index] = out_com
        in_com.parents.add(out_com)
        out_com.children.add(in_com)
