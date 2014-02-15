from circuits.circuit import Circuit


def left_rotate_in_place(circuit, shift):
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
    """
    output_size = len(circuit._outputs)
    shift %= output_size

    circuit._outputs = circuit._outputs[shift:] + circuit._outputs[:shift]
    return circuit


def left_rotate(circuit, shift):
    """
    Rotate (circular shift) the output bits of a given circuit to the left
    by `shift` bits and return a new circuit. If the number of bits to shift
    exceeds the output size of the circuit, the shift will be modded by the
    size of the output space.

    Parameters:
        circuit:
            The circuit to apply the left-rotate operation on.
        shift:
            Number of bits to rotate by.

    Returns:
        A new circuit object that is the result of the rotation.
    """
    output_size = len(circuit._outputs)
    shift %= output_size

    result = Circuit(circuit.name, len(circuit._inputs), len(circuit._outputs))
    result._inputs = circuit._inputs[:]
    result._outputs = circuit._outputs[shift:] + circuit._outputs[:shift]

    return result


def right_rotate_in_place(circuit, shift):
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
    """
    output_size = len(circuit._outputs)
    shift %= output_size

    i = output_size - shift
    circuit._outputs = circuit._outputs[i:] + circuit._outputs[:i]
    return circuit


def right_rotate(circuit, shift):
    """
    Rotate (circular shift) the output bits of a given circuit to the right
    by 'shift' bits. If the number of bits to shift exceeds the
    output size of the circuit, the shift will be modded by the size of the
    output space.

    Parameters:
        circuit:
            The circuit to apply the right-rotate operation on.
        shift:
            Number of bits to rotate by.

    Returns:
        A new circuit that is the result of the rotation.
    """
    output_size = len(circuit._outputs)
    shift %= output_size

    i = output_size - shift

    result = Circuit(circuit.name, len(circuit._inputs), len(circuit._outputs))
    result._inputs = circuit._inputs[:]
    result._outputs = circuit._outputs[i:] + circuit._outputs[:i]

    return result
