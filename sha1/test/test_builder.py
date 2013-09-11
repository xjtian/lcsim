__author__ = 'jacky'

import unittest
from sha1 import builder


class TestConstants(unittest.TestCase):
    def setUp(self):
        self.h0 = 0x67452301
        self.h1 = 0xEFCDAB89
        self.h2 = 0x98BADCFE
        self.h3 = 0x10325476
        self.h4 = 0xC3D2E1F0

    def test_h0(self):
        self.assertEqual([0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1,
                          0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
                         builder.h0.evaluate())

    def test_h1(self):
        self.assertEqual([1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1,
                          1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1],
                         builder.h1.evaluate())

    def test_h2(self):
        self.assertEqual([1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0,
                          1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                         builder.h2.evaluate())

    def test_h3(self):
        self.assertEqual([0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0,
                          0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0],
                         builder.h3.evaluate())

    def test_h4(self):
        self.assertEqual([1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0,
                          1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                         builder.h4.evaluate())

    def test_f_first_quarter(self):
        f = builder.f_first_quarter()
        result = int(''.join(map(str, f.evaluate())), 2)

        expected = (self.h1 & self.h2) | ((~ self.h1) & self.h3)
        self.assertEqual(expected, result)
