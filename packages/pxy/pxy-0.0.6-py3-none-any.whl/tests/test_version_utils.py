from pxy import compare_version, max_version, min_version


def test_compare_version():
    assert compare_version('0.0.3', '0.0.1') == 1
    assert compare_version('0.0.3', '0.0.3') == 0
    assert compare_version('0.0.3', '1.0.1') == -1


def test_max_version():
    assert max_version('0.0.1', '0.2.0', '0.2.0') == '0.2.0'


def test_min_version():
    assert min_version('0.0.1', '0.2.0', '0.2.0') == '0.0.1'
    assert min_version('1.0.1', '0.2.0', '0.2.0') == '0.2.0'
