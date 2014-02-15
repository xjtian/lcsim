from lcsim.circuits import circuit
from lcsim.components import gates

__author__ = 'Jacky'


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

    xors[1].add_input(xors[0], 0)
    ands[0].add_input(xors[0], 0)
    ors[0].add_input(ands[0], 0)
    ors[0].add_input(ands[1], 1)

    return xors, ands, ors


def full_adder_circuit():
    """
    Returns a 1-bit full adder circuit. Expected order of input bits is
    (Cin, A, B) and output bits are in order of (Cout, S).

    Returns:
        A 1-bit full-adder circuit.
    """
    result = circuit.Circuit('FAdd', 3, 2)
    xors, ands, ors = __full_adder_components()

    result.add_input_component(xors[0], {1: 0, 2: 1})
    result.add_input_component(xors[1], {0: 1})
    result.add_input_component(ands[0], {0: 1})
    result.add_input_component(ands[1], {1: 0, 2: 1})

    result.add_output_component(ors[0], 0)
    result.add_output_component(xors[1], 1)

    return result


def ripple_adder_no_carry(bits):
    """
    Create a ripple-carry adder without carry output (equivalent to addition
    mod 2^bits). When using the circuit, stack the inputs. E.g. for a 4-bit
    adder, the input space should be A0-A1-A2-A3-B0-B1-B2-B3.

    Parameters:
        bits:
            Size of inputs in bits the adder is intended to take.

    Returns:
        An n-bit ripple-carry adder with the final carry bit dropped.
    """
    result = circuit.Circuit('%dAdd' % bits, 2 * bits, bits)
    full_adds = [__full_adder_components() for _ in xrange(0, bits)]

    for i in xrange(bits - 1, -1, -1):
        if i < bits - 1:
            xors, ands, ors = full_adds[i]
            if i > 0:
                # Connect the carry bit from this adder to Cin of next
                (next_xors, next_ands, _) = full_adds[i - 1]
                # Carry bit is the result of the OR gate
                next_xors[1].add_input(ors[0], 1)
                next_ands[0].add_input(ors[0], 1)

            # Now connect the circuit inputs for this bit addition
            # Remember inputs are stacked so A is i, B is i + bits
            result.add_input_component(xors[0], {i: 0, i + bits: 1})
            result.add_input_component(ands[1], {i: 0, i + bits: 1})

            # Now set the output sum bit, result of the second XOR gate
            result.add_output_component(xors[1], i)
        else:
            # Since Cin is always 0 (off), use a half-adder for the first
            # circuit
            xor_g = gates.XORGate()
            and_g = gates.ANDGate()

            result.add_input_component(xor_g, {i: 0, i + bits: 1})
            result.add_input_component(and_g, {i: 0, i + bits: 1})

            result.add_output_component(xor_g, i)
            if bits > 1:
                # Connect carry bit the the next full adder
                (next_xors, next_ands, _) = full_adds[i - 1]
                next_xors[1].add_input(and_g, 1)
                next_ands[0].add_input(and_g, 1)

    return result