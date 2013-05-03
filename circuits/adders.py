__author__ = 'Jacky'

from circuits import circuit
from components import gates


def __full_adder_components():
    """
    Returns arrays of the gates in a full adder all internally connected.

    Returns:
        (xors, ands, ors):
            Three lists of the gates in the full adder. They are all
            internally connected properly, and only need to be hooked up to
            input/output spaces of circuits.
    """
    xors = [gates.XORGate(), gates.XORGate()]
    ands = [gates.ANDGate(), gates.ANDGate()]
    ors = [gates.ORGate()]

    xors[1].add_input(xors[0], {0: 0})
    ands[0].add_input(xors[0], {0: 0})
    ors[0].add_input(ands[0], {0: 0})
    ors[0].add_input(ands[1], {0: 1})

    return xors, ands, ors


def full_adder_circuit():
    """
    Returns a 1-bit full adder circuit. Expected order of input bits is
    (Cin, A, B) and output bits are in order of (Cout, S).

    Returns:
        A 1-bit full-adder circuit.

    Example usage:
        >>> from components import sources
        >>> from circuits import circuit
        >>> s = sources.DigitalArbitrary([1, 1, 1])
        >>> src = circuit.Circuit('src', 0, 3)
        >>> src.add_output_component(s, {0: 0, 1: 1, 2: 2})
        >>> adder = full_adder_circuit()
        >>> circuit.connect_circuits(src, adder, {0: 0, 1: 1, 2: 2})
        >>> adder.evaluate()
        [1, 1]
    """
    result = circuit.Circuit('FAdd', 3, 2)
    xors, ands, ors = __full_adder_components()

    result.add_input_component(xors[0], {1: 0, 2: 1})
    result.add_input_component(xors[1], {0: 1})
    result.add_input_component(ands[0], {0: 1})
    result.add_input_component(ands[1], {1: 0, 2: 1})

    result.add_output_component(ors[0], {0: 0})
    result.add_output_component(xors[1], {1: 0})

    return result


def ripple_adder_no_carry(bits):
    """
    Create a ripple-carry adder without carry (equivalent to a mod-adder).
    """
    result = circuit.Circuit('%dAdd' % bits, 2 * bits, bits)
    full_adds = [__full_adder_components() for _ in xrange(0, bits)]

    for i, xors, ands, ors in enumerate(full_adds):
        if i < bits:
            # First connect the carry bit from this adder to Cin of next adder
            (next_xors, next_ands, _) = full_adds[i + 1]
            # Carry bit is the result of the OR gate
            next_xors[1].add_input(ors[0], {0: 1})
            next_ands[0].add_input(ors[0], {0: 1})

        # Now connect the circuit inputs for this bit addition
        # Remember inputs are stacked so A is i, B is 2 * i
        result.add_input_component(xors[0], {i: 0, 2 * i: 1})
        result.add_input_component(ands[1], {i: 0, 2 * i: 1})

        # Now set the output sum bit, result of the second XOR gate
        result.add_output_component(xors[1], {i: 0})

    return result