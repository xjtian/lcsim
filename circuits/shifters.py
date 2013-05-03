__author__ = 'Jacky'


def left_rotate(circuit, shift):
    """
    Rotate (circular shift) the output bits of a given circuit to the left
    by 'shift' bits in place. If the number of bits to shift exceeds the
    output size of the circuit, the shift will be modded by the size of the
    output space.

    Parameters:
        circuit:
            The circuit to apply the left-rotate operation on.
        shift:
            Number of bits to rotate by.

    Returns:
        The modified circuit (same object as the one passed in the parameter).

    Example usage:
        >>> from components import sources
        >>> from circuits import circuit
        >>> s = sources.DigitalArbitrary([0, 1, 1, 0])
        >>> c = circuit.Circuit('shift', 0, 4)
        >>> c.add_output_component(s, {i: i for i in xrange(0, 4)})
        >>> left_rotate(c, 2).evaluate()
        [1, 0, 0, 1]
    """
    output_size = len(circuit._outputs)
    shift %= output_size

    circuit._outputs = circuit._outputs[shift:] + circuit._outputs[:shift]
    return circuit
