__author__ = 'Jacky Tian'


class MissingInputException(Exception):
    """
    Exception that is thrown when a component is evaluated without enough
    input bits connected.
    """

    def __init__(self, message=''):
        self.message = message

    def __str__(self):
        return self.message


class ComponentBase(object):
    """
    Base class for circuit components. Each client class is responsible for
    implementing the evaluate() method.
    """

    def __init__(self, name, input_bits, output_bits, *args, **kwargs):
        """
        Initialize a base circuit component. Specify the name of the
        component, the number of input bits, and the number of output bits.
        """
        self.name = name

        # Each index represents an input bit, and contains a tuple
        # (Component, int). int is the number of the output bit that is
        # wired to this input bit from the Component.
        self._input_bits = [None] * input_bits

        # Each list index corresponds to an output bit.
        self.output_bits = [-1] * output_bits
        # Set of output bits that are wired already
        self.occupied_outputs = set()

        # Graph edges for representing circuits as graphs
        self.parents = []
        self.children = []

    def add_input(self, component, mapping):
        """
        Connect another component to this component by connecting output
        bits to input bits. Connections are one-to-one,
        so ValueError will be  raised if occupied bits are attempted to be
        reconnected.
        """
        if len(mapping.keys()) > len(component.output_bits):
            raise ValueError(
                'Connections must be one-to-one. Too many output keys.')
        if len(mapping.values()) > len(self._input_bits):
            raise ValueError(
                'Connections must be one-to-one. Too many input values.'
            )

        for i in mapping.values():
            if i >= len(self._input_bits) or i < 0:
                raise ValueError(
                    'Invalid input bit number %d: not addressable bit.' % i)

            if self._input_bits[i] is not None:
                raise ValueError(
                    'Connections must be one-to-one. Input bit occupied')

        for i in mapping.keys():
            if i >= len(component.output_bits) or i < 0:
                raise ValueError(
                    'Invalid output bit number %d: not addressable bit.' % i)

            if i in component.occupied_outputs:
                raise ValueError(
                    'Connections must be one-to-one. Output bit occupied.')

        for k, v in mapping.items():
            # Create the mapping and mark parent output bit as occupied.
            self._input_bits[v] = (component, k)
            component.occupied_outputs.add(k)

        if component not in self.parents:
            self.parents.append(component)

        if self not in component.children:
            component.children.append(self)

    def evaluate_inputs(self):
        """
        Evaluates all input connections to this component and returns an
        array of input bit values in order. This will alter the state of
        connected parent components.
        """
        result = [0] * len(self._input_bits)
        for j, tup in enumerate(self._input_bits):
            component, i = tup
            if component.output_bits[i] == -1:
                component.evaluate()

            result[j] = component.output_bits[i]

        return result

    def evaluate(self):
        """
        Evaluate the output result of this component,
        which is stored in _output_bits. Should be implemented by client
        component classes.
        """
        pass

    def disconnect_inputs(self):
        """
        Free all input bits for this component. Calling this method will
        alter the state of the connected parent components.
        """
        for component, j in self._input_bits:
            # Free up the parent output bit
            component.occupied_outputs.discard(j)

        unique_components = set(
            [input_tuple[0] for input_tuple in self._input_bits])
        for component in unique_components:
            component.children.remove(self)
            self.parents.remove(component)

        self._input_bits = [None] * len(self._input_bits)

    def disconnect_outputs(self):
        """
        Free all output bits for this component. Calling this method will
        alter the state of the connected child components.
        """
        for component in self.children:
            component._remove_input(self)

        self.children = []

    def _remove_input(self, component):
        """
        Remove a specific input component from the inputs for this
        component. Exists as a helper method for disconnect_outputs and
        should not normally be called by client implementations.
        """
        if component not in self.parents:
            return

        self.parents.remove(component)
        for i, tup in enumerate(self._input_bits):
            c, j = tup
            if c == component:
                # 'Disconnect' output and input bit
                component.occupied_outputs.discard(j)
                self._input_bits[i] = None
