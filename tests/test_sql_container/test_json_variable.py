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
        'set': {'a', 'b'},
        1: uuid_value,
    }
    container = SqlContainer("SELECT $my_dict->'tuple' as names")(my_dict=my_dict)
    assert container.dumps() == (
        'SELECT {'
        '"id": 23, '
        '"list": ["a", "b"], '
        '"tuple": ["a", "b"], '
        '"set": ["a", "b"], '
        f'"1": "{uuid_value}"'
        "}->'tuple' as names"
    )
