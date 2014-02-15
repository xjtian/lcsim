from lcsim.components import base

__author__ = 'Jacky'


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
