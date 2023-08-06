__title__ = 'pxy'

__description__ = 'tools of python'
__url__ = 'https://github.com/foyoux/pxy'
__version__ = '0.0.2'
__author__ = 'foyou'
__author_email__ = 'yimi.0822@qq.com'
__license__ = 'GPL-3.0'
__copyright__ = f'Copyright 2021 {__author__}'
__ide__ = 'PyCharm - https://www.jetbrains.com/pycharm/'

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

    """
    if sub_size < 1:
        sub_size = 1
    return [obj_list[i:i + sub_size] for i in range(0, len(obj_list), sub_size)]
