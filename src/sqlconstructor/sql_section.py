# coding=utf-8
"""
Module of SqlSection class.
"""

from typing import Optional, Any

from .utils import indent_text, upper_sql_keywords
from .constants import SECTIONS_WITH_COMMA_SEPARATOR, SQL_KEYWORDS
from .sql_container import SqlContainer


class SqlSection:
    """SqlSection is invented to build one SQL block of query and put the result of
    this process to self.container which is SqlContainer instance.
    SQL block is build of:
        - section header provided of self.header
        - section body which consists of:
            *statements provided in self.__call__ method.
    """

    def __init__(self, header: str = ''):
        """Constract SqlSection instance.
        Params:
            - header: str - could be any string (empty is also possible).
            If it be an empty string then there will be no section header in SQL block,
            and section body will be added without indentation. Otherwise section header
            will be added, and section body starts with new line with 2 space indentation.
        """
        self.header: str = header
        self.container: Optional[SqlContainer] = None

    def __bool__(self) -> bool:
        """True if self.container is True"""
        return bool(self.container)

    def __call__(
        self,
        *statements: Any,  # any objects with __str__ method
        sep: Optional[str] = None,
        line_end: str = '\n',
        section_end: str = '',
        ind: int = 2,  # indentation
        upper_keywords: bool = True,
    ) -> SqlContainer:
        """Process building SQL block and put result to self.container and return latter.
        Params:
            - *statements: Iterable[str | SqlContainer] - statements which go to section body.
            - sep: Optional[str] - separator for statements. By default is empty string
            for majority of cases and is comma for special type of statements described in
            SECTIONS_WITH_COMMA_SEPARATOR constant.
            - line_end: str: end of each line. It is '\n' by default.
            - section_end: str - end of SQL block created. It is empty string by default.
            - ind: int - indentation of each line of section body. If section header is not empty
            string then each line of section body will be indented for 2 spaces.
            No indentation overwise.
            - upper_keywords: bool - do upper SQL keywords in section header and section body
            or do not. All SQL keywords are registered in SQL_KEYWORDS constant.
        """
        sep = (
            sep
            if sep is not None
            else ','
            if self.header.upper() in SECTIONS_WITH_COMMA_SEPARATOR
            else ''
        )
        delimiter = sep + line_end

        section_body = delimiter.join(
            # if self.section_name == '' then do not indent
            indent_text.indent_lines(str(x), ind=ind) if self.header else str(x)
            for x in statements
            if x
        )

        if not (self.header or section_body):
            raise AttributeError(
                'Header or body of sql section is not filled. '
                f'Section header={self.header}, section body={section_body}'
            )

        sql_block = ''
        if self.header:
            sql_block += self.header + '\n'
        sql_block += section_body + section_end

        if upper_keywords:
            sql_block = upper_sql_keywords.upper_keywords(sql_block, keywords=SQL_KEYWORDS)

        self.container = SqlContainer(sql_block)

        for statement in statements:
            if isinstance(statement, SqlContainer):
                self.container.vars.update(statement.vars)

        return self.container
