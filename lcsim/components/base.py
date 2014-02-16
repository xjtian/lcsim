__author__ = 'Jacky Tian'


class MissingInputException(Exception):
    """
    A MissingInputException is thrown by a circuit component object when it
    is evaluated without enough input bits connected.
    """

    def __init__(self, message=''):
        self.message = message

    def __str__(self):
        return self.message


class ComponentBase(object):
    """
    Base class for circuit components. All functionality that is required
    for components is already defined except evaluate().

    For most cases, child classes will only need to override evaluate() and
    the constructor to define the behavior of the component/gate. In some
    circumstances it may be necessary to extend or override add_input(),
    and only in extremely rare circumstances should any other methods need
    to be overridden.
    """

    count = 0

    def __init__(self, name, input_bits, *args, **kwargs):
        """
        Initialize a base circuit component with a name and specific number
        of input and output bits.

        Parameters:
            name:
                Name of this component. Any arbitrary string will do.
            input_bits:
                Number of input bits the component accepts.

        :type name str
        :type input_bits int
        """
        self.name = name

        # Each element in the array represents an input bit, and is
        # a reference to a ComponentBase object that connects to
        # the input slot.
        self._input_bits = [None] * input_bits

        # Value of the output - None if unevaluated, otherwise 0 or 1
        self.output_bit = None

        # Graph edges for representing circuits as graphs
        self.parents = set()
        self.children = set()

        ComponentBase.count += 1

    def add_input(self, component, input_space):
        """
        Connect another component to this component by wiring output bits to
        input bits. The order of connection is specified by the
        mapping parameter, a dictionary keyed by the output
        component bit number to the input bit number of this
        component to wire to.

        Connections are one-to-one, so ValueError will be raised if this
        property is violated or non-existent bit indices are mapped.

        Note that this will alter the state of connected output component.

        Parameters:
            component:
                Output component to connect to this component's input spaces.
            input_space:
                Index of the bit of this component to connect to.

        Raises:
            ValueError if the input space is taken or out of bounds.

        :type component ComponentBase
        :type input_space int
        """
        if input_space < 0 or input_space >= len(self._input_bits):
            raise ValueError('Invalid input bit index %d' % input_space)

        if self._input_bits[input_space] is not None:
            raise ValueError('Input bit index %d is already taken' % input_space)

        self._input_bits[input_space] = component

        self.parents.add(component)
        component.children.add(self)

    def evaluate_inputs(self):
        """
        Evaluates all components connected to input slots of this component
        and returns an array of input bit values in order. ***This method
        should always be called BEFORE the body of logic in evaluate()***.

        Input values  are evaluated recursively, so the states of all parents
        and (grand)+parents of this component will be altered - namely,
        their output bits will be evaluated.

        Returns:
            int list of evaluated input bits in order.

        Raises:
            MissingInputException if any components that need to be
            evaluated to evaluate the result of this component have missing
            input connections.
        """
        result = [0] * len(self._input_bits)
        for j, gate in enumerate(self._input_bits):
            if gate.output_bit is None:
                gate.evaluate()

            result[j] = gate.output_bit

        return result

    def evaluate(self):
        """
        Evaluate the output result of this component. The result is stored
        in output_bits. Client classes should override this method to do
        whatever logic the component does with input gates after a call to
        evaluate_inputs().

        Note that the logic of this method is basically the only thing that
        differentiates different types of gates, apart from input space size.
        """
        pass

    def disconnect_inputs(self):
        """
        Free all input bits for this component. Calling this method will
        alter the state of the connected parent components as well by
        disconnecting their output bits.
        """
        for component in self.parents:
            component.children.remove(self)

        self.parents = set()
        self._input_bits = [None] * len(self._input_bits)

    def disconnect_outputs(self):
        """
        Free all output bits for this component. Calling this method will
        alter the state of the connected child components as well by
        disconnecting their corresponding input bits.
        """
        for component in frozenset(self.children):
            component._remove_input(self)

    def _remove_input(self, component):
        """
        Remove a specific input component from the inputs for this
        component. Exists as a helper method for disconnect_outputs and
        should not, except under extraordinary conditions,
        be called by client implementations.
        """
        if component not in self.parents:
            return

        self.parents.remove(component)
        component.children.remove(self)

        for i, gate in enumerate(self._input_bits):
            if gate is component:
                self._input_bits[i] = None

    def __hash__(self):
        """
        For hash(circuit_a) == hash(circuit_b), all inputs have to be
        the same (i.e. identical gates and bit indices), all circuits
        connected to are the same, and names are the same
        """
        return id(self)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return id(self) == id(other)
