import pytest
import uuid

from sqlconstructor import SqlContainer, SqlVal, SqlCol


@pytest.mark.SqlContainer
@pytest.mark.SqlVal
@pytest.mark.SqlCol
def test_json_variable():
    uuid_value = uuid.uuid4()
    my_dict = {
        'id': 23,
        'list': ['a', 'b'],
        'tuple': ('a', 'b'),
        'set': {1, 2},
        1: uuid_value,
        'container': SqlContainer('a'),
        'val': SqlVal('a'),
        'col': SqlCol('a'),
    }
    container = SqlContainer("SELECT $my_dict::json->'tuple' as names")(my_dict=my_dict)

    assert container.dumps() == (
        "SELECT E'{"
        '"id": 23, '
        '"list": ["a", "b"], '
        '"tuple": ["a", "b"], '
        '"set": [1, 2], '
        f'"1": "{uuid_value}", '
        '"container": "a", '
        '"val": "\\\'a\\\'", '
        '"col": "\\\\"a\\\\""'
        "}'::json->'tuple' as names"
    )
