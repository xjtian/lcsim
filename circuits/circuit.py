__author__ = 'Jacky'


class Circuit(object):
    """
    Base class for all circuits. Abstractly, a circuit is just a graph
    consisting of circuit elements as nodes and the wires between them as
    edges.

    In this representation, only the first and last "levels" of the circuit
    are explicitly tracked. The input spaces of all first-level components
    represent the input space of the circuit, and the output spaces of all
    last-level components represent the output space of the circuit.

    In this way, the circuit can also be thought of as a function n->m bits.
    """
    def __init__(self, name, inputs, outputs):
        """
        Initialize a base circuit, basically a network of connected circuit
        components.

        Parameters:
            name:
                The name for this circuit, can be any arbitrary string.

            inputs:
                If known, a list of circuit components (inherit from
                ComponentBase) that form the first "level" of the circuit.

            outputs:
                If known, a list of circuit components (inherit from
                ComponentBase) that for the last "level" of the circuit.
                These are the gates that form the output space of the circuit.

        Example usage:
            >>> from components import gates
            >>> a = gates.ANDGate()
            >>> b = gates.ORGate()
            >>> c = gates.ANDGate()
            >>> c.add_input(a, {0: 0})
            >>> c.add_input(b, {0: 1})
            >>> circuit = Circuit('example', [a, b], [c])
            >>> circuit.input_size
            4
            >>> circuit.output_size
            1
        """
        self.name = name
        self.inputs = inputs
        self.outputs = outputs

        self.input_size = 0
        self.output_size = 0

        for gate in self.inputs:
            self.input_size += len(gate._input_bits)

        for gate in self.outputs:
            self.output_size += len(gate.output_bits)

    def append_input(self, component):
        """
        Append a component to the input space of the circuit.

        Parameters:
            component:
                The circuit component (inherit from ComponentBase) to append
                 to the input space of the circuit.

        Example usage:
            >>> from components import gates
            >>> c = Circuit('example', [], [])
            >>> c.append_input(gates.ANDGate())
            >>> c.input_size
            2
        """
        self.inputs.append(component)
        self.input_size += len(component._input_bits)

    def prepend_input(self, component):
        """
        Prepend a component to the input space of the circuit.

        Parameters:
            component:
                The circuit component (inherit from ComponentBase) to
                prepend to the input space of the circuit.

        Example usage:
            >>> from components import gates
            >>> c = Circuit('example', [], [])
            >>> c.prepend_input(gates.ANDGate())
            >>> c.input_size
            2
        """
        self.inputs.insert(0, component)
        self.input_size += len(component._input_bits)

    def append_output(self, component):
        """
        Append a component to the output space of the circuit.

        Parameters:
            component:
                The circuit component (inherit from ComponentBase) to append
                 to the output space of the circuit.

        Example usage:
            >>> from components import gates
            >>> c = Circuit('example', [], [])
            >>> c.append_output(gates.ANDGate())
            >>> c.output_size
            1
        """
        self.outputs.append(component)
        self.output_size += len(component.output_bits)

    def prepend_output(self, component):
        """
        Prepend a component to the output space of the circuit.

        Parameters:
            component:
                The circuit component (inherit from ComponentBase) to
                prepend to the output space of the circuit.

        Example usage:
            >>> from components import gates
            >>> c = Circuit('example', [], [])
            >>> c.prepend_output(gates.ANDGate())
            >>> c.output_size
            1
        """
        self.outputs.insert(0, component)
        self.output_size += len(component.output_bits)

    def evaluate(self):
        """
        Evaluate the result of the circuit. This method will raise an
        exception if any components in the circuit are not fully connected (
        i.e. have less input bits than minimally necessary).

        If all gates are fully connected, then the result of this method
        call will be that all the gates in the circuit are evaluated.
        Returns the evaluated output bits of all last-level gates in order
        as a list of ints.

        Returns:
            int list of evaluated output of circuit

        Raises:
            MissingInputException from evaluate() calls to gates if any gate
             is not connected.

        Example usage:
            >>> from components import gates, sources
            >>> s = sources.DigitalArbitrary([0, 1, 1, 1])
            >>> a = gates.ANDGate()
            >>> b = gates.ORGate()
            >>> a.add_input(s, {0: 0, 1: 1})
            >>> b.add_input(s, {2: 0, 3: 1})
            >>> circuit = Circuit('example', [s], [a, b])
            >>> circuit.evaluate()
            [0, 1]
        """
        i = 0
        output = [0] * self.output_size

        for gate in self.outputs:
            gate.evaluate()
            for bit in gate.output_bits:
                output[i] = bit
                i += 1

        return output


def connect_circuits(out_circuit, in_circuit, mapping):
    """
    Connect two circuits together by wiring output bits from one to the
    input bits of another. The wiring order is specified by the mapping
    parameter.

    Parameters:
        out_circuit:
            Circuit (inherits from Circuit) to wire connections from.
        in_circuit:
            Circuit (inherits from Circuit) to wire connections to.
        mapping:
            dictionary of int: int keyed by output bit number of output
             circuit to input bit number of target input circuit.

    Raises:
        ValueError if the mapping is invalid in some way (connections
        must be one-to-one and within the output/input range of both
        circuits).

    Example usage:
        >>> from components import gates, sources
        >>> s = sources.DigitalArbitrary([0, 1])
        >>> a = gates.ORGate()
        >>> b = gates.NOTGate()
        >>> a.add_input(s, {0: 0, 1: 1})
        >>> c1 = Circuit('example1', [s], [a])
        >>> c2 = Circuit('example2', [b], [b])
        >>> connect_circuits(c1, c2, {0: 0})
        >>> c2.evaluate()
        [0]
    """
    if len(mapping.keys()) > out_circuit.output_size or len(mapping.values()) >\
            in_circuit.input_size:
        raise ValueError('Connections must be one-to-one. Too many pairs'
                         ' in mapping')

    for i in mapping.keys():
        if i >= out_circuit.output_size:
            raise ValueError('Invalid output bit number %d: not '
                             'addressable.' % i)

    for i in mapping.values():
        if i >= in_circuit.input_size:
            raise ValueError('Invalid input bit number %d: not '
                             'addressable.' % i)

    output_cache = [None] * out_circuit.output_size
    input_cache = [None] * in_circuit.input_size

    i = 0
    for gate in out_circuit.outputs:
        for j in xrange(0, len(gate.output_bits)):
            output_cache[i+j] = (gate, i)
        i += len(gate.output_bits)

    i = 0
    for gate in in_circuit.inputs:
        for j in xrange(0, len(gate._input_bits)):
            input_cache[i+j] = (gate, i)
        i += len(gate._input_bits)

    # Let the components handle the rest of the validation process
    for k, v in mapping.items():
        input_gate, i = input_cache[v]
        output_gate, j = output_cache[k]

        input_gate.add_input(output_gate, {k-j: v-i})


def stack_circuits(name, c1, c2):
    """
    Stack two circuits together by merging them side-by-side. Conceptually
    like putting two circuits together in parallel. Returns the resulting
    circuit.

    Parameters:
        name:
            The name to give to the resulting circuit. Can be any arbitrary
            string.
        c1:
            Top circuit to stack. The input and output bit positions of this
            circuit will remain unchanged in the resulting stacked circuit.

        c2:
            Bottom circuit to stack. The input and output bit positions of
            this circuit will be shifted by the input and output size of c1,
            respectively.

    Returns:
        The resulting stacked circuit as a single circuit object.

    Example usage:
        >>> from components import gates, sources
        >>> s1 = sources.DigitalArbitrary([1, 1])
        >>> s2 = sources.DigitalArbitrary([0, 0])
        >>> a = gates.ANDGate()
        >>> b = gates.ORGate()
        >>> a.add_input(s1, {0: 0, 1: 1})
        >>> b.add_input(s2, {0: 0, 1: 1})
        >>> c1 = Circuit('example1', [s1], [a])
        >>> c2 = Circuit('example2', [s2], [b])
        >>> c3 = stack_circuits('example3', c1, c2)
        >>> c3.evaluate()
        [1, 0]
    """
    return Circuit(name, c1.inputs + c2.inputs, c1.outputs + c2.outputs)


def merge_circuits(name, c1, c2):
    """
    Merge two circuits together. The input components of c1 become the input
    components of the resulting merged circuit, and the output components
    of c2 become the output components of the merged circuit. Returns the
    merged circuit.

    Unless all output bits of c1 and all input bits of c2 are connected,
    you should hang on to those references so you can still manipulate the
    output components of c1 and input components of c2 that get hidden when
    the two circuits are merged.

    Parameters:
        name:
            The name to give to the resulting circuit. Can be any arbitrary
            string.
        c1:
            Circuit to take inputs from.
        c2:
            Circuit to take outputs from.

    Returns:
        The resulting merged circuit.

    Example usage:
        >>> from components import gates, sources
        >>> s1 = sources.DigitalArbitrary([0, 1, 1, 1])
        >>> a = gates.ANDGate()
        >>> b = gates.ORGate()
        >>> c = gates.XORGate()
        >>> a.add_input(s1, {0: 0, 1: 1})
        >>> b.add_input(s1, {2: 0, 3: 1})
        >>> left_circuit = Circuit('example', [s1], [a,b])
        >>> right_circuit = Circuit('example2', [c], [c])
        >>> connect_circuits(left_circuit, right_circuit, {0: 0, 1: 1})
        >>> merge_circuits('example3', left_circuit, right_circuit).evaluate()
        [1]
    """
    return Circuit(name, c1.inputs, c2.outputs)