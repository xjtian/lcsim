__author__ = 'Jacky'

from components import base


class DigitalZero(base.ComponentBase):
    """
    Digital source component that always outputs 0.
    """
    def __init__(self):
        super(DigitalZero, self).__init__('D0', 0, 1)
        self.output_bits[0] = 0

    def evaluate(self):
        self.output_bits[0] = 0


class DigitalOne(base.ComponentBase):
    """
    Digital source component that always outputs 1.
    """
    def __init__(self):
        super(DigitalOne, self).__init__('D1', 0, 1)
        self.output_bits[0] = 1

    def evaluate(self):
        self.output_bits[0] = 1
