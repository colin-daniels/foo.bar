import java.util.Arrays;

public class Solution {
    /**
     * @param h Height of the perfect tree of converters, must be greater than 0 and less than 31.
     * @param q A list of positive integers representing different flux converters, must be less than 2^h.
     * @return A list of integers p where each element in p is the label of the converter that sits on top of the
     *   respective converter in q, or -1 if there is no such converter.
     */
    public static int[] solution(int h, int[] q) {
        // root node label is 2^h - 1
        int root = (2 << (h - 1)) - 1;

        // Just go ahead and calculate the parents for each number.
        // Note that we just use a regular for loop and don't do any input
        // validation because Commander Lambda loves efficiency, etc etc.
        int[] parents = new int[q.length];
        for (int i = 0; i < parents.length; i++) {
            int n = q[i];
            if (n == root) {
                parents[i] = -1;
            } else {
                parents[i] = calculateParentLabel(n);
            }
        }

        return parents;
    }


    /**
     * @param n Post-order traversal node label, must be greater than 0 and less than 2^31 - 1.
     * @return Parent node label.
     */
    static int calculateParentLabel(int n) {
        // Consider the following perfectly-balanced binary tree of height 4 that has
        // nodes labeled by post-order traversal:
        //
        //                15
        //         7              14
        //     3       6      10      13
        //   1   2   4   5   8   9  11  12
        //
        // We consider the problem of finding the difference between a node's parent
        // label and its own. In particular we establish two base cases,
        //
        //   1. The immediate left child of the root (difference is n + 1, e.g. 7 + 8 = 15).
        //   2. The immediate right child of the root (difference is 1, e.g. 14 + 1 = 15).
        //
        // What about other nodes? Well, we can take advantage of two things,
        //
        //   1. Parent node labels don't depend on tree height (except for the root).
        //   2. Labels of the right subtree are identical to the left, except they are offset
        //      by the size of the left subtree, e.g.,
        //
        //                                       15
        //                   7                                       (7+7)
        //         3                   6                   (3+7)               (6+7)
        //    1         2         4         5         (1+7)     (2+7)     (4+7)     (5+7)
        //
        // So to find the parent node id we can just do:
        int x = n;
        while (true) {
            // Find the largest Mersenne number that is less than x (note we need to deal
            // with two's complement, so we don't use 0xFFFFFFFF)
            int closestMersenne = 0x7FFFFFFF >> Integer.numberOfLeadingZeros(x);
            // We're done if x is either (2 * closestMersenne) or (2 * closestMersenne + 1)
            if (x >> 1 == closestMersenne) {
                if ((x & 1) == 0) {
                    // If x is even, we're a right child.
                    return n + 1;
                } else {
                    // If x is odd, we're a left child.
                    return n + (x + 1);
                }
            } else {
                // Shift x until we get to the "leftmost" tree.
                x = x - closestMersenne;
            }
        }
    }
    
    public static void main(String[] args) {
        assert Arrays.equals(solution(5, new int[]{19, 14, 28}), new int[]{21, 15, 29});
        assert Arrays.equals(solution(3, new int[]{7, 3, 5, 1}), new int[]{-1, 7, 6, 3});
    }
}
