from lcsim.circuits import circuit, sources, adders

__author__ = 'Jacky'

import unittest
import itertools


class TestFullAdder(unittest.TestCase):
    def test_function(self):
        # Test for all inputs
        it = itertools.product([0, 1], [0, 1], [0, 1])

        for x in it:
            src = sources.digital_source_circuit(x)

            a = adders.full_adder_circuit()
            circuit.connect_circuits(src, a, {0: 0, 1: 1, 2: 2})

            num = int(''.join(map(str, a.evaluate())), 2)
            self.assertEqual(sum(x), num)


class TestRippleAdderNoCarry(unittest.TestCase):
    def test_function(self):
        # Test for all inputs up to 8 bits
        for l in xrange(2, 9):
            space = [[0, 1] for _ in xrange(0, l)]

            it1 = itertools.product(*space)
            it2 = itertools.product(*space)

            for x in it1:
                for y in it2:
                    n1 = int(''.join(map(str, x)), 2)
                    n2 = int(''.join(map(str, y)), 2)
                    mapping = {i: i for i in xrange(0, 2 * l)}

                    src = sources.digital_source_circuit(x + y)

                    a = adders.ripple_adder_no_carry(l)
                    circuit.connect_circuits(src, a, mapping)

                    num = int(''.join(map(str, a.evaluate())), 2)
                    self.assertEqual('%dAdd' % l, a.name)
                    self.assertEqual((n1 + n2) % (2 ** l), num)

    def test_specific(self):
        a = 0xe8a4602c
        b = 0x98badcfe

        al = map(int, list(bin(a)[2:]))
        bl = map(int, list(bin(b)[2:]))

        while len(al) < 32:
            al.insert(0, 0)
        while len(bl) < 32:
            bl.insert(0, 0)

        src = sources.digital_source_circuit(al + bl)

        adder = adders.ripple_adder_no_carry(32)
        circuit.connect_circuits(src, adder, {i: i for i in xrange(0, 64)})

        num = int(''.join(map(str, adder.evaluate())), 2)
        self.assertEqual((a + b) % (1 << 32), num)
