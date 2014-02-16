from itertools import izip

from lcsim.circuits.bitwise import bitwise_or_circuit, bitwise_and_circuit, bitwise_not_circuit, bitwise_xor_circuit
from lcsim.circuits.circuit import connect_circuits, stack_circuits
from lcsim.circuits.sources import digital_source_int_circuit
from lcsim.circuits.adders import ripple_adder_no_carry
from lcsim.circuits.shifters import left_rotate


def sha1(message, rounds=80):
    """
    Runs the sha-1 block operation on a 512-bit message/chunk.
    """
    # Initial constants
    a = digital_source_int_circuit(0x67452301, 32)
    b = digital_source_int_circuit(0xEFCDAB89, 32)
    c = digital_source_int_circuit(0x98BADCFE, 32)
    d = digital_source_int_circuit(0x10325476, 32)
    e = digital_source_int_circuit(0xC3D2E1F0, 32)

    h0, h1, h2, h3, h4 = block_operation(message, a, b, c, d, e, rounds)

    # Concatenate results
    h01 = stack_circuits('h01', h0, h1)
    h012 = stack_circuits('h012', h01, h2)
    h0123 = stack_circuits('h0123', h012, h3)
    h = stack_circuits('H', h0123, h4)

    result = int(''.join(map(str, h.evaluate())), 2)
    return result, h


def block_operation(chunk, h0, h1, h2, h3, h4, rounds=80):
    """
    Returns (h0, h1, h2, h3, h4), the h-constants that result from running
    the SHA-1 algorithm on one block.
    """

    a, b, c, d, e = h0, h1, h2, h3, h4

    w = create_words(chunk, rounds)

    # Main loop here
    for i in xrange(0, rounds):
        if 0 <= i <= 19:
            # f = (b and c) or ((not b) and d)
            b_and_c = bitwise_and_circuit(32)
            connect_circuits(b, b_and_c, {x: x for x in xrange(0, 32)})
            connect_circuits(c, b_and_c, {x: x + 32 for x in xrange(0, 32)})

            not_b = bitwise_not_circuit(32)
            connect_circuits(b, not_b, {x: x for x in xrange(0, 32)})

            not_b_and_d = bitwise_and_circuit(32)
            connect_circuits(not_b, not_b_and_d, {x: x for x in xrange(0, 32)})
            connect_circuits(d, not_b_and_d, {x: x + 32 for x in xrange(0, 32)})

            f = bitwise_or_circuit(32)
            connect_circuits(b_and_c, f, {x: x for x in xrange(0, 32)})
            connect_circuits(not_b_and_d, f, {x: x + 32 for x in xrange(0, 32)})

            k = digital_source_int_circuit(0x5A827999, 32)
        elif 20 <= i <= 39:
            # f = b xor c xor d
            b_xor_c = bitwise_xor_circuit(32)
            connect_circuits(b, b_xor_c, {x: x for x in xrange(0, 32)})
            connect_circuits(c, b_xor_c, {x: x + 32 for x in xrange(0, 32)})

            f = bitwise_xor_circuit(32)
            connect_circuits(b_xor_c, f, {x: x for x in xrange(0, 32)})
            connect_circuits(d, f, {x: x + 32 for x in xrange(0, 32)})

            k = digital_source_int_circuit(0x6ED9EBA1, 32)
        elif 40 <= i <= 59:
            # f = (b and c) or (b and d) or (c and d)
            b_and_c = bitwise_and_circuit(32)
            connect_circuits(b, b_and_c, {x: x for x in xrange(0, 32)})
            connect_circuits(c, b_and_c, {x: x + 32 for x in xrange(0, 32)})

            b_and_d = bitwise_and_circuit(32)
            connect_circuits(b, b_and_d, {x: x for x in xrange(0, 32)})
            connect_circuits(d, b_and_d, {x: x + 32 for x in xrange(0, 32)})

            c_and_d = bitwise_and_circuit(32)
            connect_circuits(c, c_and_d, {x: x for x in xrange(0, 32)})
            connect_circuits(d, c_and_d, {x: x + 32 for x in xrange(0, 32)})

            bnc_or_bnd = bitwise_or_circuit(32)
            connect_circuits(b_and_c, bnc_or_bnd, {x: x for x in xrange(0, 32)})
            connect_circuits(b_and_d, bnc_or_bnd, {x: x + 32 for x in xrange(0, 32)})

            f = bitwise_or_circuit(32)
            connect_circuits(bnc_or_bnd, f, {x: x for x in xrange(0, 32)})
            connect_circuits(c_and_d, f, {x: x + 32 for x in xrange(0, 32)})

            k = digital_source_int_circuit(0x8F1BBCDC, 32)
        elif 60 <= i <= 79:
            # f = b xor c xor d
            b_xor_c = bitwise_xor_circuit(32)
            connect_circuits(b, b_xor_c, {x: x for x in xrange(0, 32)})
            connect_circuits(c, b_xor_c, {x: x + 32 for x in xrange(0, 32)})

            f = bitwise_xor_circuit(32)
            connect_circuits(b_xor_c, f, {x: x for x in xrange(0, 32)})
            connect_circuits(d, f, {x: x + 32 for x in xrange(0, 32)})

            k = digital_source_int_circuit(0xCA62C1D6, 32)
        else:
            raise Exception("Invalid word index in main loop!")

        # (a leftrotate 5) + f
        temp = ripple_adder_no_carry(32)
        connect_circuits(a, temp, {x: x - 5 for x in xrange(5, 32)})
        connect_circuits(a, temp, {x: x + 27 for x in xrange(0, 5)})
        connect_circuits(f, temp, {x: x + 32 for x in xrange(0, 32)})

        # result + e
        temp2 = ripple_adder_no_carry(32)
        connect_circuits(temp, temp2, {x: x for x in xrange(0, 32)})
        connect_circuits(e, temp2, {x: x + 32 for x in xrange(0, 32)})

        # result + k
        temp = ripple_adder_no_carry(32)
        connect_circuits(temp2, temp, {x: x for x in xrange(0, 32)})
        connect_circuits(k, temp, {x: x + 32 for x in xrange(0, 32)})

        # result + w[i]
        temp2 = ripple_adder_no_carry(32)
        connect_circuits(temp, temp2, {x: x for x in xrange(0, 32)})
        connect_circuits(w[i][0], temp2, {x: y for (x, y) in izip(w[i][1], xrange(32, 64))})

        # temp = (a leftrotate 5) + f + e + k + w[i]
        temp = temp2

        e = d
        d = c
        c = left_rotate(b, 30)
        b = a
        a = temp

    h0_add = ripple_adder_no_carry(32)
    connect_circuits(h0, h0_add, {i: i for i in xrange(0, 32)})
    connect_circuits(a, h0_add, {i: i + 32 for i in xrange(0, 32)})

    h1_add = ripple_adder_no_carry(32)
    connect_circuits(h1, h1_add, {i: i for i in xrange(0, 32)})
    connect_circuits(b, h1_add, {i: i + 32 for i in xrange(0, 32)})

    h2_add = ripple_adder_no_carry(32)
    connect_circuits(h2, h2_add, {i: i for i in xrange(0, 32)})
    connect_circuits(c, h2_add, {i: i + 32 for i in xrange(0, 32)})

    h3_add = ripple_adder_no_carry(32)
    connect_circuits(h3, h3_add, {i: i for i in xrange(0, 32)})
    connect_circuits(d, h3_add, {i: i + 32 for i in xrange(0, 32)})

    h4_add = ripple_adder_no_carry(32)
    connect_circuits(h4, h4_add, {i: i for i in xrange(0, 32)})
    connect_circuits(e, h4_add, {i: i + 32 for i in xrange(0, 32)})

    return h0_add, h1_add, h2_add, h3_add, h4_add


def create_words(chunk, rounds=80):
    w = [None] * rounds

    for i in xrange(0, min(rounds, 16)):
        w[i] = (chunk, xrange(i * 32, i * 32 + 32))

    for i in xrange(16, min(rounds, 80)):
        # w[i] = (w[i-3] xor w[i-8] xor w[i-14] xor w[i-16]) leftrotate 1
        xtemp = bitwise_xor_circuit(32)

        connect_circuits(w[i - 3][0], xtemp, {
            x: y for (x, y) in izip(w[i - 3][1], xrange(0, 32))
        })

        connect_circuits(w[i - 8][0], xtemp, {
            x: y for (x, y) in izip(w[i - 8][1], xrange(32, 64))
        })

        # result xor w[i - 14]
        xtemp2 = bitwise_xor_circuit(32)
        connect_circuits(xtemp, xtemp2, {x: x for x in xrange(0, 32)})
        connect_circuits(w[i - 14][0], xtemp2, {
            x: y for (x, y) in izip(w[i - 14][1], xrange(32, 64))
        })

        # result xor w[i - 16]
        xtemp = bitwise_xor_circuit(32)
        connect_circuits(xtemp2, xtemp, {x: x for x in xrange(0, 32)})
        connect_circuits(w[i - 16][0], xtemp, {
            x: y for (x, y) in izip(w[i - 16][1], xrange(32, 64))
        })

        # leftrotate 1
        word = left_rotate(xtemp, 1)
        w[i] = (word, xrange(0, 32))

    return w