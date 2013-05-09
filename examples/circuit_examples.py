__author__ = 'jacky'

from circuits import sources, shifters, adders, bitwise, circuit


def readme_example():
    plus = adders.ripple_adder_no_carry(4)
    shifters.left_rotate(plus, 2)
    xor = bitwise.bitwise_xor_circuit(4)

    circuit.connect_circuits(plus, xor, {0: 0, 1: 1, 2: 2, 3: 3})

    inputs = sources.digital_source_circuit([0, 1, 0, 1, 1, 1, 0, 1])
    c = sources.digital_source_circuit([0, 1, 1, 0])

    circuit.connect_circuits(inputs, plus, {i: i for i in xrange(0, 8)})
    circuit.connect_circuits(c, xor, {0: 4, 1: 5, 2: 6, 3: 7})

    combined_sources = circuit.stack_circuits('src', inputs, c)
    op = circuit.merge_circuits('ex', combined_sources, xor)

    print op.evaluate()


def main():
    readme_example()


if __name__ == '__main__':
    main()
