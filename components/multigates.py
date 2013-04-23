__author__ = 'Jacky'

from components import base


class MultiGateBase(base.ComponentBase):
    """
    Base class for all multiple fan-in logic gates.
    """

    def __init__(self, name, minimum_input, output_bits):
        self.min_input = minimum_input
        super(MultiGateBase, self).__init__(name, minimum_input, output_bits)

    def add_input(self, component, mapping):
        """
        Appends input spaces as necessary and consolidates the input bits to
        eliminate unused inputs.
        """
        max_val = max(mapping.values())
        if max_val >= len(self._input_bits):
            self._input_bits.extend(
                [None] * (max_val - len(self._input_bits) + 1))

        super(MultiGateBase, self).add_input(component, mapping)

        # Strip out all unused input bits
        self._input_bits = filter(None, self._input_bits)

    def evaluate(self):
        """
        Called by client classes before evaluation logic to make sure gate
        has enough input bits to function.
        """
        count = 0
        for i, bit in enumerate(self._input_bits):
            if bit is not None:
                count += 1
                if count >= self.min_input:
                    break

        if count < self.min_input:
            raise base.MissingInputException(
                '%s gate requires at least %d input bits. '
                'Only %d are connected.' % (self.name, self.min_input, count))


class MultiANDGate(MultiGateBase):
    """
    AND gate with multiple fan-in.
    """

    def __init__(self):
        super(MultiANDGate, self).__init__('mAND', 2, 1)

    def evaluate(self):
        super(MultiANDGate, self).evaluate()
        if all(self.evaluate_inputs()):
            self.output_bits[0] = 1
        else:
            self.output_bits[0] = 0


class MultiORGate(MultiGateBase):
    """
    OR gate with multiple fan-in.
    """

    def __init__(self):
        super(MultiORGate, self).__init__('mOR', 2, 1)

    def evaluate(self):
        super(MultiORGate, self).evaluate()

        if any(self.evaluate_inputs()):
            self.output_bits[0] = 1
        else:
            self.output_bits[0] = 0


class MultiNOTGate(MultiGateBase):
    """
    NOT gate with multiple fan-in and corresponding multiple fan-out
    """

    def __init__(self):
        super(MultiNOTGate, self).__init__('mNOT', 1, 1)

    def evaluate(self):
        super(MultiNOTGate, self).evaluate()
        self.output_bits = map(lambda x: int(not x), self.evaluate_inputs())


class MultiXORGate(MultiGateBase):
    """
    XOR gate with multiple fan-in. Outputs 1 if the number of high input
    bits is odd, 0 otherwise.
    """

    def __init__(self):
        super(MultiXORGate, self).__init__('mXOR', 2, 1)

    def evaluate(self):
        super(MultiXORGate, self).evaluate()
        self.output_bits[0] = sum(self.evaluate_inputs()) % 2
