#!/usr/bin/env python2.7

import unittest
from solution import solution


class TestSolution(unittest.TestCase):
    def test_something(self):
        self.assertEqual(solution([
            [0, 2, 2, 2, -1], 
            [9, 0, 2, 2, -1], 
            [9, 3, 0, 2, -1], 
            [9, 3, 2, 0, -1], 
            [9, 3, 2, 2, 0],
        ], 1), [1, 2])

        for limit in xrange(1, 5):
            self.assertEqual(solution([
                [0, 1, 1, 1, 1],
                [1, 0, 1, 1, 1],
                [1, 1, 0, 1, 1],
                [1, 1, 1, 0, 1],
                [1, 1, 1, 1, 0],
            ], limit), range(limit - 1))

        # no bunnies
        self.assertEqual(solution([
            [0, 1],
            [1, 0],
        ], 10), [])

        # negative cycle
        self.assertEqual(solution([
            [0, 1, 1, -1, 5],
            [1, 0, 1, 1, 5],
            [1, 1, 0, 1, 5],
            [-1, 1, 1, 0, 5],
            [1, 1, 1, 1, 0],
        ], 0), [0, 1, 2])


if __name__ == '__main__':
    unittest.main()
