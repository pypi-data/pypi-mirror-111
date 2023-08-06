def compare_version(v1: str, v2: str):
    """
    标准版本号比较
    :param v1:
    :param v2:
    :return: v1>v2 返回1, v1<v2 返回v1<v2, 否则返回0
    """

    v1l = v1.split('.')
    v2l = v2.split('.')

    for i in range(3):
        i1 = int(v1l[i])
        i2 = int(v2l[i])
        if i1 == i2:
            continue
        if i1 > i2:
            return 1
        else:
            return -1

    return 0


def max_version(*args):
    """

    :param args:
    :return:
    """
    max = None
    for arg in args:
        if max is None:
            max = arg
            continue
        if compare_version(max, arg) == -1:
            max = arg
    return max


def min_version(*args):
    """

    :param args:
    :return:
    """
    min = None
    for arg in args:
        if min is None:
            min = arg
            continue
        if compare_version(min, arg) == 1:
            min = arg
    return min
