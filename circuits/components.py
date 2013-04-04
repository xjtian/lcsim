__author__ = 'Jacky Tian'


class ComponentBase(object):
    """
    Base class for circuit components. Each client class is responsible for implementing the evaluate() method.
    """

    def __init__(self, name, input_bits, output_bits, *args, **kwargs):
        """
        Initialize a base circuit component. Specify the name of the component, the number of input bits, and the
        number of output bits.
        """
        self.name = name

        # Each index represents an input bit, and should contain a tuple (Component, int) where the second element in
        # the tuple represents the output bit number that is wired to this input bit from the Component.
        self._input_bits = [None] * input_bits

        # Each index represents an output bit, and should contain a 2-element list [int, bool]. The first element in
        # the list is the output bit (0, 1, or -1) and the boolean value represents if the bit is already wired.
        self._output_bits = [[-1, False]] * output_bits

        # Graph edges for representing circuits as graphs
        self.parents = []
        self.children = []

    def add_input(self, component, mapping):
        """
        Connect another component to this component by connecting output bits to input bits. Connections are one-to-one,
        so ValueError will be raised if occupied bits are attempted to be reconnected.

        @param component: Input component
        @type component: ComponentBase

        @param mapping: Dictionary keyed by output bit number to input bit number.
        @type mapping: dict
        """
        # TODO: rewrite more efficiently (backtracking)
        if len(mapping.keys()) > len(component._output_bits):
            raise ValueError('Connections must be one-to-one. Too many output keys in mapping')

        for i in mapping.values():
            if i >= len(self._input_bits) or i < 0:
                raise ValueError('Invalid input bit number %d: not addressable bit.' % i)

            if self._input_bits[i] is not None:
                raise ValueError('Connections must be one-to-one. Input bit already occupied')

        for i in mapping.keys():
            if i >= len(component._output_bits) or i < 0:
                raise ValueError('Invalid output bit number %d: not addressable bit.' % i)

            if component._output_bits[i][1]:
                raise ValueError('Connections must be one-to-one. Output bit already occupied.')

        for k, v in mapping.items():
            # Create the mapping and mark parent output bit as occupied.
            self._input_bits[v] = (component, k)
            component._output_bits[k][1] = True

        if component not in self.parents:
            self.parents.append(component)

        if self not in component.children:
            component.children.append(self)

    def evaluate_inputs(self):
        """
        Evaluates all input connections to this component and returns an array of input bit values in order. This will
        alter the state of connected parent components.
        """
        result = [0] * len(self._input_bits)
        for j, component, i in self._input_bits:
            if component._output_bits[i][0] == -1:
                component.evaluate()

            result[j] = component._output_bits[i][0]

        return result

    def evaluate(self):
        """
        Evaluate the output result of this component, which is stored in _output_bits. Should be implemented by client
        component classes.
        """
        pass

    def disconnect_inputs(self):
        """
        Free all input bits for this component. Calling this method will alter the state of the connected parent
        components.
        """
        for component, j in self._input_bits:
            # Free up the parent output bit
            component._output_bits[j][1] = False

        unique_components = set([input_tuple[0] for input_tuple in self._input_bits])
        for component in unique_components:
            component.children.remove(self)
            self.parents.remove(component)

        self._input_bits = [None] * len(self._input_bits)

    def disconnect_outputs(self):
        """
        Free all output bits for this component. Calling this method will alter the state of the connected child
        components.
        """
        for component in self.children:
            component._remove_input(self)

        self.children = []

    def _remove_input(self, component):
        """
        Remove a specific input component from the inputs for this component. Exists as a helper method for
        disconnect_outputs and should not normally be called by client implementations.

        @param component: Input component to remove.
        @type component: ComponentBase
        """
        if component not in self.parents:
            return

        self.parents.remove(component)
        for i, (c, _) in enumerate(self._input_bits):
            if c == component:
                self._input_bits[i] = None
