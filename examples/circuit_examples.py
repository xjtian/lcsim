__author__ = 'jacky'

from circuits import sources, shifters, adders, bitwise, circuit


def readme_example():
    """
    Code example from the README. ((A+B) leftrotate 2) xor C, 4-bit inputs.
    """
    plus = adders.ripple_adder_no_carry(4)
    shifters.left_rotate_in_place(plus, 2)
    xor = bitwise.bitwise_xor_circuit(4)

    circuit.connect_circuits(plus, xor, {0: 0, 1: 1, 2: 2, 3: 3})

    inputs = sources.digital_source_circuit([0, 1, 0, 1, 1, 1, 0, 1])
    c = sources.digital_source_circuit([0, 1, 1, 0])

    circuit.connect_circuits(inputs, plus, {i: i for i in xrange(0, 8)})
    circuit.connect_circuits(c, xor, {0: 4, 1: 5, 2: 6, 3: 7})

    combined_sources = circuit.stack_circuits('src', inputs, c)
    op = circuit.merge_circuits('ex', combined_sources, xor)

    print 'Result of operation: ', ''.join(map(str, op.evaluate()))


def simple_calculator(a, b):
    """
    Simple calculator that adds 32-bit unsigned integers.
    """
    plus = adders.ripple_adder_no_carry(32)
    a_bits = map(int, bin(a)[2:])
    while len(a_bits) < 32:
        a_bits.insert(0, 0)

    b_bits = map(int, bin(b)[2:])
    while len(b_bits) < 32:
        b_bits.insert(0, 0)

    inputs = sources.digital_source_circuit(a_bits + b_bits)

    circuit.connect_circuits(inputs, plus, {i: i for i in xrange(0, 64)})
    calc_circuit = circuit.merge_circuits('calc', inputs, plus)

    return calc_circuit.evaluate()


def main():
    readme_example()
    result = simple_calculator(8345, 143)
    print '32-bit unsigned result of addition: ', ''.join(map(str, result))
    print 'Decimal equivalent: ', int(''.join(map(str, result)), 2)


if __name__ == '__main__':
    main()
