#!/usr/bin/env python2.7

import unittest
from solution import solution
import math


def naive(u, n):
    return sum((long(n * u) for n in xrange(n + 1)))


class TestSolution(unittest.TestCase):
    def test_something(self):
        for n in range(1, 1000):
            self.assertEqual(str(naive(math.sqrt(2), n)),
                             solution(str(n)))

        self.assertEqual(
            solution(10**100),
            "70710678118654752440084436210484903928483593768"
            "84740365883398689953662392310535194251937671638"
            "20786388217601234110900952546854238410272534805"
            "65451739737157454059823250037671948325191776995"
            "310741236436"
        )
        # self.assertEqual("7071067832576154", solution(str(100000000)))
        # self.assertEqual("28284271288883260", solution(str(200000000)))


if __name__ == '__main__':
    unittest.main()
