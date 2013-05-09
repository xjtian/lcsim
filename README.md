lcsim
=====

lcsim is a logical circuit simulator for Python. Circuits are represented as
intra- and inter-connected networks of circuit components. Circuit
components generically are black boxes that transform an input of m bits to
an output of n bits (e.g. boolean operators, adders, etc.).

Components
----------
A component can be any arbitrary operation on input bits. To define a custom
component, subclass the `components.ComponentBase` class and define your own
constructor and `evaluate()` methods.

Consider the following component that, given a 4-bit input integer A outputs
the result of the operation `3*(A << 1)`:

    from components import base
    class ExampleCom(base.ComponentBase):
        def __init__(self):
            super(ExampleCom, self).__init__('ex', 4, 4)

        def evaluate():
            inputs = self.evaluate_inputs()
            a = int(''.join(map(str, inputs)), 2)

            b = map(int, bin((3 * (a << 1)) % 16)[2:])
            while len(b) < 4:
                b.insert(0, 0)

            self.output_bits = b

Circuits
--------
A circuit is a network of connected components, usually basic logic gates
(AND, NOT, OR, XOR). Just like components, circuits take an input of m bits
and transform to an output of n bits. For every possible component,
an equivalent circuit should exist as well.

Circuits are meant to be built modularly from other circuits. Consider the
following circuit that, given an input of 3 4-bit integers A,B, and C,
outputs `((A + B) leftrotate 2) xor C` (with addition mod 2^4).

    from circuits import sources, shifters, adders, bitwise, circuit

    plus = adders.ripple_adder_no_carry(4)
    shifters.left_rotate(plus, 2)
    xor = bitwise.bitwise_xor_circuit(4)

    circuit.connect_circuits(plus, xor, {0: 0, 1: 1, 2: 2, 3: 3})

    inputs = sources.digital_source_circuit([0, 1, 0, 1, 1, 1, 0, 1])
    c = sources.digital_source_circuit([0, 1, 1, 0])

    circuit.connect_circuits(inputs, plus, {i: i for i in xrange(0, 8)})
    circuit.connect_circuits(c, xor, {0: 4, 1: 5, 2: 6, 3: 7})

    combined_sources = circuit.stack_circuits(inputs, c)
    op = circuit.merge_circuits(combined_sources, xor)

    print op.evaluate()

