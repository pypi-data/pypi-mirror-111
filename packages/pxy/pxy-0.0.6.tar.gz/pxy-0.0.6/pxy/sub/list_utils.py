from typing import List


def split_list(obj_list: List, sub_size: int = 128) -> List[list]:
    """
    split list
    :param obj_list: list object
    :param sub_size: sub list size
    :return: List[list]
    """
    if not isinstance(obj_list, list):
        return [[obj_list]]
    if sub_size < 1:
        sub_size = 1
    return [obj_list[i:i + sub_size] for i in range(0, len(obj_list), sub_size)]
