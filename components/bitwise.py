__author__ = 'Jacky'

from components import base


class BitwiseAND(base.ComponentBase):
    """
    Component to compute the bitwise AND of two equal-sized inputs.

    Example usage:
        >>> from components import sources
        >>> a = BitwiseAND(4)
        >>> s = sources.DigitalArbitrary([0, 1, 1, 0, 1, 1, 0, 0])
        >>> a.add_input(s, {i: i for i in xrange(0, 8)})
        >>> a.evaluate()
        >>> a.output_bits
        [0, 1, 0, 0]
    """
    def __init__(self, bits):
        super(BitwiseAND, self).__init__('bAND', 2 * bits, bits)
        self.bits = bits

    def evaluate(self):
        inputs = self.evaluate_inputs()

        left = inputs[:self.bits]
        right = inputs[self.bits:]

        for i in xrange(0, self.bits):
            self.output_bits[i] = int(left[i] and right[i])


class BitwiseOR(base.ComponentBase):
    """
    Component to compute the bitwise OR of two equal-sized inputs.

    Example usage:
        >>> from components import sources
        >>> a = BitwiseOR(4)
        >>> s = sources.DigitalArbitrary([0, 1, 1, 0, 1, 1, 0, 0])
        >>> a.add_input(s, {i: i for i in xrange(0, 8)})
        >>> a.evaluate()
        >>> a.output_bits
        [1, 1, 1, 0]
    """
    def __init__(self, bits):
        super(BitwiseOR, self).__init__('bOR', 2 * bits, bits)
        self.bits = bits

    def evaluate(self):
        inputs = self.evaluate_inputs()

        left = inputs[:self.bits]
        right = inputs[self.bits:]

        for i in xrange(0, self.bits):
            self.output_bits[i] = int(left[i] or right[i])


class BitwiseXOR(base.ComponentBase):
    """
    Component to compute the bitwise XOR of two equal-sized inputs.

    Example usage:
        >>> from components import sources
        >>> a = BitwiseXOR(4)
        >>> s = sources.DigitalArbitrary([0, 1, 1, 0, 1, 1, 0, 0])
        >>> a.add_input(s, {i: i for i in xrange(0, 8)})
        >>> a.evaluate()
        >>> a.output_bits
        [1, 0, 1, 0]
    """
    def __init__(self, bits):
        super(BitwiseXOR, self).__init__('bXOR', 2 * bits, bits)
        self.bits = bits

    def evaluate(self):
        inputs = self.evaluate_inputs()

        left = inputs[:self.bits]
        right = inputs[self.bits:]

        for i in xrange(0, self.bits):
            self.output_bits[i] = left[i] ^ right[i]


class BitwiseNOT(base.ComponentBase):
    """
    Component to compute the bitwise NOT of a set-size input (i.e. invert
    all the bits in the input).

    Example usage:
        >>> from components import sources
        >>> a = BitwiseNOT(4)
        >>> s = sources.DigitalArbitrary([0, 1, 1, 0])
        >>> a.add_input(s, {i: i for i in xrange(0, 4)})
        >>> a.evaluate()
        >>> a.output_bits
        [1, 0, 0, 1]
    """
    def __init__(self, bits):
        super(BitwiseNOT, self).__init__('bNOT', bits, bits)

    def evaluate(self):
        self.output_bits = map(lambda x: int(not x), self.evaluate_inputs())
