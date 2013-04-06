__author__ = 'Jacky'

from components import base


class ComponentMockZero(base.ComponentBase):
    """
    Mock implementation of ComponentBase, all bits evaluate to 0.
    """
    def __init__(self, name, input_bits, output_bits, *args, **kwargs):
        super(ComponentMockZero, self).__init__(name, input_bits, output_bits, *args, **kwargs)

    def evaluate(self):
        self.output_bits = [0] * len(self.output_bits)


class ComponentMockOne(base.ComponentBase):
    """
    Mock implementation of ComponentBase, all bits evaluate to 1.
    """
    def __init__(self, name, input_bits, output_bits, *args, **kwargs):
        super(ComponentMockOne, self).__init__(name, input_bits, output_bits, *args, **kwargs)

    def evaluate(self):
        self.output_bits = [1] * len(self.output_bits)
