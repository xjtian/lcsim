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

    def __init__(self, name, input_bits, output_bits, *args, **kwargs):
        """
        Initialize a base circuit component with a name and specific number
        of input and output bits.

        Parameters:
            name:
                Name of this component. Any arbitrary string will do.
            input_bits:
                Number of input bits the component accepts.
            output_bits:
                Number of output bits the component returns.
        """
        self.name = name

        # Each index represents an input bit, and contains a tuple
        # (Component, int). int is the number of the output bit that is
        # wired to this input bit from the Component.
        self._input_bits = [None] * input_bits

        # Each list index corresponds to an output bit.
        self.output_bits = [-1] * output_bits

        # Graph edges for representing circuits as graphs
        self.parents = []
        self.children = []

    def add_input(self, component, mapping):
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
            mapping:
                int: int dictionary keyed by output component output bit
                number to the input bit number fo this component to connect
                it to.

        Raises:
            ValueError if the mapping is invalid in some way: not one-to-one
            or outside the range of addressable bits in input/output spaces.
        """
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

        for k, v in mapping.items():
            # Create the mapping
            self._input_bits[v] = (component, k)

        if component not in self.parents:
            self.parents.append(component)

        if self not in component.children:
            component.children.append(self)

    def evaluate_inputs(self):
        """
        Evaluates all input connections to this component and returns an
        array of input bit values in order. This method should always be
        called first before the body of logic in evaluate().

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
        for j, tup in enumerate(self._input_bits):
            component, i = tup
            if component.output_bits[i] == -1:
                component.evaluate()

            result[j] = component.output_bits[i]

        return result

    def evaluate(self):
        """
        Evaluate the output result of this component. The result is stored
        in output_bits. Client classes should override this method to do
        whatever logic the component does with input gates after a call to
        evaluate_inputs().

        Note that the logic of this method is basically the only thing that
        differentiates different types of gates, apart from input/output
        space sizes.
        """
        pass

    def disconnect_inputs(self):
        """
        Free all input bits for this component. Calling this method will
        alter the state of the connected parent components as well by
        disconnecting their output bits.
        """
        unique_components = set(
            [input_tuple[0] for input_tuple in self._input_bits])
        for component in unique_components:
            component.children.remove(self)
            self.parents.remove(component)

        self._input_bits = [None] * len(self._input_bits)

    def disconnect_outputs(self):
        """
        Free all output bits for this component. Calling this method will
        alter the state of the connected child components as well by
        disconnecting their corresponding input bits.
        """
        for component in self.children:
            component._remove_input(self)

        self.children = []

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
        for i, tup in enumerate(self._input_bits):
            c, j = tup
            if c == component:
                # 'Disconnect' input bit
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
