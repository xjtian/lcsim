__author__ = 'Jacky'

from circuits import circuit
from components import gates


def full_adder_circuit():
    """
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
    xors = [gates.XORGate(), gates.XORGate()]
    ands = [gates.ANDGate(), gates.ANDGate()]
    ors = [gates.ORGate()]

    result.add_input_component(xors[0], {1: 0, 2: 1})
    result.add_input_component(xors[1], {0: 1})
    result.add_input_component(ands[0], {0: 1})
    result.add_input_component(ands[1], {1: 0, 2: 1})

    result.add_output_component(ors[0], {0: 0})
    result.add_output_component(xors[1], {1: 0})

    xors[1].add_input(xors[0], {0: 0})
    ands[0].add_input(xors[0], {0: 0})
    ors[0].add_input(ands[0], {0: 0})
    ors[0].add_input(ands[1], {0: 1})

    return result
