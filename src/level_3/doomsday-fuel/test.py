#!/usr/bin/env python2.7

import unittest
from solution import solution


class TestSolution(unittest.TestCase):
    def test_something(self):
        self.assertEqual(solution([
            [0, 2, 1, 0, 0],
            [0, 0, 0, 3, 4],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]), [7, 6, 8, 21])

        self.assertEqual(solution([
            [0, 1, 0, 0, 0, 1],
            [4, 0, 0, 3, 2, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ]), [0, 3, 2, 9, 14])

        # sanity checks
        self.assertEqual(solution([
            [0, 1],
            [0, 0],
        ]), [1, 1])

        self.assertEqual(solution([
            [0, 1, 1],
            [1, 0, 1],
            [0, 0, 0],
        ]), [1, 1])

        self.assertEqual(solution([
            [0, 3, 7],
            [0, 0, 0],
            [0, 0, 0],
        ]), [3, 7, 10])

        self.assertEqual(solution([
            [0, 1, 1, 1],
            [1, 0, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]), [1, 1, 2])

        self.assertEqual(solution([
            [0, 1, 1, 0, 0],
            [0, 0, 0, 1, 3],
            [0, 0, 0, 1, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]), [3, 5, 8])


if __name__ == '__main__':
    unittest.main()
