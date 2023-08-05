import pytest
from sqlconstructor import SqlSection


@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_upper_keywords_in_select():
    section = SqlSection('')
    line = 'select some'
    section(line)
    assert str(section.container) == 'SELECT SOME'


@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_do_not_upper_between_single_quotes():
    section = SqlSection('')
    line = "select 'some'"
    section(line)
    assert str(section.container) == "SELECT 'some'"


@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_do_not_upper_between_single_quotes_if_keyword_in_middle():
    section = SqlSection('')
    line = "select 'abc some xyz'"
    section(line)
    assert str(section.container) == "SELECT 'abc some xyz'"


@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_do_not_upper_between_double_quotes():
    section = SqlSection('')
    line = 'select "some"'
    section(line)
    assert str(section.container) == 'SELECT "some"'


@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_do_not_upper_between_double_quotes_if_keyword_in_middle():
    section = SqlSection('')
    line = 'select "abc some xyz"'
    section(line)
    assert str(section.container) == 'SELECT "abc some xyz"'


@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_do_not_upper_keyword_in_inline_sql_comment_which_starts_with_keyword():
    section = SqlSection('')
    inline_comment = '-- some comment here'
    section(inline_comment)
    assert str(section.container) == inline_comment


@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_do_not_upper_keyword_in_inline_sql_comment_if_keyword_in_middle_of_comment():
    section = SqlSection('')
    inline_comment = '-- comment some here'
    section(inline_comment)
    assert str(section.container) == inline_comment


@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_upper_keywords_in_select_and_do_not_upper_in_inline_comment():
    section = SqlSection('')
    line = 'select some -- comment some here'
    section(line)
    assert str(section.container) == 'SELECT SOME -- comment some here'


@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_do_not_upper_keyword_in_multiline_sql_comment_which_starts_with_keyword():
    section = SqlSection('')
    multiline_comment = '/*\n some comment here\n */'
    section(multiline_comment)
    assert str(section.container) == multiline_comment


@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_do_not_upper_keyword_in_multiline_sql_comment_where_keyword_in_middle():
    section = SqlSection('')
    multiline_comment = '/*\n comment some here\n */'
    section(multiline_comment)
    assert str(section.container) == multiline_comment
