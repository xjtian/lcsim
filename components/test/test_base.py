__author__ = 'jacky'

import unittest
from components.base import ComponentBase


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

    def test_add_input_multibit(self):
        """
        Test add_input with two multi-bit input and output components.
        """
        in_com = ComponentBase('', 5, 0)
        out_com = ComponentBase('', 0, 5)
        mapping = {0: 4, 1: 2, 2: 3, 3: 0, 4: 1}

        in_com.add_input(out_com, mapping)
        self.add_input_helper(in_com, out_com, mapping)

    def test_add_input_multicom(self):
        """
        Test add_input with multiple devices wired to one.
        """
        in_com = ComponentBase('', 5, 0)
        out_com1 = ComponentBase('', 0, 2)
        out_com2 = ComponentBase('', 0, 3)

        mapping1 = {0: 4, 1: 2}
        mapping2 = {0: 3, 1: 0, 2: 1}

        in_com.add_input(out_com1, mapping1)
        in_com.add_input(out_com2, mapping2)

        self.add_input_helper(in_com, out_com1, mapping1)
        self.add_input_helper(in_com, out_com2, mapping2)

    def test_add_input_failures(self):
        """
        Test add_input catches invalid operations properly.
        """
        in_com = ComponentBase('', 5, 0)
        out_com1 = ComponentBase('', 0, 2)
        out_com2 = ComponentBase('', 0, 3)

        # Output bit out of range
        self.assertRaises(ValueError, in_com.add_input, out_com1, {3: 0})
        self.assertRaises(ValueError, in_com.add_input, out_com1, {-1: 0})
        # Input bit out of range
        self.assertRaises(ValueError, in_com.add_input, out_com2, {2: 5})
        self.assertRaises(ValueError, in_com.add_input, out_com2, {2: -1})

        # Wiring to occupied input bit
        in_com.add_input(out_com1, {0: 1})
        self.assertRaises(ValueError, in_com.add_input, out_com2, {0: 1})

        # Wiring from occupied output bit
        self.assertRaises(ValueError, in_com.add_input, out_com1, {0: 2})

    def add_input_helper(self, in_com, out_com, mapping):
        """
        Helper method for add_input tests.
        """
        for k, v in mapping.items():
            self.assertEqual(k, in_com._input_bits[v][1])
            self.assertIs(out_com, in_com._input_bits[v][0])

            self.assert_(out_com._output_bits[k][1])

        self.assertIn(out_com, in_com.parents)
        self.assertIn(in_com, out_com.children)

    def test_evaluate_inputs(self):
        """
        Test evaluate_inputs method.
        """
        in_com = ComponentBase('', 2, 0)
        out_com1 = ComponentBase('', 0, 1)
        out_com2 = ComponentBase('', 0, 1)

        self.add_input_alias(in_com, out_com1, {0: 0})
        self.add_input_alias(in_com, out_com2, {0: 1})

        out_com2._output_bits[0][0] = 1

        self.assertEqual([-1, 1], in_com.evaluate_inputs())

    def test_remove_input(self):
        """
        Test the _remove_input helper method.
        """
        in_com = ComponentBase('', 1, 0)
        out_com = ComponentBase('', 0, 1)

        self.add_input_alias(in_com, out_com, {0: 0})

        in_com._remove_input(out_com)
        self.assertNotIn(in_com, out_com.children)
        self.assertNotIn(out_com, in_com.parents)

        self.assertIsNone(in_com._input_bits[0])
        self.assert_(not out_com._output_bits[0][1])

    def test_disconnect_inputs(self):
        """
        Test the disconnect_inputs method.
        """
        in_com = ComponentBase('', 2, 0)
        out_com1 = ComponentBase('', 0, 1)
        out_com2 = ComponentBase('', 0, 1)

        self.add_input_alias(in_com, out_com1, {0: 0})
        self.add_input_alias(in_com, out_com2, {0: 1})

        in_com.disconnect_inputs()
        self.assertEquals([None, None], in_com._input_bits)
        self.assertNotIn(in_com, out_com1.children)
        self.assertNotIn(in_com, out_com2.children)

        self.assertNotIn(out_com1, in_com.parents)
        self.assertNotIn(out_com2, in_com.parents)

        self.assert_(not out_com1._output_bits[0][1])
        self.assert_(not out_com2._output_bits[0][1])

    def test_disconnect_outputs(self):
        self.fail('Not implemented yet.')

    def add_input_alias(self, in_com, out_com, mapping):
        """
        Alters state of components like add_input should without depending on the method itself.
        """
        for k, v in mapping.items():
            in_com._input_bits[v] = (out_com, k)
            out_com._output_bits[k][1] = True

        in_com.parents.append(out_com)
        out_com.children.append(in_com)
