from typing import List


def split_list(obj_list: List, sub_size: int = 128) -> List[list]:
    """
    split list
    :param obj_list: list object
    :param sub_size: sub list size
    :return: List[list]

    >>> split_list([], -1)
    []
    >>> split_list([1], -1)
    [[1]]
    >>> split_list([1], 0)
    [[1]]
    >>> split_list([1], 10)
    [[1]]
    >>> split_list([1,2,3,4,5,6,7,8], 10)
    [[1, 2, 3, 4, 5, 6, 7, 8]]
    >>> split_list([1,2,3,4,5,6,7,8], 2)
    [[1, 2], [3, 4], [5, 6], [7, 8]]
    >>> split_list([1,2,3,4,5,6,7,8], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8]]
    >>> split_list([1,2,3,4,5,6,7,8], 6)
    [[1, 2, 3, 4, 5, 6], [7, 8]]
    >>> split_list('你好')
    [['你好']]
    """
    if not isinstance(obj_list, list):
        return [[obj_list]]
    if sub_size < 1:
        sub_size = 1
    return [obj_list[i:i + sub_size] for i in range(0, len(obj_list), sub_size)]
