__author__ = 'jacky'

from circuits.sources import digital_source_int_circuit


def h0():
    """
    Returns a digital source circuit that evaluates to the h0 constant.
    """
    return digital_source_int_circuit(0x67452301, 32)


def h1():
    """
    Returns a digital source circuit that evaluates to the h1 constant.
    """
    return digital_source_int_circuit(0xEFCDAB89, 32)


def h2():
    """
    Returns a digital source circuit that evaluates to the h2 constant.
    """
    return digital_source_int_circuit(0x98BADCFE, 32)


def h3():
    """
    Returns a digital source circuit that evaluates to the h3 constant.
    """
    return digital_source_int_circuit(0x10325476, 32)


def h4():
    """
    Returns a digital source circuit that evaluates to the h4 constant.
    """
    return digital_source_int_circuit(0xC3D2E1F0, 32)
