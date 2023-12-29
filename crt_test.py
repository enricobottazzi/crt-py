import unittest
from crt import Q


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


if __name__ == "__main__":
    unittest.main()
