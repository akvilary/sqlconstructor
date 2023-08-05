import pytest
import uuid

from sqlconstructor import SqlContainer


@pytest.mark.SqlContainer
def test_json_variable():
    uuid_value = uuid.uuid4()
    my_dict = {'id': 23, 'names': ['xo', 'ox'], 1: uuid_value}
    container = SqlContainer("SELECT $my_dict->'names' as names")(my_dict=my_dict)
    assert (
        container.dumps()
        == (
        "SELECT json_build_object("
        f"'id', 23, 'names', ARRAY['xo', 'ox'], 1, '{uuid_value}'"
        ")->'names' as names"
        )
    )
