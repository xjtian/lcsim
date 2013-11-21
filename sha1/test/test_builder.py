import unittest
import sys

from sha1.builder import *


def chunk_words(chunk):
    w = [-1] * 80
    for i in xrange(0, 16):
        w[i] = (chunk >> 32 * (15 - i)) & 0xFFFFFFFF
    for i in xrange(16, 80):
        w[i] = w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16]
        w[i] = ((w[i] << 1) % (1 << 32) | (w[i] >> 31))

    return w


def sha1_block(chunk):
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    w = chunk_words(chunk)

    a, b, c, d, e = h0, h1, h2, h3, h4
    f, k = None, None
    for i in xrange(0, 79):
        #print 'At iteration %d' % i
        #print 'a = %x' % a
        #print 'b = %x' % b
        #print 'c = %x' % c
        #print 'd = %x' % d
        #print 'e = %x' % e

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

        temp = ((a << 5) % (1 << 32) | a >> 27)
        temp = (temp + f) % (1 << 32)

        temp = (temp + e) % (1 << 32)
        temp = (temp + k) % (1 << 32)
        temp = (temp + w[i]) % (1 << 32)

        e = d
        d = c
        c = ((b << 30) % (1 << 32) | b >> 2)
        b = a
        a = temp

    eh0 = (h0 + a) % (1 << 32)
    eh1 = (h1 + b) % (1 << 32)
    eh2 = (h2 + c) % (1 << 32)
    eh3 = (h3 + d) % (1 << 32)
    eh4 = (h4 + e) % (1 << 32)

    return eh0, eh1, eh2, eh3, eh4


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
        eh = sha1_block(chunk)

        #Now run the same algorithm without circuits
        print 'Actual from circuit:'
        for h in nh:
            print '%x' % h

        eh = sha1_block(chunk)
        print 'Hash result from code:'
        for h in eh:
            print '%x' % h


class TestCreateWords(unittest.TestCase):
    def test_function(self):
        chunk = 0x25afbbc1415e115f68b57be44bd10a75f90d7bec20c24bfce34a1a34409b7f9373496da68e4db94e9bc60f07a9d435fe40a8c4cf41b11d5fcc09d11878d653cb
        chunk_circuit = digital_source_int_circuit(chunk, 512)

        w_circs = create_words(chunk_circuit)

        def eval_to_int(circ):
            eval = circ[0].evaluate()[circ[1][0]:circ[1][-1] + 1]
            self.assertEqual(32, len(circ[1]))

            return int(''.join(map(str, eval)), 2)

        res_words = map(eval_to_int, w_circs)
        exp_words = chunk_words(chunk)

        self.assertEqual(exp_words, res_words)
