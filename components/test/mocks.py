__author__ = 'Jacky'

from components import base, multigates


class ComponentMockZero(base.ComponentBase):
    """
    Mock implementation of ComponentBase, always evaluates to 0.
    """

    def __init__(self, name, input_bits):
        super(ComponentMockZero, self).__init__(name, input_bits)

    def evaluate(self):
        self.output_bit = 0


class ComponentMockOne(base.ComponentBase):
    """
    Mock implementation of ComponentBase, always evaluates to 1.
    """

    def __init__(self, name, input_bits):
        super(ComponentMockOne, self).__init__(name, input_bits)

    def evaluate(self):
        self.output_bit = 1


class MultiGateAddInputMock(multigates.MultiGateBase):
    """
    Mock implementation of MultiGateBase that just defers to the
    ComponentBase add_input method.
    """

    def __init__(self, name, minimum_input, output_bits):
        super(MultiGateAddInputMock, self).__init__(name, minimum_input,
                                                    output_bits)

    def add_input(self, component, mapping):
        super(MultiGateAddInputMock, self).add_input(component, mapping)
