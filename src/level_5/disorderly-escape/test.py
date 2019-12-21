#!/usr/bin/env python2.7

import unittest
from solution import solution


class TestSolution(unittest.TestCase):
    def test_something(self):
        self.assertEqual(solution(2, 2, 2), "7")

        self.assertEqual(solution(3, 3, 3), "738")
        self.assertEqual(solution(3, 4, 3), "5053")

        self.assertEqual(solution(1, 1, 4), "4")
        self.assertEqual(solution(2, 1, 4), "10")
        self.assertEqual(solution(2, 2, 4), "76")
        self.assertEqual(solution(2, 3, 4), "430")
        self.assertEqual(solution(2, 4, 4), "1996")
        self.assertEqual(solution(4, 2, 4), "1996")
        self.assertEqual(solution(3, 4, 4), "131505")
        self.assertEqual(solution(4, 3, 4), "131505")


if __name__ == '__main__':
    unittest.main()
