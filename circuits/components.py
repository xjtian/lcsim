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

        # Each index represents an output bit, and should contain a tuple (int, bool). The first element in the tuple
        # is the output bit (0 or 1) and the boolean value represents if the bit is already wired.
        self._output_bits = [(-1, False)] * output_bits

        # Graph edges for representing circuits as graphs
        self.parents = []
        self.children = []

    def add_input(self, component, mapping):
        """
        Connect another component to this component by connecting output bits to input bits.

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
            self._input_bits[k] = (component, v)

        if component not in self.parents:
            self.parents.append(component)

        if self not in component.children:
            component.children.append(self)

    def evaluate(self):
        """
        Evaluates the result of this component by recursively getting input values. Result is stored in output_bits and
        returned.

        @return: output_bits after evaluation
        """
        pass

    def remove_input(self, component):
        """
        Remove a specific input component from the inputs for this component.

        @param component: Input component to remove.
        @type component: ComponentBase
        """
        pass

    def disconnect(self):
        """
        Disconnect this component from its connections.
        """
        pass
