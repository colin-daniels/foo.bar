#!/usr/bin/env python2.7

import unittest
from solution import solution


class TestSolution(unittest.TestCase):
    def test_something(self):
        self.assertEqual(solution([0], [3], [
            [0, 7, 0, 0],
            [0, 0, 6, 0],
            [0, 0, 0, 8],
            [9, 0, 0, 0],
        ]), 6)

        self.assertEqual(solution([0, 1], [4, 5], [
            [0, 0, 4, 6, 0, 0],
            [0, 0, 5, 2, 0, 0],
            [0, 0, 0, 0, 4, 4],
            [0, 0, 0, 0, 6, 6],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]), 16)

if __name__ == '__main__':
    unittest.main()
