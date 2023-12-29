import unittest
from crt import Q, CRTInteger, CRTPolynomial
import numpy as np


class TestQ(unittest.TestCase):
    def test_init_q_valid(self):
        qis = [2, 3, 5]
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
        x = 78
        crt_integer = CRTInteger.from_integer(q, x)
        self.assertEqual(crt_integer.recover(), 78)

    def test_add_valid(self):
        qis = [5, 7, 8]
        q = Q(qis)
        xis1 = [3, 1, 6]
        xis2 = [4, 2, 2]
        crt_integer_1 = CRTInteger.from_crt_components(q, xis1)
        crt_integer_2 = CRTInteger.from_crt_components(q, xis2)
        crt_integer_3 = crt_integer_1 + crt_integer_2
        recovered_1 = crt_integer_1.recover()
        recovered_2 = crt_integer_2.recover()
        recovered_3 = crt_integer_3.recover()
        self.assertEqual(recovered_1 + recovered_2 % q.q, recovered_3)

    def test_mul_valid(self):
        qis = [5, 7, 8]
        q = Q(qis)
        xis1 = [3, 1, 6]
        xis2 = [4, 2, 2]
        crt_integer_1 = CRTInteger.from_crt_components(q, xis1)
        crt_integer_2 = CRTInteger.from_crt_components(q, xis2)
        crt_integer_3 = crt_integer_1 * crt_integer_2
        recovered_1 = crt_integer_1.recover()
        recovered_2 = crt_integer_2.recover()
        recovered_3 = crt_integer_3.recover()
        self.assertEqual(recovered_1 * recovered_2 % q.q, recovered_3)


class TestCRTPolynomial(unittest.TestCase):
    def test_from_crt_components_coefficients_valid(
        self,
    ):
        qis = [5, 7, 8]
        q = Q(qis)
        coeff_1 = [3, 1, 6]
        coeff_2 = [4, 2, 2]
        coeffs = [coeff_1, coeff_2]
        crt_poly = CRTPolynomial.from_crt_components_coefficients(q, coeffs)
        self.assertEqual(crt_poly.coefficients[0].recover(), 78)
        self.assertEqual(crt_poly.coefficients[1].recover(), 114)

    def test_from_crt_components_polynomial_valid(
        self,
    ):
        qis = [5, 7, 8]
        q = Q(qis)
        coeff_1 = 78
        coeff_2 = 114
        coeffs = [coeff_1, coeff_2]
        crt_poly = CRTPolynomial.from_int_coefficients(q, coeffs)
        self.assertEqual(crt_poly.coefficients[0].recover(), 78)
        self.assertEqual(crt_poly.coefficients[1].recover(), 114)

    def test_add_valid(self):
        qis = [5, 7, 8]
        q = Q(qis)
        coeff_1 = [3, 1, 6]
        coeff_2 = [4, 2, 2]
        coeffs = [coeff_1, coeff_2]
        crt_poly_1 = CRTPolynomial.from_crt_components_coefficients(q, coeffs)
        crt_poly_2 = CRTPolynomial.from_crt_components_coefficients(q, coeffs)
        poly_1_recovered_coeffs = crt_poly_1.recover()
        poly_2_recovered_coeffs = crt_poly_2.recover()
        poly_1 = np.poly1d(poly_1_recovered_coeffs)
        poly_2 = np.poly1d(poly_2_recovered_coeffs)
        poly_3 = poly_1 + poly_2
        poly_3_coeffs = poly_3.coefficients.tolist()
        poly_3_coeffs = [coeff % q.q for coeff in poly_3_coeffs]
        crt_poly_3 = crt_poly_1 + crt_poly_2
        poly_3_recovered_coeffs = crt_poly_3.recover()
        self.assertEqual(poly_3_recovered_coeffs, poly_3_coeffs)

    def test_mul_valid(self):
        qis = [5, 7, 8]
        q = Q(qis)
        coeff_1 = [3, 1, 6]
        coeff_2 = [4, 2, 2]
        coeffs = [coeff_1, coeff_2]
        crt_poly_1 = CRTPolynomial.from_crt_components_coefficients(q, coeffs)
        crt_poly_2 = CRTPolynomial.from_crt_components_coefficients(q, coeffs)
        poly_1_recovered_coeffs = crt_poly_1.recover()
        poly_2_recovered_coeffs = crt_poly_2.recover()
        poly_1 = np.poly1d(poly_1_recovered_coeffs)
        poly_2 = np.poly1d(poly_2_recovered_coeffs)
        poly_3 = poly_1 * poly_2
        poly_3_coeffs = [coeff % q.q for coeff in poly_3]
        crt_poly_3 = crt_poly_1 * crt_poly_2
        poly_3_recovered_coeffs = crt_poly_3.recover()
        self.assertEqual(poly_3_recovered_coeffs, poly_3_coeffs)


if __name__ == "__main__":
    unittest.main()
