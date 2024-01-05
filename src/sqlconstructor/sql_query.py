# coding=utf-8
"""
Module of SqlQuery class.
"""

__author__ = 'https://github.com/akvilary'

import uuid
from typing import Optional, Type, Self
from collections import UserList, UserDict

from .sql_section import SqlSection
from .sql_container import SqlContainer
from .utils.classes.string_convertible import StringConvertible
from .utils.classes.container_convertible import ContainerConvertible


class SqlQuery(StringConvertible, UserList):
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
        **sections_default_kwargs,
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
            - sections_default_kwargs - default kwwargs for all future sections of query such as
            sep, line_end, section_end, header_ind, body_ind, do_upper_keywords.
        """
        UserList.__init__(self)
        self.sections_default_kwargs = sections_default_kwargs

        self.ctes = SqlCte()

        self.sql_id = sql_id or None
        if self.sql_id:
            self.add(f"-- sql_id='{self.sql_id}'")

        if query:
            add_sections_by_dict(self, query)

    def __getitem__(self, item: str | int | slice) -> SqlSection | Self:
        """Add SQL section by name of.
        Params:
            - section: str - section name. The name will be header in SqlSection instance.
            Name is not required to be unique.
            You could add as many SQL sections with same header as you like.
        """
        if isinstance(item, int):
            return self.data[item]
        if isinstance(item, slice):
            query = SqlQuery()
            query.data = self.data[item]
            return query
        section = SqlSection(item, self.sections_default_kwargs)
        self.append(section)
        return section

    def __call__(
        self,
        wrap: Optional[str] = None,
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
        container = SqlContainer(self.__to_text())
        if wrap is not None:
            container.wrap(wrap)

        # inherit all vars of included containers
        for section in self:
            container.vars.update(section.container.vars)

        return container

    def __iadd__(self, text: str | SqlContainer) -> Type:
        """Add text as sql section and return instance"""
        self.add(text)
        return self

    def __str__(self):
        return str(self())

    def __len__(self):
        return len(self.ctes) + len(self.data)

    def add(
        self,
        data: str | SqlContainer | dict,
        ind: int = 0,
    ):
        """Add data as sql section"""
        if isinstance(data, dict):
            add_sections_by_dict(self, data, ind=ind)
        else:
            self[''](data, **self.sections_default_kwargs).indent(ind)

    def __to_text(
        self,
    ) -> str:
        """
        Used in __call__ method.
        Description:
          - Build SQL text by SQL sections and return string (not SqlContainer!).
        Params:
          - ind: int - add additional indentation for each line of SQL query.
        """
        sections = []
        if self.ctes:
            sections.append(self.ctes())

        sections += [section.container for section in self if section]
        query_text = '\n'.join(str(x) for x in sections) if sections else ''
        return query_text


def add_sections_by_dict(
    query: SqlQuery,
    data: dict,
    *,
    ind: int = 0,
):
    """
    Add SqlSections by dict to SqlQuery
    """
    section_data = dict(data)
    section_kwargs = query.sections_default_kwargs | {
        x: kwarg
        for x in (
            'header_end',
            'sep',
            'line_end',
            'section_end',
            'header_ind',
            'body_ind',
            'do_upper_keywords',
        )
        if (kwarg := section_data.pop('__' + x + '__', None)) is not None
    }
    for section_header, value in section_data.items():
        if isinstance(value, (tuple, list)):
            query[section_header](*value, **section_kwargs).indent(ind)
        elif isinstance(value, dict):
            add_section_by_dict(query, value, section_header, ind=ind)
        else:
            query[section_header](value, **section_kwargs).indent(ind)


def add_section_by_dict(
    query: SqlQuery,
    data: dict,
    section_header: str = '',
    *,
    ind: int = 0,
):
    """
    Add SqlSection by dict to SqlQuery
    """
    subquery_dict = dict(data)
    is_cte = subquery_dict.pop('__is_cte__', None)
    if section_header == '__ctes__':
        for cte_name, cte_dict in subquery_dict.items():
            container = form_container_by_dict(cte_dict).indent(ind)
            query.ctes[cte_name] = container
    else:
        container = form_container_by_dict(subquery_dict)
        container.indent(ind)
        if is_cte:
            query.ctes[section_header] = container
        else:
            query[section_header](container)


def form_container_by_dict(
    subquery_dict: dict,
) -> SqlContainer:
    """
    Form container by dict
    """
    do_wrap = subquery_dict.pop('__do_wrap__', None)
    wrapper_text = subquery_dict.pop('__wrapper_text__', None)
    sql_id = subquery_dict.pop('__sql_id__', None)

    kwargs = {}
    if sql_id:
        kwargs['sql_id'] = sql_id
    container = SqlQuery(subquery_dict, **kwargs)()

    if do_wrap or isinstance(wrapper_text, str):
        container.wrap(wrapper_text if isinstance(wrapper_text, str) else '')

    return container


###################################################################################################
# Because of circular dependency we need to pass SqlCte here
###################################################################################################


class SqlCte(UserDict, StringConvertible, ContainerConvertible):
    """
    SqlCte class is invented for better experience with filling cte queries.
    It is possible to register cte and fill it after.
    Or you could add filled query as cte instantly.
    Now it is your choice!
    """

    def __init__(
        self,
        *args,
        sql_id: Optional[str | uuid.UUID] = '',
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.sql_id = sql_id

    def __setitem__(self, key, item):
        if isinstance(item, dict):
            item = copy_cte_dict(item)
        UserDict.__setitem__(self, key, item)

    def __call__(self, **kwargs) -> SqlContainer:
        result = SqlQuery(sql_id=self.sql_id) if self.sql_id else SqlQuery()
        ctes_size = len(self)
        for counter, (cte_name, cte) in enumerate(self.items()):
            if counter == 0:
                sql_section_header = f'with {cte_name} as'
                wrapper_text = ',' if ctes_size > (counter + 1) else ''
                add_cte_section(result, cte, sql_section_header, wrapper_text)
            else:
                sql_section_header = f'{cte_name} as'
                wrapper_text = '' if ctes_size == (counter + 1) else ','
                add_cte_section(result, cte, sql_section_header, wrapper_text)
        container = result()
        if kwargs:
            container(**kwargs)
        return container

    def __str__(self):
        return str(self())

    def reg(
        self,
        cte_name: str,
        sql_query: Optional[SqlQuery | SqlContainer | dict] = None,
        *,
        sql_id: Optional[str | uuid.UUID] = '',  # works only if sql_query parameter is not provided
    ) -> SqlQuery:
        """Create new cte and return SqlQuery instance"""
        kwargs = {}
        if sql_id:
            kwargs['sql_id'] = sql_id
        if isinstance(sql_query, SqlQuery):
            query = sql_query
        elif isinstance(sql_query, dict):
            sql_query = copy_cte_dict(sql_query)
            query = SqlQuery(sql_query, **kwargs)
        elif isinstance(sql_query, SqlContainer):
            query = SqlQuery(**kwargs)
            query[''](sql_query)
        else:
            query = SqlQuery(**kwargs)
        self[cte_name] = query
        return query


def add_cte_section(
    query: SqlQuery,
    cte: SqlQuery | SqlContainer | dict,
    sql_section_header: str,
    wrapper_text: str,
):
    """Add cte as SqlSection in SqlQuery"""
    if isinstance(cte, SqlQuery):
        query[sql_section_header](cte(wrapper_text))
    else:
        if isinstance(cte, dict):
            cte = form_container_by_dict(cte)

        cte.is_multiline_wrap_type = True
        cte.wrapper_text = wrapper_text
        query[sql_section_header](cte)


def copy_cte_dict(dictionary: dict) -> dict:
    """
    Copy dict and remove service fields
    """
    if '__ctes__' in dictionary:
        raise AttributeError('Unallowed attribute: __ctes__')

    cte_dict_copy = dict(dictionary)
    for field_name in ('__is_cte__',):
        cte_dict_copy.pop(field_name, None)
    return cte_dict_copy
