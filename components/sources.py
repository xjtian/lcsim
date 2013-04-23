__author__ = 'Jacky'

from components import base


class DigitalSourceBase(base.ComponentBase):
    """
    Base class for all digital source components. Digital sources are gates
    that map 0->n bits, always outputting the same permutation of bit values.
    """
    def __init__(self, name, output):
        """
        Initialize a new digital source component.
        """
        if any([x != 0 and x != 1 for x in output]):
            raise ValueError('Bits can only be 0 or 1. Invalid value.')

        super(DigitalSourceBase, self).__init__(name, 0, len(output))
        # Keep a private version just in case output_bits is changed somehow.
        self.__exp_output = output
        self.output_bits = output

    def evaluate(self):
        self.output_bits = self.__exp_output


class DigitalZero(DigitalSourceBase):
    """
    Digital source component that always outputs 0.
    """
    def __init__(self):
        super(DigitalZero, self).__init__('D0', [0])


class DigitalOne(DigitalSourceBase):
    """
    Digital source component that always outputs 1.
    """
    def __init__(self):
        super(DigitalOne, self).__init__('D1', [1])


class DigitalArbitrary(DigitalSourceBase):
    """
    Any arbitrary digital source that has no inputs and always outputs a set
    number and arrangement of bits.
    """
    def __init__(self, output):
        super(DigitalArbitrary, self).__init__('DArb', output)
