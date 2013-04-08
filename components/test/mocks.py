__author__ = 'Jacky'

from components import base, multigates


class ComponentMockZero(base.ComponentBase):
    """
    Mock implementation of ComponentBase, all bits evaluate to 0.
    """
    def __init__(self, name, input_bits, output_bits):
        super(ComponentMockZero, self).__init__(name, input_bits, output_bits)

    def evaluate(self):
        self.output_bits = [0] * len(self.output_bits)


class ComponentMockOne(base.ComponentBase):
    """
    Mock implementation of ComponentBase, all bits evaluate to 1.
    """
    def __init__(self, name, input_bits, output_bits):
        super(ComponentMockOne, self).__init__(name, input_bits, output_bits)

    def evaluate(self):
        self.output_bits = [1] * len(self.output_bits)


class SourceMock(base.ComponentBase):
    """
    Mock implementation of ComponentBase, bits evaluate to whatever arbitrary list passed in constructor
    """
    def __init__(self, name, input_bits, output_list):
        super(SourceMock, self).__init__(name, input_bits, len(output_list))
        self.output_list = output_list
        self.output_bits = output_list

    def evaluate(self):
        self.output_bits = self.output_list


class MultiGateAddInputMock(multigates.MultiGateBase):
    """
    Mock implementation of MultiGateBase that just defers to the ComponentBase add_input method.
    """
    def __init__(self, name, minimum_input, output_bits):
        super(MultiGateAddInputMock, self).__init__(name, minimum_input, output_bits)

    def add_input(self, component, mapping):
        super(MultiGateAddInputMock, self).add_input(component, mapping)
