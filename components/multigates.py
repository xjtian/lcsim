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
        Appends input spaces as necessary and rstrips unused input bits.
        """
        max_val = max(mapping.values())
        if max_val >= len(self._input_bits):
            self._input_bits.extend([None] * (max_val - len(self._input_bits) + 1))

        super(MultiGateBase, self).add_input(component, mapping)

        # Strip out any strings of unused input bits at the end of _input_bits
        count = 0
        for i in xrange(len(self._input_bits) - 1, -1, -1):
            if not self._input_bits[i]:
                count += 1
            else:
                break

        if count:
            self._input_bits = self._input_bits[:-count]

    def evaluate(self):
        """
        Called by client classes before evaluation logic to make sure gate has enough input bits to function.
        """
        count = 0
        for i, bit in enumerate(self._input_bits):
            if bit is not None:
                count += 1
                if count >= self.min_input:
                    break

        if count < self.min_input:
            raise base.MissingInputException(
                '%s gate requires at least %d input bits. Only %d are connected.' % (self.name, self.min_input, count))
