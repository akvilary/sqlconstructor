import pytest
from sqlconstructor import SqlCase


@pytest.mark.SqlCase
def test_str():
    sql_case = SqlCase(('b=1', "'one'"), ('b=2', "'two'"), "'nothing'")
    assert str(sql_case) == '\n'.join(
        (
            'CASE',
            '  WHEN',
            '    b=1',
            '  THEN',
            "    'one'",
            '  WHEN',
            '    b=2',
            '  THEN',
            "    'two'",
            '  ELSE',
            "    'nothing'",
            'END',
        )
    )
