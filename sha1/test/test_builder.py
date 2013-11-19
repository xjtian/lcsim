import unittest
import sys

from circuits.sources import digital_source_int_circuit
from sha1.builder import block_operation


class TestBlockOperation(unittest.TestCase):
    def test_function(self):
        sys.setrecursionlimit(10000)
        # Each chunk is 512 bits
        # From random.org
        chunk = 0x25afbbc1415e115f68b57be44bd10a75f90d7bec20c24bfce34a1a34409b7f9373496da68e4db94e9bc60f07a9d435fe40a8c4cf41b11d5fcc09d11878d653cb

        chunk_circuit = digital_source_int_circuit(chunk, 512)
        ch0 = digital_source_int_circuit(0x67452301, 32)
        ch1 = digital_source_int_circuit(0xEFCDAB89, 32)
        ch2 = digital_source_int_circuit(0x98BADCFE, 32)
        ch3 = digital_source_int_circuit(0x10325476, 32)
        ch4 = digital_source_int_circuit(0xC3D2E1F0, 32)

        result = block_operation(chunk_circuit, ch0, ch1, ch2, ch3, ch4)

        def eval_to_int(nh):
            eval = nh.evaluate()

            return int(''.join(map(str, eval)), 2)

        nh = map(eval_to_int, result)

        # Now run the same algorithm without circuits
        h0 = 0x67452301
        h1 = 0xEFCDAB89
        h2 = 0x98BADCFE
        h3 = 0x10325476
        h4 = 0xC3D2E1F0

        # Split into words
        w = [-1] * 80
        for i in xrange(15, -1, -1):
            w[15 - i] = ((chunk >> (i * 32))) & 0xFFFFFFFF

        a, b, c, d, e = h0, h1, h2, h3, h4
        for i in xrange(0, 79):
            if 0 <= i <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            elif 60 <= i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = ((a << 5 | a >> 27) + f) % 0xFFFFFFFF
            temp = (temp + e) % 0xFFFFFFFF
            temp = (temp + k) % 0xFFFFFFFF
            temp = (temp + w[i]) % 0xFFFFFFFF

            e = d
            d = c
            c = (b << 32 | b >> 2)
            b = a
            a = temp

        eh0 = (h0 + a) % 0xFFFFFFFF
        eh1 = (h1 + b) % 0xFFFFFFFF
        eh2 = (h2 + c) % 0xFFFFFFFF
        eh3 = (h3 + d) % 0xFFFFFFFF
        eh4 = (h4 + e) % 0xFFFFFFFF

        print 'Actual from circuit:'
        for h in nh:
            print '%x' % h

        print 'From pseudocode:'
        for h in [eh0, eh1, eh2, eh3, eh4]:
            print '%x' % h
