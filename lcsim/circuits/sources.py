from lcsim.circuits import circuit
from lcsim.components import sources

__author__ = 'Jacky'


def digital_source_circuit(output):
    """
    Create a digital source circuit that will always output the sequence of
    bits specified by the 'output' parameter. The circuit itself is composed
    entirely of DigitalOne and DigitalZero components instead of
    DigitalArbitrary.

    Parameters:
        output:
            A list of ints (0 or 1) that specifies the output sequence of
            the circuit.

    Returns:
        The resulting source circuit.

    Raises:
        ValueError if any values in 'output' parameter are not 1 or 0.

    Example usage:
        >>> c = digital_source_circuit([0, 1, 1, 0])
        >>> c.evaluate()
        [0, 1, 1, 0]
    """
    if any([x != 1 and x != 0 for x in output]):
        raise ValueError('Digital sources can only output 1 or 0.')

    result = circuit.Circuit('dSrc', 0, len(output))
    comps = [sources.DigitalOne() if x else sources.DigitalZero() for x in
             output]

    for i, src in enumerate(comps):
        result.add_output_component(src, i)

    return result


def digital_source_int_circuit(number, bits):
    """
    Create a digital source circuit that will always output the sequence
    and number of bits that correspond to the given positive integer and
    bit count. The circuit is composed entirely of DigitalOne and
    DigitalZero components instead of DigitalArbitrary.

    Parameters:
        number:
            The positive integer for the output sequence of bits.
        bits:
            How many bits should be used to represent the number.

    Returns:
        The resulting source circuit.

    Raises:
        ValueError if 'number' is negative, or the bit count is too low for
        the given number.

    Example usage:
        >>> c = digital_source_int_circuit(78, 8)
        >>> c.evaluate()
        [0, 1, 0, 0, 1, 1, 1, 0]
    """
    if number < 0:
        raise ValueError('Digital source output number must be unsigned.')

    if number > (1 << bits) - 1:
        raise ValueError('Digital source output number is too large to be '
                         'represented by the given bit count.')

    result = circuit.Circuit('dSrc', 0, bits)

    o_bits = map(int, bin(number)[2:])
    # Pad left with zeroes to get to bit count
    zeroes = [0 for _ in xrange(0, bits - len(o_bits))]
    zeroes.extend(o_bits)

    comps = [sources.DigitalOne() if x else sources.DigitalZero() for x in zeroes]
    for i, src in enumerate(comps):
        result.add_output_component(src, i)

    return result

