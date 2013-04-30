__author__ = 'jacky'

from components import base


class HalfAdder(base.ComponentBase):
    """
    Half-adder component. Takes 2 bits A and B and outputs their sum. The
    sum bit is the second output bit and the carry bit is the first.

    Example usage:
        >>> from components import sources
        >>> a = HalfAdder()
        >>> s = sources.DigitalArbitrary([0, 1])
        >>> a.add_input(s, {0: 0, 1: 1})
        >>> a.evaluate()
        >>> a.output_bits
        [0, 1]
    """
    def __init__(self):
        """
        Initialize a new half-adder.
        """
        super(HalfAdder, self).__init__('HAdd', 2, 2)

    def evaluate(self):
        """
        Evaluate the sum of the input bits. The sum bit will be stored in
        the second output bit and the carry bit in the first.
        """
        inputs = self.evaluate_inputs()

        result = bin(inputs[0] + inputs[1])[2:]
        if len(result) == 2:
            self.output_bits = [1, 0]
        else:
            self.output_bits[1] = int(result[0])
            self.output_bits[0] = 0


class FullAdder(base.ComponentBase):
    """
    Full-adder component. Takes 3 input bits A, B, and Cin,
    and outputs their sum. The sum bit is the second output bit and the carry
    bit is the first.

    Example usage:
        >>> from components import sources
        >>> a = FullAdder()
        >>> s = sources.DigitalArbitrary([0, 1, 1])
        >>> a.add_input(s, {0: 0, 1: 1, 2: 2})
        >>> a.evaluate()
        >>> a.output_bits
        [1, 0]
    """
    def __init__(self):
        super(FullAdder, self).__init__('FAdd', 3, 2)

    def evaluate(self):
        """
        Evaluate the sum of the three input bits. The sum bit will be stored
        in the second output bit and the carry bit in the first.
        """
        inputs = self.evaluate_inputs()

        result = bin(sum(inputs))[2:]
        if len(result) == 2:
            self.output_bits[0] = 1
            self.output_bits[1] = int(result[1])
        else:
            self.output_bits[0] = 0
            self.output_bits[1] = int(result[0])


class NBitAdder(base.ComponentBase):
    """
    N-bit adder component. Takes two n-bit numbers (input size specified on
    initialization) and outputs their sum. First output bit is carry bit and
    the rest of the output bits are the sum bits in proper order.

    Example usage:
        >>> from components import sources
        >>> a = NBitAdder(4)
        >>> s = sources.DigitalArbitrary([1, 1, 0, 1, 1, 0, 0, 0])
        >>> a.add_input(s, {i: i for i in xrange(0, 8)})
        >>> a.evaluate()
        >>> a.output_bits
        [1, 0, 1, 0, 1]
    """
    def __init__(self, bits):
        super(NBitAdder, self).__init__('%dAdd' % bits, bits * 2, bits + 1)
        self.bits = bits

    def evaluate(self):
        inputs = self.evaluate_inputs()

        n1 = int(''.join(map(str, inputs[:self.bits])), 2)
        n2 = int(''.join(map(str, inputs[self.bits:])), 2)

        result = bin(n1 + n2)[2:]

        self.output_bits = map(int, result)
        if len(result) == self.bits:
            self.output_bits.insert(0, 0)