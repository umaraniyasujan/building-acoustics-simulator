import unittest
from app import sabine_rt60

class SabineTests(unittest.TestCase):
    def test_known_case(self):
        # V=100 m3, A=10 m2 sabin => RT60=1.61 s
        v, a, rt = sabine_rt60(10, 5, 2, [("all", 10, 1)])
        self.assertAlmostEqual(v, 100)
        self.assertAlmostEqual(a, 10)
        self.assertAlmostEqual(rt, 1.61)

    def test_rejects_invalid_alpha(self):
        with self.assertRaises(ValueError):
            sabine_rt60(4, 5, 2, [("wall", 20, 1.2)])

    def test_rejects_zero_absorption(self):
        with self.assertRaises(ValueError):
            sabine_rt60(4, 5, 2, [("wall", 20, 0)])

if __name__ == "__main__":
    unittest.main()
