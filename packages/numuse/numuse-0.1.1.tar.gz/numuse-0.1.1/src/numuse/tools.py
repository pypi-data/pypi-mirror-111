
def I(x: int, y: int) -> int:
    """Return the interval between the musical objects

    The interval between two notes is the number you have to
    add to the first to get the second

    :param x: The base note
    :type x: Note

    :param y: The secondary note
    :type y: Note


    :return: The interval between x and y
    :rtype: int
    """
    return y - x


def ranged_modulus_operator(x: int, m: int = 12) -> int:
    """Return what x is congruent to in the range 0 ... m-1

    :param x: The number to be converted
    :type x: int

    :param m: The modulus
    :type m: int

    :return: The unique number from 0 to m-1 (inclusive) that x is congruent to
    :rtype: int
    """
    while x < 0:
        x += m

    return x % m
