import math
from typing import List


class Q:
    def __init__(self, qis: List[int]):
        q = 1
        # qis should be same size single precision integers of 60 bits (or less)
        for qi in qis:
            assert isinstance(qi, int)
            assert qi.bit_length() <= 60, "qi is too large"
            q *= qi

        # qis should be coprime
        for i in range(len(qis)):
            for j in range(i + 1, len(qis)):
                assert math.gcd(qis[i], qis[j]) == 1, "qis are not pairwise coprime"

        self.qis = qis
        self.q = q


class CRTInteger:
    def __init__(self, q: Q, xis: List[int]):
        self.q = q
        self.xis = xis

    def from_crt_components(q: Q, xis: List[int]):
        return CRTInteger(q, xis)

    def from_integer(q: Q, x: int):
        xis = []
        for qi in q.qis:
            xis.append(x % qi)

        return CRTInteger(q, xis)

    def recover(self):
        x = 0
        for i in range(len(self.q.qis)):
            xi = self.xis[i]
            qi_star = self.q.q // self.q.qis[i]
            qi_tilde = pow(
                qi_star, -1, self.q.qis[i]
            )  # inverse of qi_star mod self.q.qis[i]
            x += xi * qi_star * qi_tilde

        return x % self.q.q

    def __add__(self, other):
        assert isinstance(other, CRTInteger)
        assert self.q == other.q, "q is not the same"
        assert len(self.xis) == len(other.xis), "xis are not the same size"

        xis = []
        for i in range(len(self.xis)):
            xis.append((self.xis[i] + other.xis[i]) % self.q.qis[i])

        return CRTInteger(self.q, xis)

    def __mul__(self, other):
        assert isinstance(other, CRTInteger)
        assert self.q == other.q, "q is not the same"
        assert len(self.xis) == len(other.xis), "xis are not the same size"

        xis = []
        for i in range(len(self.xis)):
            xis.append((self.xis[i] * other.xis[i]) % self.q.qis[i])

        return CRTInteger(self.q, xis)


class CRTPolynomial:
    def __init__(self, q: Q, coefficients: List[CRTInteger]):
        self.q = q
        self.coefficients = coefficients

    def from_crt_components_coefficients(
        q: Q, coefficients_crt_componenents: List[List[int]]
    ):
        coefficients = []
        for coefficient_crt_components in coefficients_crt_componenents:
            coefficients.append(
                CRTInteger.from_crt_components(q, coefficient_crt_components)
            )

        return CRTPolynomial(q, coefficients)

    def from_int_coefficients(q: Q, coefficients_int: List[int]):
        coefficients = []
        for coefficient_int in coefficients_int:
            coefficients.append(CRTInteger.from_integer(q, coefficient_int))

        return CRTPolynomial(q, coefficients)

    def recover(self):
        coefficients = []
        for i in range(len(self.coefficients)):
            coefficients.append(self.coefficients[i].recover())

        return coefficients

    def __add__(self, other):
        assert isinstance(other, CRTPolynomial)
        assert self.q == other.q, "q is not the same"
        assert len(self.coefficients) == len(
            other.coefficients
        ), "coefficients are not the same size"

        coefficients = []
        for i in range(len(self.coefficients)):
            coefficients.append(self.coefficients[i] + other.coefficients[i])

        return CRTPolynomial(self.q, coefficients)

    def __mul__(self, other):
        assert isinstance(other, CRTPolynomial)
        assert self.q == other.q, "q is not the same"
        assert len(self.coefficients) == len(
            other.coefficients
        ), "coefficients are not the same size"

        coefficients = []
        for i in range(len(self.coefficients)):
            for j in range(len(self.coefficients)):
                if i + j < len(coefficients):
                    coefficients[i + j] += self.coefficients[i] * other.coefficients[j]
                else:
                    coefficients.append(self.coefficients[i] * other.coefficients[j])

        return CRTPolynomial(self.q, coefficients)