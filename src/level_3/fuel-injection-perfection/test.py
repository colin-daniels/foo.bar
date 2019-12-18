#!/usr/bin/env python2.7

import unittest
from solution import solution


def solution_naive(n):
    n = long(n)

    if n == 1:
        return 0
    elif n % 2 == 0:
        return 1 + solution_naive(n // 2)
    else:
        return min(
            1 + solution_naive(n + 1),
            1 + solution_naive(n - 1),
        )


class TestSolution(unittest.TestCase):
    def test_something(self):
        for i in range(1, 2048):
            self.assertEqual(solution_naive(i), solution(i), msg="mismatch: {} [{:b}]".format(i, i))

        self.assertEqual(solution("4"), 2)
        self.assertEqual(solution("15"), 5)
        self.assertEqual(solution("31"), 6)
        self.assertEqual(solution("63"), 7)
        self.assertEqual(solution("72357"), 23)
        self.assertEqual(solution("7263413578"), 44)


if __name__ == '__main__':
    unittest.main()
