import unittest
from crt import Q, CRTInteger, CRTPolynomial
import numpy as np
import random as rand


class TestQ(unittest.TestCase):
    def test_init_q_valid(self):
        qis = [2, 3, 5]
        q = Q(qis)
        self.assertEqual(q.qis, qis)

    def test_init_q_valid_2(self):
        qis = [
            1152921504606584833,
            1152921504598720513,
            1152921504597016577,
            1152921504595968001,
            1152921504595640321,
            1152921504593412097,
            1152921504592822273,
            1152921504592429057,
            1152921504589938689,
            1152921504586530817,
            1152921504585547777,
            1152921504583647233,
            1152921504581877761,
            1152921504581419009,
            1152921504580894721,
        ]
        q = Q(qis)
        self.assertEqual(q.qis, qis)

    def test_init_q_invalid_no_coprime(self):
        qis = [2, 3, 9]
        with self.assertRaisesRegex(AssertionError, "qis are not pairwise coprime"):
            Q(qis)

    def test_init_q_invalid_too_large(self):
        qis = [2, 3, 2**61]
        with self.assertRaisesRegex(AssertionError, "qi is too large"):
            Q(qis)


class TestCRTInteger(unittest.TestCase):
    def test_from_crt_components_valid(
        self,
    ):  # from tutorial https://www.youtube.com/watch?v=zIFehsBHB8o
        qis = [5, 7, 8]
        q = Q(qis)
        xis = [3, 1, 6]
        crt_integer = CRTInteger.from_crt_components(q, xis)
        self.assertEqual(crt_integer.recover(), 78)

    def test_from_integer_valid(self):
        qis = [5, 7, 8]
        q = Q(qis)
        x = rand.randint(0, q.q - 1)
        crt_integer = CRTInteger.from_integer(q, x)
        self.assertEqual(crt_integer.xis, [x % qi for qi in q.qis])
        self.assertEqual(crt_integer.recover(), x)

    def test_add_valid(self):
        qis = [5, 7, 8]
        q = Q(qis)
        x1 = rand.randint(0, q.q - 1)
        x2 = rand.randint(0, q.q - 1)
        crt_integer_1 = CRTInteger.from_integer(q, x1)
        crt_integer_2 = CRTInteger.from_integer(q, x2)
        crt_integer_3 = crt_integer_1 + crt_integer_2

        self.assertEqual((x1 + x2) % q.q, crt_integer_3.recover())

    def test_mul_valid(self):
        qis = [5, 7, 8]
        q = Q(qis)
        x1 = rand.randint(0, q.q - 1)
        x2 = rand.randint(0, q.q - 1)
        crt_integer_1 = CRTInteger.from_integer(q, x1)
        crt_integer_2 = CRTInteger.from_integer(q, x2)
        crt_integer_3 = crt_integer_1 * crt_integer_2
        self.assertEqual((x1 * x2) % q.q, crt_integer_3.recover())


class TestCRTPolynomial(unittest.TestCase):
    def test_from_crt_components_coefficients_valid(
        self,
    ):
        qis = [5, 7, 8]
        q = Q(qis)
        coeff_1_crt_components = [3, 1, 6]
        coeff_2_crt_components = [4, 2, 2]
        coeffs_crt_components = [coeff_1_crt_components, coeff_2_crt_components]
        crt_poly = CRTPolynomial.from_crt_components_coefficients(
            q, coeffs_crt_components
        )
        self.assertEqual(crt_poly.recover(), [78, 114])

    def test_from_crt_components_polynomial_valid(
        self,
    ):
        qis = [5, 7, 8]
        q = Q(qis)
        coeff_1_int = rand.randint(0, q.q - 1)
        coeff_2_int = rand.randint(0, q.q - 1)
        coeffs_int = [coeff_1_int, coeff_2_int]
        crt_poly = CRTPolynomial.from_int_coefficients(q, coeffs_int)
        self.assertEqual(crt_poly.recover(), coeffs_int)

    def test_add_valid(self):
        qis = [5, 7, 8]
        q = Q(qis)
        coeffs_1 = [rand.randint(0, q.q - 1), rand.randint(0, q.q - 1)]
        coeffs_2 = [rand.randint(0, q.q - 1), rand.randint(0, q.q - 1)]
        crt_poly_1 = CRTPolynomial.from_int_coefficients(q, coeffs_1)
        crt_poly_2 = CRTPolynomial.from_int_coefficients(q, coeffs_2)
        crt_poly_3 = crt_poly_1 + crt_poly_2
        poly_1 = np.poly1d(coeffs_1)
        poly_2 = np.poly1d(coeffs_2)
        poly_3 = poly_1 + poly_2
        poly_3_coeffs = poly_3.coefficients.tolist()
        poly_3_coeffs_reduced = [coeff % q.q for coeff in poly_3_coeffs]
        self.assertEqual(crt_poly_3.recover(), poly_3_coeffs_reduced)

    def test_mul_valid(self):
        qis = [5, 7, 8]
        q = Q(qis)
        coeffs_1 = [rand.randint(0, q.q - 1), rand.randint(0, q.q - 1)]
        coeffs_2 = [rand.randint(0, q.q - 1), rand.randint(0, q.q - 1)]
        crt_poly_1 = CRTPolynomial.from_int_coefficients(q, coeffs_1)
        crt_poly_2 = CRTPolynomial.from_int_coefficients(q, coeffs_2)
        crt_poly_3 = crt_poly_1 * crt_poly_2
        poly_1 = np.poly1d(coeffs_1)
        poly_2 = np.poly1d(coeffs_2)
        poly_3 = poly_1 * poly_2
        poly_3_coeffs = poly_3.coefficients.tolist()
        poly_3_coeffs_reduced = [coeff % q.q for coeff in poly_3_coeffs]
        self.assertEqual(crt_poly_3.recover(), poly_3_coeffs_reduced)


if __name__ == "__main__":
    unittest.main()
