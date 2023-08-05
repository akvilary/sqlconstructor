import pytest
from sqlconstructor import SqlSection

SECTION_HEADER = 'select'


@pytest.mark.SqlSection
def test_init_with_no_header():
    section = SqlSection()
    assert section.header == ''
    assert section.container is None


@pytest.mark.SqlSection
@pytest.mark.parametrize("args, kwargs", [
    ([SECTION_HEADER], {}),
    ([], {'header': SECTION_HEADER}),
])
def test_init_with_section_header(args, kwargs):
    section = SqlSection(*args, **kwargs)
    assert section.header == SECTION_HEADER
    assert section.container is None
