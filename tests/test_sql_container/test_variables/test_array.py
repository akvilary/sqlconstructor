import pytest

from sqlconstructor import SqlContainer


@pytest.mark.SqlContainer
@pytest.mark.parametrize("my_array", [
    [1, 2],
    (1, 2),
    {1, 2},
])
def test_array_variable(my_array):
    container = SqlContainer('$my_array')(my_array=my_array)
    assert container.dumps() == "ARRAY[1, 2]"


def test_array_variable_case_nested_arrays():
    my_arrays = [['a', 'b'], ['c', 'd']]
    container = SqlContainer('$my_arrays')(my_arrays=my_arrays)
    assert container.dumps() == "ARRAY[ARRAY['a', 'b'], ARRAY['c', 'd']]"


def test_array_variable_strings_case_single_quotes():
    my_array = ['a', 'b']
    container = SqlContainer('$my_array')(my_array=my_array)
    assert container.dumps() == "ARRAY['a', 'b']"


def test_array_variable_strings_case_double_quotes():
    my_array = ["a", "b"]
    container = SqlContainer('$my_array')(my_array=my_array)
    assert container.dumps() == "ARRAY['a', 'b']"
