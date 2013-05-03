__author__ = 'Jacky'

from circuits import circuit
from components import gates


def full_adder_circuit():
    result = circuit.Circuit('FAdd', 3, 2)
    xors = [gates.XORGate(), gates.XORGate()]
    ands = [gates.ANDGate(), gates.ANDGate()]
    ors = [gates.ORGate()]

    result.add_input_component(xors[0], {0: 0, 1: 1})
