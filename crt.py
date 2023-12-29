import math


class Q:
    def __init__(self, qis: list):
        # qis should be same size single precision integers of 60 bits (or less)
        for qi in qis:
            assert isinstance(qi, int)
            assert qi.bit_length() <= 60, "qi is too large"

        # assert that qis are pairwise coprime
        for i in range(len(qis)):
            for j in range(i + 1, len(qis)):
                assert math.gcd(qis[i], qis[j]) == 1, "qis are not pairwise coprime"

        self.qis = qis
