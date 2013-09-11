__author__ = 'jacky'

from circuits.sources import digital_source_int_circuit
from circuits import bitwise, circuit

h0 = digital_source_int_circuit(0x67452301, 32)


h1 = digital_source_int_circuit(0xEFCDAB89, 32)


h2 = digital_source_int_circuit(0x98BADCFE, 32)


h3 = digital_source_int_circuit(0x10325476, 32)


h4 = digital_source_int_circuit(0xC3D2E1F0, 32)


def f_first_quarter():
    """
    Returns the circuit that evaluates (h1 and h2) or ((not h1) and h3).
    In the pseudocode, this is f = (b and c) or ((not b) and d) for
    0 <= i <= 19.
    """
    # (h1 and h2)
    c_and = bitwise.bitwise_and_circuit(32)
    stacked_inputs = circuit.stack_circuits('h1-h2 stack', h1, h2)
    circuit.connect_circuits(stacked_inputs, c_and, {i: i for i in xrange(0, 64)})

    h1_and_h2 = circuit.merge_circuits('h1 and h2', stacked_inputs, c_and)

    # (not h1)
    c_not = bitwise.bitwise_not_circuit(32)
    circuit.connect_circuits(h1, c_not, {i: i for i in xrange(0, 32)})

    not_h1 = circuit.merge_circuits('not h1', h1, c_not)

    # ((not h1) and h3)
    c_and = bitwise.bitwise_and_circuit(32)
    stacked_inputs = circuit.stack_circuits('not h1-h3 stack', not_h1, h3)
    circuit.connect_circuits(stacked_inputs, c_and, {i: i for i in xrange(0, 64)})

    not_h1_and_h3 = circuit.merge_circuits('(not h1) and h3', stacked_inputs, c_and)

    # (h1 and h2) or ((not h1) and h3)
    c_or = bitwise.bitwise_or_circuit(32)
    stacked_inputs = circuit.stack_circuits('final stack', h1_and_h2, not_h1_and_h3)
    circuit.connect_circuits(stacked_inputs, c_or, {i: i for i in xrange(0, 64)})

    result = circuit.merge_circuits('first quarter main loop', stacked_inputs, c_or)
    return result
