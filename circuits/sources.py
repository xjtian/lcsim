__author__ = 'Jacky'

from components import sources
from circuits import circuit


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
        result.add_output_component(src, {i: 0})

    return result
