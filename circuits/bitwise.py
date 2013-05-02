__author__ = 'Jacky'

from circuits import circuit
from components import gates


def bitwise_and_circuit(bits):
    """
    Create a circuit to compute the bitwise AND of two equal-sized inputs.
    When using the circuit, stack the inputs on top of each other. E.g. for
    a 4-bit circuit, the input space would be A0-A1-A2-A3-B0-B1-B2-B3.

    Parameters:
        bits:
            The number of bits expected for each input argument. The size of
            the input space of the circuit is 2*bits and the sie of the
            output space is bits.

    Returns:
        Bitwise AND circuit for 2 inputs of the specified size.

    Example usage:
        >>> from components import sources
        >>> from circuits import circuit
        >>> s1 = sources.DigitalArbitrary([0, 1, 1, 0])
        >>> s2 = sources.DigitalArbitrary([0, 1, 0, 1])
        >>> c1 = circuit.Circuit('in1', 0, 4)
        >>> c2 = circuit.Circuit('in2', 0, 4)
        >>> c1.add_output_component(s1, {0: 0, 1: 1, 2: 2, 3: 3})
        >>> c2.add_output_component(s2, {0: 0, 1: 1, 2: 2, 3: 3})
        >>> and_c = bitwise_and_circuit(4)
        >>> circuit.connect_circuits(c1, and_c, {i: i for i in xrange(0, 4)})
        >>> circuit.connect_circuits(c2, and_c, {0: 4, 1: 5, 2: 6, 3: 7})
        >>> and_c.evaluate()
        [0, 1, 0, 0]
    """
    result = circuit.Circuit('bAND', 2*bits, bits)
    comps = [gates.ANDGate() for _ in xrange(0, bits)]

    for i in xrange(0, bits):
        result.add_input_component(comps[i], {i: 0})
        result.add_input_component(comps[i], {i + bits: 1})

        result.add_output_component(comps[i], {i: 0})

    return result
