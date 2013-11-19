import unittest

from circuits.sources import digital_source_int_circuit
from sha1.builder import block_operation


class TestBlockOperation(unittest.TestCase):
    def test_function(self):
        # Each chunk is 512 bits
        # From random.org
        chunk = 0x25afbbc1415e115f68b57be44bd10a75f90d7bec20c24bfce34a1a34409b7f9373496da68e4db94e9bc60f07a9d435fe40a8c4cf41b11d5fcc09d11878d653cb


        chunk_circuit = digital_source_int_circuit(chunk, 512)
        h0 = digital_source_int_circuit(0x67452301, 32)
        h1 = digital_source_int_circuit(0xEFCDAB89, 32)
        h2 = digital_source_int_circuit(0x98BADCFE, 32)
        h3 = digital_source_int_circuit(0x10325476, 32)
        h4 = digital_source_int_circuit(0xC3D2E1F0, 32)

        nh0, nh1, nh2, nh3, nh4 = block_operation(chunk_circuit, h0, h1, h2, h3, h4)
