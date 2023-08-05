import pytest
import uuid

from sqlconstructor import SqlContainer


@pytest.mark.SqlContainer
def test_json_variable():
    uuid_value = uuid.uuid4()
    my_dict = {
        'id': 23,
        'list': ['a', 'b'],
        'tuple': ('a', 'b'),
        'set': {1, 2},
        1: uuid_value,
    }
    container = SqlContainer("SELECT $my_dict::json->'tuple' as names")(my_dict=my_dict)
    assert container.dumps() == (
        'SELECT {'
        '"id": 23, '
        '"list": ["a", "b"], '
        '"tuple": ["a", "b"], '
        '"set": [1, 2], '
        f'"1": "{uuid_value}"'
        "}::json->'tuple' as names"
    )
