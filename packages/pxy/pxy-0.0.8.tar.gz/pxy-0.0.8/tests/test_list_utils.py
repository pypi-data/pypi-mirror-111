from pxy import split_list


def test_split_list():
    assert split_list([], -1) == []
    assert split_list([1], -1) == [[1]]
    assert split_list([1], 0) == [[1]]
    assert split_list([1], 10) == [[1]]
    assert split_list([1, 2, 3, 4, 5, 6, 7, 8], 10) == [[1, 2, 3, 4, 5, 6, 7, 8]]
    assert split_list([1, 2, 3, 4, 5, 6, 7, 8], 2) == [[1, 2], [3, 4], [5, 6], [7, 8]]
    assert split_list([1, 2, 3, 4, 5, 6, 7, 8], 3) == [[1, 2, 3], [4, 5, 6], [7, 8]]
    assert split_list([1, 2, 3, 4, 5, 6, 7, 8], 6) == [[1, 2, 3, 4, 5, 6], [7, 8]]
    assert split_list('你好') == [['你好']]
