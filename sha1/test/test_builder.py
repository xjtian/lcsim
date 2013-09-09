__author__ = 'jacky'

import unittest
from sha1 import builder


class TestConstants(unittest.TestCase):
    def test_h0(self):
        result = builder.h0()

        self.assertEqual([0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1,
                          0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
                         result.evaluate())

    def test_h1(self):
        result = builder.h1()

        self.assertEqual([1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1,
                          1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1],
                         result.evaluate())

    def test_h2(self):
        result = builder.h2()

        self.assertEqual([1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0,
                          1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                         result.evaluate())

    def test_h3(self):
        result = builder.h3()

        self.assertEqual([0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0,
                          0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0],
                         result.evaluate())

    def test_h4(self):
        result = builder.h4()

        self.assertEqual([1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0,
                          1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                         result.evaluate())
