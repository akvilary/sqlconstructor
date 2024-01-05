# coding=utf-8
"""
Module of SqlSection class.
"""

from typing import Optional, Any

import sqlconstructor.sql_query as s_q
from .constants import DEFAULT_IND
from .constants import SECTIONS_WITH_COMMA_SEPARATOR, SQL_KEYWORDS
from .sql_container import SqlContainer
from .utils import indent_text, upper_sql_keywords
from .utils.classes.string_convertible import StringConvertible
from .utils.classes.container_convertible import ContainerConvertible
from .sql_bultin_functions import coalesce


class SqlSection(StringConvertible, ContainerConvertible):
    """SqlSection is invented to build one SQL block of query and put the result of
    this process to self.container which is SqlContainer instance.
    SQL block is build of:
        - section header provided of self.header
        - section body which consists of:
            *statements provided in self.__call__ method.
    """

    def __init__(
        self,
        header: str | StringConvertible = '',
        default_kwargs: Optional[dict] = None,
    ):
        """Constract SqlSection instance.
        Params:
            - header: str - could be any string (empty is also possible).
            If it be an empty string then there will be no section header in SQL block,
            and section body will be added without indentation. Otherwise section header
            will be added, and section body starts with new line with default space indentation.
        """
        self.header: str = str(header)
        self.container: Optional[SqlContainer] = None
        self.default_kwargs: dict = default_kwargs if default_kwargs is not None else {}

    def __bool__(self) -> bool:
        """True if self.container is True"""
        return bool(self.container)

    def __str__(self) -> str:
        return str(self.container) if self.container else ''

    def __call__(
        self,
        *statements: Any,  # any objects with __str__ method
        sep: Optional[str] = None,
        header_end: Optional[str] = None,
        line_end: Optional[str] = None,
        section_end: Optional[str] = None,
        # indentation
        header_ind: Optional[int] = None,
        body_ind: Optional[int] = None,
        do_upper_keywords: Optional[bool] = None,
    ) -> SqlContainer:
        """Process building SQL block and put result to self.container and return latter.
        Params:
            - *statements: Iterable[str | SqlContainer] - statements which go to section body.
            - sep: Optional[str] - separator for statements. By default is empty string
            for majority of cases and is comma for special type of statements described in
            SECTIONS_WITH_COMMA_SEPARATOR constant.
            - line_end: str: end of each line. It is '\n' by default.
            - section_end: str - end of SQL block created. It is empty string by default.
            - header_ind: int - indentation for section header. Default=0.
            - body_ind: int - indentation for section body.
            Default is 2 if section header exists else 0.
            - do_upper_keywords: bool - do upper SQL keywords in section header and section body
            or do not. All SQL keywords are registered in SQL_KEYWORDS constant.
        """
        header_end: str = coalesce(
            header_end,
            self.default_kwargs.get('header_end'),
            '\n',
        )
        section_body = form_section_body(
            *statements,
            section_header=self.header,
            sep=coalesce(
                sep,
                self.default_kwargs.get('sep'),
                ',' if self.header.strip().upper() in SECTIONS_WITH_COMMA_SEPARATOR else '',
            ),
            header_end=header_end,
            line_end=coalesce(
                line_end,
                self.default_kwargs.get('line_end'),
                '\n',
            ),
            body_ind=coalesce(
                body_ind,
                self.default_kwargs.get('body_ind'),
            ),
        )

        sql_block = ''
        if self.header:
            header_ind = coalesce(
                header_ind,
                self.default_kwargs.get('header_ind'),
            )
            sql_block += (
                indent_text.indent_lines(
                    str(self.header),
                    ind=header_ind,
                )
                if header_ind
                else str(self.header)
            )
            if section_body:
                sql_block += header_end

        sql_block += section_body + coalesce(
            section_end,
            self.default_kwargs.get('section_end'),
            '',
        )

        if coalesce(
            do_upper_keywords,
            self.default_kwargs.get('do_upper_keywords'),
            True,
        ):
            sql_block = upper_sql_keywords.upper_keywords(sql_block, keywords=SQL_KEYWORDS)

        self.container = SqlContainer(sql_block)

        for statement in statements:
            if isinstance(statement, s_q.SqlQuery):
                statement: SqlContainer = statement()
            if isinstance(statement, SqlContainer):
                self.container.vars.update(statement.vars)

        return self.container


def form_section_body(
    *statements: Any,  # any objects with __str__ method
    section_header: str = '',
    sep: str = '',
    header_end: str = '\n',
    line_end: str = '\n',
    body_ind: Optional[int] = None,
) -> str:
    """
    Form section body as string from statements
    """
    delimiter = sep + line_end

    section_body = ''
    for statement in statements:
        if statement:
            if section_body:
                section_body += delimiter

            calculated_body_ind = calculate_body_ind(
                body_ind,
                section_header,
                header_end,
                line_end,
                section_body,
            )
            if calculated_body_ind:
                body_part = indent_text.indent_lines(
                    str(statement),
                    ind=calculated_body_ind,
                )
            else:
                body_part = str(statement)

            section_body += body_part

    if not (section_header or section_body):
        raise AttributeError(
            'Header or body of sql section is not filled. '
            f'Section header={section_header}, section body={section_body}'
        )

    return section_body


def calculate_body_ind(
    body_ind: Optional[int],
    section_header: Optional[str],
    header_end: str,
    line_end: str,
    section_body: str,
) -> int:
    """
    Calculate_body_ind
    """
    calc_ind = 0
    if section_header:
        if (not line_end.strip(' ') and section_body) or (
            not header_end.strip(' ') and not section_body
        ):
            calc_ind = 0
        else:
            calc_ind = coalesce(body_ind, DEFAULT_IND)
    else:
        calc_ind = coalesce(body_ind, 0)
    return calc_ind
