from lcsim.components import base

__author__ = 'Jacky'


class DigitalSourceBase(base.ComponentBase):
    """
    Base class for all digital source components. Digital sources are gates
    that map 0->n bits, always outputting the same permutation of bit values.
    """
    def __init__(self, name, output):
        """
        Initialize a new digital source component.
        """
        if output != 0 and output != 1:
            raise ValueError('Bits can only be 0 or 1. Invalid value %d.' % output)

        super(DigitalSourceBase, self).__init__(name, 0)

        # Keep a private version just in case output_bits is changed somehow.
        self.__exp_output = output
        self.output_bit = output

    def evaluate(self):
        self.output_bit = self.__exp_output


class DigitalZero(DigitalSourceBase):
    """
    Digital source component that always outputs 0.
    """
    def __init__(self):
        super(DigitalZero, self).__init__('D0', 0)


class DigitalOne(DigitalSourceBase):
    """
    Digital source component that always outputs 1.
    """
    def __init__(self):
        super(DigitalOne, self).__init__('D1', 1)
