#!/usr/bin/env python2.7

import unittest
from solution import solution


def solution_naive(l):
    n = len(l)
    triples = 0

    for i in range(n):
        x = l[i]
        for j in range(i + 1, n):
            y = l[j]
            if y % x != 0:
                continue

            for k in range(j + 1, n):
                z = l[k]
                if z % y == 0:
                    triples += 1

    return triples


class TestSolution(unittest.TestCase):
    def test_something(self):
        self.assertEqual(solution([1, 2, 3, 4, 5, 6]), 3)
        self.assertEqual(solution([1, 1, 1]), 1)
        self.assertEqual(solution([1, 3, 5, 7, 11, 13]), 0)

        large_list = [
            397, 161, 933, 824, 600, 445, 606, 634, 549, 290, 617, 536,  77,
            748, 641,  88, 479, 232, 564, 368, 225, 947, 768, 620, 653, 673,
            645, 995, 573,  76, 500, 700, 704, 517, 556, 160, 531, 165, 790,
            581, 700, 699, 432, 216,  56, 741, 357, 350, 281, 500, 841, 294,
            571, 380, 915, 878, 249, 144, 474, 796, 297, 597, 592, 959, 290,
            86, 397, 360, 570, 362, 718, 672, 616, 693, 576, 468, 292, 132,
            811, 688, 531, 892, 304, 124, 937, 162, 100, 287, 262, 718,  19,
            268, 334, 125, 729, 873, 298, 905, 277, 615,  39, 205, 198, 229,
            445, 895, 641, 816, 580, 643, 683, 488, 166, 579, 914,  64, 994,
            92, 391, 526, 932, 685, 262, 305, 108,  67, 993, 784, 830,   4,
            236, 802,  25, 485, 653, 588, 633, 860,  51, 918, 146, 406, 426,
            154, 710,  37, 414, 554, 566, 286,  23, 513,  33, 276, 843, 461,
            371, 573, 244, 682, 942, 991, 157, 389, 950, 921, 152, 887, 135,
            347, 369, 577, 253, 442, 294, 352, 229, 649, 191, 482, 444, 384,
            719, 368, 777, 623, 514, 860, 684,  97, 143, 836, 263, 985, 536,
            788, 942, 573, 993, 184, 682, 957, 173, 777, 648, 271, 977,   8,
            481,  78,  12, 253, 816, 356, 208, 648, 487, 179, 736, 370, 431,
            709, 611, 421, 712, 617,  36, 258, 838, 571,  81, 670, 859, 493,
            107, 352, 555, 346, 136, 542, 883, 545, 629, 663, 863, 400, 770,
            226, 490, 831, 108, 638, 288, 769, 318, 334, 331, 255, 586, 648,
            606,  97, 698, 411, 559, 653, 448, 201, 589, 453, 529,   7, 590,
            213, 705,  93, 883,   3, 938, 831, 756, 162, 991, 748, 381, 182,
            991, 410, 642, 987,  45, 121, 846, 491,  37,  16, 927, 561, 385,
            758, 937, 340, 330, 928, 906, 239, 161, 630, 120, 509, 561, 269,
            730, 916, 590, 153, 147, 438, 519, 268, 675, 452,  43, 520, 617,
            257, 427, 539, 579, 664, 390, 672, 869, 844, 930, 376,  71, 633,
            524, 683, 796, 450, 852,   3,   4, 533, 592, 463, 487, 721, 354,
            30, 630, 774, 196, 229, 747, 741,  14, 360, 823, 955, 460, 660,
            17, 486, 236, 865, 776, 466, 474,  40, 588, 955, 666, 691, 307,
            662, 425, 335, 989, 141,  96, 873, 473, 278, 896, 219, 631, 308,
            252, 163, 453, 529, 660, 602, 289, 363, 490,  55
        ]
        sorted_list = sorted(large_list)

        self.assertEqual(solution(large_list), solution_naive(large_list))
        self.assertEqual(solution(sorted_list), solution_naive(sorted_list))


if __name__ == '__main__':
    unittest.main()
