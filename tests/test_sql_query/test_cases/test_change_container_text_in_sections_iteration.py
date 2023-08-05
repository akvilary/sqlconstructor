import pytest
from sqlconstructor import SqlQuery


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_change_container_text_in_sections_interation():
    q = SqlQuery()
    q['select'](
        'id',
        'name',
    )
    q['from']('product')
    q['where'](
        "quality = 'Best'",
        'and brand_id = 1',
    )
    for section in q:
        # add empty line for "from statement"
        if section.header == 'from':
            # change container's text in place
            section.container.text += '\n'
    end_line = '\n'
    assert str(q()) == end_line.join(
        (
            'SELECT',
            '  id,',
            '  name',
            'FROM',
            '  product\n',
            'WHERE',
            "  quality = 'Best'",
            '  AND brand_id = 1',
        )
    )
