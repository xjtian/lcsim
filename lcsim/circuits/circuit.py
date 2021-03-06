__author__ = 'Jacky'


class InvalidCircuitException(Exception):
    """
    An InvalidCircuitException is thrown by a circuit when not all input and
    output spaces have been filled on evaluation.
    """
    def __init__(self, message=''):
        self.message = message

    def __str__(self):
        return self.message


class Circuit(object):
    """
    Base class for all circuits. Abstractly, a circuit is just a graph
    consisting of components (gates) as nodes and the wires between them as
    edges.

    Each available slot in the input space of the circuit maps directly to
    an available input slot for some gate, and each available output slot
    maps to an available output slot for some gate.
    """
    def __init__(self, name, input_size, output_size):
        """
        Initialize a base circuit, basically a network of connected circuit
        components.

        Parameters:
            name:
                The name for this circuit, can be any arbitrary string.

            input_size:
                The number of bits in the input space of the circuit.

            output_size:
                The number of bits in the output space of the circuit.
        """
        self.name = name

        # Each index represents an input space, and contains a list of tuples
        # (ComponentBase, int) representing the component and the input index of
        # it that occupies this input space.
        self._inputs = [[] for _ in xrange(0, input_size)]

        # Each index represents an output space, and contains a reference to
        # a ComponentBase that represents the component that outputs at this
        # space.
        self._outputs = [None] * output_size

    def add_input_component(self, component, mapping):
        """
        Set an input component for the circuit. Specify a mapping keyed by
        the circuit input space to the component input bit.

        Parameters:
            component:
                The component (inherit from ComponentBase) to add as an
                input.
            mapping:
                int: int dictionary keyed by intended input space of this
                circuit to the input bit number of the component.

        Raises:
            ValueError if the input space of the circuit is already taken
            or any mapping values are out of range.

        :type component ComponentBase
        :type mapping dict
        """
        for k, v in mapping.iteritems():
            if k < 0:
                raise ValueError('Invalid input space index %d.' % k)
            if v < 0:
                raise ValueError('Invalid input component index %d' % v)

            if k >= len(self._inputs):
                raise ValueError('Invalid input space index %d.' % k)
            if v >= len(component._input_bits):
                raise ValueError('Invalid component input index %d' % v)

        for k, v in mapping.iteritems():
            self._inputs[k].append((component, v))

    def add_output_component(self, component, output_index):
        """
        Set an output component for the circuit. Output bit index of the
        circuit is specified by the output_index parameter.

        Parameters:
            component:
                The component (inherit from ComponentBase) to add as an
                output.
            output_index:
                Output index of the circuit the given component is for.

        Raises:
            ValueError if the output space of the circuit is already taken
            or out of range.

        :type component ComponentBase
        :type output_index int
        """
        if output_index < 0 or output_index >= len(self._outputs):
            raise ValueError('Output index out of bounds: %d' % output_index)

        if self._outputs[output_index] is not None:
            raise ValueError('Circuit output space %d already taken.' % output_index)

        self._outputs[output_index] = component

    def evaluate(self):
        """
        Evaluate the result of the circuit. If any components in the circuit
        are not fully connected (i.e. have less input connections than
        minimally necessary) then a MissingInputException will bubble up.

        If there are missing components in the input or output space this
        method will raise an InvalidCircuitException.

        If all gates are fully connected, then the result of this method
        call will be that all the gates in the circuit are evaluated.
        Returns the evaluated output bits of all last-level gates in order
        as a list of ints.

        Returns:
            int list of evaluated output of circuit

        Raises:
            InvalidCircuitException if there are any unspecified input or
            output spaces.
        """
        if None in self._inputs:
            raise InvalidCircuitException('Circuit inputs not fully '
                                          'specified')
        if None in self._outputs:
            raise InvalidCircuitException('Circuit outputs not fully '
                                          'specified')

        result = [-1] * len(self._outputs)
        for i, gate in enumerate(self._outputs):
            gate.evaluate()
            result[i] = gate.output_bit

        return result


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
            int: int dictionary keyed by space of output circuit to space of
            input circuit.

    Raises:
        ValueError if the mapping is invalid in some way (connections
        must be one-to-one and within the output/input range of both
        circuits).

    :type out_circuit Circuit
    :type in_circuit Circuit
    :type mapping dict
    """
    for i in mapping.keys():
        if i >= len(out_circuit._outputs) or i < 0:
            raise ValueError('Invalid output bit number %d: not '
                             'addressable.' % i)

    for i in mapping.values():
        if i >= len(in_circuit._inputs) or i < 0:
            raise ValueError('Invalid input bit number %d: not '
                             'addressable.' % i)

    if None in out_circuit._outputs:
        raise ValueError('Output circuit is incomplete.')

    for k, v in mapping.iteritems():
        com_out = out_circuit._outputs[k]
        in_list = in_circuit._inputs[v]

        for (com_in, j) in in_list:
            com_in.add_input(com_out, j)


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
        >>> from lcsim.components import gates, sources
        >>> a = gates.ANDGate()
        >>> b = gates.ORGate()
        >>> s = sources.DigitalArbitrary([1, 1, 0, 0])
        >>> a.add_input(s, {0: 0, 1: 1})
        >>> b.add_input(s, {2: 0, 3: 1})
        >>> c1 = Circuit('top', 0, 1)
        >>> c2 = Circuit('bottom', 0, 1)
        >>> c1.add_output_component(a, {0: 0})
        >>> c2.add_output_component(b, {0: 0})
        >>> c3 = stack_circuits('name', c1, c2)
        >>> c3.evaluate()
        [1, 0]
    """
    new_inputs = c1._inputs + c2._inputs
    new_outputs = c1._outputs + c2._outputs

    result = Circuit(name, len(new_inputs), len(new_outputs))
    result._inputs = new_inputs
    result._outputs = new_outputs

    return result


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
        >>> from lcsim.components import gates, sources
        >>> a = gates.NOTGate()
        >>> b = gates.XORGate()
        >>> s = sources.DigitalArbitrary([1, 1, 0])
        >>> c = gates.ORGate()
        >>> c1 = Circuit('left', 0, 2)
        >>> c2 = Circuit('right', 2, 1)
        >>> a.add_input(s, {0: 0})
        >>> b.add_input(s, {1: 0, 2: 1})
        >>> c1.add_output_component(a, {0: 0})
        >>> c1.add_output_component(b, {1: 0})
        >>> c2.add_input_component(c, {0: 0, 1: 1})
        >>> c2.add_output_component(c, {0: 0})
        >>> connect_circuits(c1, c2, {0: 0, 1: 1})
        >>> c3 = merge_circuits('merged', c1, c2)
        >>> c3.evaluate()
        [1]
    """
    result = Circuit(name, len(c1._inputs), len(c2._outputs))
    result._inputs = c1._inputs
    result._outputs = c2._outputs

    return result
