__author__ = 'jacky'

from components import base


class LogicGateBase(base.ComponentBase):
    """
    Base class for all basic logic gates, itself a subclass of the ComponentBase class.
    """

    def __init__(self, name, input_bits, output_bits):
        super(LogicGateBase, self).__init__(name, input_bits, output_bits)

    def evaluate(self):
        """
        Called by client classes before evaluation logic to make sure gate has enough input components.
        """
        for i, bit in enumerate(self._input_bits):
            if not bit:
                raise base.MissingInputException(
                    '%s gate requires %d input bits. Bit %d is missing.' % (self.name, len(self._input_bits), i))


class ANDGate(LogicGateBase):
    """
    Basic AND gate.
    """

    def __init__(self):
        super(ANDGate, self).__init__('AND', 2, 1)

    def evaluate(self):
        super(ANDGate, self).evaluate()

        inputs = self.evaluate_inputs()
        self.output_bits[0] = int(inputs[0] and inputs[1])


class ORGate(LogicGateBase):
    """
    Basic OR gate.
    """

    def __init__(self):
        super(ORGate, self).__init__('OR', 2, 1)

    def evaluate(self):
        super(ORGate, self).evaluate()

        inputs = self.evaluate_inputs()
        self.output_bits[0] = int(inputs[0] or inputs[1])


class XORGate(LogicGateBase):
    """
    Basic XOR gate.
    """

    def __init__(self):
        super(XORGate, self).__init__('XOR', 2, 1)

    def evaluate(self):
        super(XORGate, self).evaluate()

        inputs = self.evaluate_inputs()
        self.output_bits[0] = inputs[0] ^ inputs[1]


class NOTGate(LogicGateBase):
    """
    Basic NOT gate.
    """

    def __init__(self):
        super(NOTGate, self).__init__('NOT', 1, 1)

    def evaluate(self):
        super(NOTGate, self).evaluate()

        inputs = self.evaluate_inputs()
        self.output_bits[0] = int(not inputs[0])


class NANDGate(LogicGateBase):
    """
    Basic NAND gate.
    """

    def __init__(self):
        super(NANDGate, self).__init__('NAND', 2, 1)

    def evaluate(self):
        super(NANDGate, self).evaluate()

        inputs = self.evaluate_inputs()
        self.output_bits[0] = int(not (inputs[0] and inputs[1]))


class NORGate(LogicGateBase):
    """
    Basic NOR gate.
    """

    def __init__(self):
        super(NORGate, self).__init__('NOR', 2, 1)

    def evaluate(self):
        super(NORGate, self).evaluate()

        inputs = self.evaluate_inputs()
        self.output_bits[0] = int(not (inputs[0] or inputs[1]))


class XNORGate(LogicGateBase):
    """
    Basic XNOR gate.
    """

    def __init__(self):
        super(XNORGate, self).__init__('XNOR', 2, 1)

    def evaluate(self):
        super(XNORGate, self).evaluate()

        inputs = self.evaluate_inputs()
        self.output_bits[0] = int(not (inputs[0] ^ inputs[1]))