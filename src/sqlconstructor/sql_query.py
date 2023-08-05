# coding=utf-8
"""
Module of SqlQuery class.
"""

__author__ = 'https://github.com/akvilary'

import uuid
from typing import List, Optional, Type

from .utils import indent_text
from .sql_section import SqlSection
from .sql_container import SqlContainer


class SqlQuery:
    """SqlQuery is a top-level class for constacting SQL query.
    When you start building query or subquery then you create SqlQuery instance first.
    Second you fill the query out by SQL sections.

    Instance of SqlQuery class contains:
        1) self.sections: List[SqlSection] - SQL sections of query.
        Each section has:
            header (like "SELECT", "UPDATE", "WITH some_cte AS" and etc. or empty string)
            and body (continued and related to header SQL statements);

    Notice: if you want to find certain SQL query in your repository by logs later
    then we recommend you to provide sql_id (is any unique string) when you create
    SqlQuery instance. The sql_id will be added at the top of SQL query as comment.
    """

    def __init__(
        self,
        query: Optional[dict] = None,
        *,
        sql_id: Optional[str | uuid.UUID] = '',
    ):
        """Create SqlQuery instance.
        Params:
            - query: Optional[dict] - if you would like to fill query out in one step
            while creating an instance you could provide dictionary to do so.
            It is usefull if query is simple and does not have duplicate headers of SQL blocks.
            If does then it is also possible to provide dict with empty string as key
            like this {'': all_sql_text_as_string} but it is not a constacting SQL in pythonic way.
            If query is complicated then usually query argument is not provided
            and you add as many SQL sections as you like (with nesting subqueries if required)
            later.
            - sql_id: str - any unique string that will be added at the top of the SQL query
            as comment in format "-- sql_id='your_string_here'". It makes possible to find your
            source code after you encounter query in logs or in debuging tools.
        """
        self.sections: List[Optional[SqlSection]] = []

        self.sql_id = sql_id or None
        if self.sql_id:
            self.add(f"-- sql_id='{self.sql_id}'")

        if query:
            for section, value in query.items():
                if isinstance(value, (list, tuple)):
                    self[section](*value)
                elif isinstance(value, dict):
                    nested = dict(value)
                    do_wrap = nested.pop('__do_wrap__', None)
                    wrapper_text = nested.pop('__wrapper_text__', None)
                    sql_id = nested.pop('__sql_id__', None)
                    kwargs = {}
                    if sql_id:
                        kwargs['sql_id'] = sql_id
                    container = SqlQuery(nested, **kwargs)()
                    if do_wrap or isinstance(wrapper_text, str):
                        container.wrap(wrapper_text if isinstance(wrapper_text, str) else '')
                    self[section](container)
                else:
                    self[str(section)](str(value))


    def __bool__(self) -> bool:
        return bool(self.sections)

    def __len__(self) -> int:
        return len(self.sections)

    def __getitem__(self, section_name: str) -> SqlSection:
        """Add SQL section by name of.
        Params:
            - section: str - section name. The name will be header in SqlSection instance.
            Name is not required to be unique.
            You could add as many SQL sections with same header as you like.
        """
        section = SqlSection(section_name)
        self.sections.append(section)
        return section

    def __call__(
        self,
        wrap: Optional[str] = None,
        *,
        ind: int = 0,  # indentation
    ) -> SqlContainer:
        """Build SQL query by sections.
        Params:
            - wrap: str - add wrapper of SQL query. The argument
            usually useful for subqueries which you want to wrap with
            parentheses and optionally add text after parentheses. If wrapper_text is provided
            and is not None then do wrap SQL query with parentheses and add 'wrap' value
            after parentheses (empty string is possible). If you provide an empty string
            in 'wrap' argument then only parentheses will wrap SQL query text.
            - ind : int - you could set additional indentation for each line of query text.
            But it is rarely used because nested subelements automatically add 2 space indentation.
        """
        params = {'text': self.__text(ind=ind)}
        if wrap is not None:
            params['wrapper_text'] = wrap
        container = SqlContainer(**params)

        # inherit all vars of included containers
        for section in self.sections:
            container.vars.update(section.container.vars)
        return container

    def __iter__(self):
        return iter(self.sections)

    def __add__(self, text: str | SqlContainer) -> Type:
        """Add text as sql section and return instance"""
        self.add(text)
        return self

    def add(self, text: str | SqlContainer):
        """Add text as sql section"""
        self[''](text)

    def __text(
        self,
        ind: int = 0,  # indentation
    ) -> str:
        """
        Used in __call__ method.
        Description:
          - Build SQL text by SQL sections and return string (not SqlContainer!).
        Params:
          - ind: int - add additional indentation for each line of SQL query.
        """
        sections = [section.container for section in self.sections if section]
        query_text = '\n'.join(str(x) for x in sections) if sections else ''
        query_text = indent_text.indent_lines(query_text, ind=ind)
        return query_text
