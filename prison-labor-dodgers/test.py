#!/usr/bin/env python2.7

import unittest
from solution import solution


class TestSolution(unittest.TestCase):
    def test_required(self):
        self.assertEqual(solution([13, 5, 6, 2, 5], [5, 2, 5, 13]), 6)
        self.assertEqual(solution([5, 2, 5, 13], [13, 5, 6, 2, 5]), 6)
        self.assertEqual(solution([14, 27, 1, 4, 2, 50, 3, 1], [2, 4, -4, 3, 1, 1, 14, 27, 50]), -4)
        self.assertEqual(solution([2, 4, -4, 3, 1, 1, 14, 27, 50], [14, 27, 1, 4, 2, 50, 3, 1]), -4)

    def test_other(self):
        self.assertEqual(solution([5], [5, 0]), 0)
        self.assertEqual(solution([5, 0], [5]), 0)
        self.assertEqual(solution([
            -64, -78, -92, -44, -73, -27, -77, 89, -90, 33, -39,
            28, 12, -53, -83, 10, 84, 56, 24, -25, 57, 97,
            95, 28, 93, 80, -30, 72, -100, -9, 51, -46, 50,
            76, -79, 65, -34, -86, 40, 55, 68, 58, -35, -68,
            24, -54, 40, 23, 67, -87, 12, -68, 82, -75, -81,
            50, 13, 8, -89, -94, 3, -85, -44, -81, -93, 67,
            -44, 18, -60, -6, 24, 55, -88, 24, -91, -6, -31,
            66, 30, -59, 91, 73, 44, 19, -27, -21, -30, -81,
            38, -56, 77, 16, 73, 56, -73, 36, -34, 72, 58
        ], [
            -44, -90, 56, 55, 24, 24, 73, 58, -34, 97, -100,
            -35, -9, -86, 82, -81, -77, 50, -81, -30, 58, 30,
            77, 40, 95, -73, -46, 51, -87, 10, 84, -78, 40,
            -21, 65, 66, -93, -25, 38, 68, 13, 93, 55, -30,
            -83, -44, -81, -56, 91, 67, 8, 76, 36, -88, -59,
            73, 80, 44, 28, 56, -92, 24, 12, -27, -75, -6,
            -68, 57, -85, 33, 28, -53, -89, -6, 72, 16, 67,
            -64, -44, -34, -91, -54, -27, 72, 12, 19, -60, 3,
            -68, 50, -79, -39, 89, -94, 24, -31, -73, 23
        ]), 18)

    def test_split(self):
        with self.assertRaises(TypeError):
            solution(1, [1])
        with self.assertRaises(TypeError):
            solution([1], 1)

        with self.assertRaises(ValueError):
            solution([1], [1, 1])
        with self.assertRaises(ValueError):
            solution([1, 1], [1])


if __name__ == '__main__':
    unittest.main()
