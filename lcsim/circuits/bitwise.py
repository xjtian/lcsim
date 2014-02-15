from lcsim.circuits import circuit
from lcsim.components import gates

__author__ = 'Jacky'


def bitwise_and_circuit(bits):
    """
    Create a circuit to compute the bitwise AND of two equal-sized inputs.
    When using the circuit, stack the inputs on top of each other. E.g. for
    a 4-bit circuit, the input space would be A0-A1-A2-A3-B0-B1-B2-B3.

    Parameters:
        bits:
            The number of bits expected for each input argument. The size of
            the input space of the circuit is 2*bits and the size of the
            output space is bits.

    Returns:
        Bitwise AND circuit for 2 inputs of the specified size.
    """
    result = circuit.Circuit('bAND', 2*bits, bits)
    comps = [gates.ANDGate() for _ in xrange(0, bits)]

    for i in xrange(0, bits):
        result.add_input_component(comps[i], {i: 0})
        result.add_input_component(comps[i], {i + bits: 1})

        result.add_output_component(comps[i], i)

    return result


def bitwise_or_circuit(bits):
    """
    Create a circuit to compute the bitwise OR of two equal-sized inputs.
    When using the circuit, stack the inputs on top of each other. E.g. for
    a 4-bit circuit, the input space would be A0-A1-A2-A3-B0-B1-B2-B3.

    Parameters:
        bits:
            The number of bits expected for each input argument. The size of
            the input space of the circuit is 2*bits and the size of the
            output space is bits.

    Returns:
        Bitwise OR circuit for 2 inputs of the specified size.
    """
    result = circuit.Circuit('bOR', 2*bits, bits)
    comps = [gates.ORGate() for _ in xrange(0, bits)]

    for i in xrange(0, bits):
        result.add_input_component(comps[i], {i: 0})
        result.add_input_component(comps[i], {i + bits: 1})

        result.add_output_component(comps[i], i)

    return result


def bitwise_xor_circuit(bits):
    """
    Create a circuit to compute the bitwise XOR of two equal-sized inputs.
    When using the circuit, stack the inputs on top of each other. E.g. for
    a 4-bit circuit, the input space would be A0-A1-A2-A3-B0-B1-B2-B3.

    Parameters:
        bits:
            The number of bits expected for each input argument. The size of
            the input space of the circuit is 2*bits and the size of the
            output space is bits.

    Returns:
        Bitwise XOR circuit for 2 inputs of the specified size.
    """
    result = circuit.Circuit('bXOR', 2*bits, bits)
    comps = [gates.XORGate() for _ in xrange(0, bits)]

    for i in xrange(0, bits):
        result.add_input_component(comps[i], {i: 0})
        result.add_input_component(comps[i], {i + bits: 1})

        result.add_output_component(comps[i], i)

    return result


def bitwise_not_circuit(bits):
    """
    Create a circuit to compute the bitwise inverse of the input.

    Parameters:
        bits:
            The number of bits expected for each input argument,
            which determines the size of the input and output space.

    Returns:
        Bitwise NOT circuit for specified input size.
    """
    result = circuit.Circuit('bNOT', bits, bits)
    comps = [gates.NOTGate() for _ in xrange(0, bits)]

    for i in xrange(0, bits):
        result.add_input_component(comps[i], {i: 0})
        result.add_output_component(comps[i], i)

    return result
