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
        # the tuple represents the output bit number that is wired to this input bit.
        self._input_bits = [None] * input_bits
		
		# Each index represents an output bit, and should contain a tuple (int, bool). The first element in the tuple 
		# is the output bit (0 or 1) and the boolean value represents if the bit is already wired.
        self.output_bits = [None] * output_bits

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
        pass

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
