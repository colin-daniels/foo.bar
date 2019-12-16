def solution(l):
    """
    Given a list of elevator versions represented as strings, returns the same list sorted in
    ascending order by major, minor, and revision number.

    Warnings:
        Since Commander Lambda loves efficiency, essentially no input checking is done.

    Args:
        l: List of version strings.

    Returns:
        Sorted version strings.
    """
    # Convert version strings to lists of version numbers (e.g. "1.2.0" -> [1, 2, 0]),
    # then just let python sort the list according to lexicographical ordering.
    return sorted(l, key=lambda version: [int(n) for n in version.split(".")])
