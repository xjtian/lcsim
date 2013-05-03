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
        The modified circuit. The operation is done in place so this will be
        the same reference as the parameter.

    Example usage:
        >>> from components import sources
        >>> from circuits import circuit
        >>> s = sources.DigitalArbitrary([0, 1, 1, 0, 1, 1])
        >>> c = circuit.Circuit('shift', 0, 6)
        >>> c.add_output_component(s, {i: i for i in xrange(0, 6)})
        >>> left_rotate(c, 2).evaluate()
        [1, 0, 1, 1, 0, 1]
    """
    output_size = len(circuit._outputs)
    shift %= output_size

    circuit._outputs = circuit._outputs[shift:] + circuit._outputs[:shift]
    return circuit


def right_rotate(circuit, shift):
    """
    Rotate (circular shift) the output bits of a given circuit to the right
    by 'shift' bits in place. If the number of bits to shift exceeds the
    output size of the circuit, the shift will be modded by the size of the
    output space.

    Parameters:
        circuit:
            The circuit to apply the right-rotate operation on.
        shift:
            Number of bits to rotate by.

    Returns:
        The modified circuit. The operation is done in place so this will be
        the same reference as the parameter.

    Example usage:
        >>> from components import sources
        >>> from circuits import circuit
        >>> s = sources.DigitalArbitrary([0, 1, 1, 0, 1, 1])
        >>> c = circuit.Circuit('shift', 0, 6)
        >>> c.add_output_component(s, {i: i for i in xrange(0, 6)})
        >>> right_rotate(c, 2).evaluate()
        [1, 1, 0, 1, 1, 0]
    """
    output_size = len(circuit._outputs)
    shift %= output_size

    i = output_size - shift
    circuit._outputs = circuit._outputs[i:] + circuit._outputs[:i]
    return circuit
