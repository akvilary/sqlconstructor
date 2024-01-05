# sqlconstructor
**sqlconstructor** is simple, yet very flexible, sql building tool.

## How to install
You could install from PyPi:
```console
$ python3 -m pip install sqlconstructor
```
## A little bit of theory
1) Each sql building starts with SqlQuery - class instance that helps us to register into it as many SqlSection instances as we would like to.
2) SqlSection - it is part of SqlQuery. It process data and store it to SqlContainer (which located as SqlSection instance attribute).
3) SqlContainer holds result of processed data. SqlContainer contains sql text (as string), optional wrapper (usually required for nested subqueries), and optional variables (to be replaced with placeholders).
4) We register (i.e. append) SqlSection by \_\_getitem\_\_ method of SqlQuery. It is possible to add sections with duplicate header. Header can be any string! SqlSection instances will be written in query in order you set them.
5) Because of sql headers ('select', 'from' and etc.) cannot be unique that's why it is only possible to append sql sections (but not get it back by sql header).
6) When we call \_\_call\_\_ method of SqlSection we build SqlContainer of SqlSection (combining sql header with values passed by arguments).
7) When you build query (call \_\_call\_\_ method of SqlQuery) then you union all SqlContainer instances (of each SqlSection) into one SqlContainer which inherits variables of united instances and return it.


## How to use
### Build simple query
```python
from sqlconstructor import SqlQuery, SqlContainer


# create SqlQuery instance
q = SqlQuery()
# register as many SqlSection instances as you'd like
q['select'](
    'id',
    'name',
)
q['from'](
    'product'
)
q['where'](
    "quality = 'Best'",
    'and brand_id = 1',
)

# build query into SqlContainer
container: SqlContainer = q()
# get sql as string
sql_text: str = str(container)
```
### Output
**SqlSection** automatically transforms all sql keywords in uppercase. 
It does not upper in following cases:
- if sql keyword is located in inline/multiline comment.
- if sql keyword is located inside single/double quotes.

**SqlSection** automatically adds comma between provided sql statements in \_\_call\_\_ method for next headers:
- SELECT
- FROM
- SET
- VALUES
- ORDER BY
- GROUP BY
- JSON_OBJECT_AGG
- COALESCE

Output of sql_text is:
```sql
SELECT
  id,
  name
FROM
  product
WHERE
  quality = 'Best'
  AND brand_id = 1
```

In release >= 1.4.0 it is possible to add default settings for all future sections by special kwargs in SqlQuery constructor such as **header_end**, **sep**, **line_end**, **section_end**, **body_ind**, **header_ind**, **do_upper_keywords**.
```python
from sqlconstructor import SqlQuery


q = SqlQuery(do_upper_keywords=False)
```

### SqlSection \_\_call\_\_
It is possible to give special keyword arguments in SqlSection \_\_call\_\_ method:
- header_ind - relative indentation of section header (can be positive or negative). Default=0.
- body_ind - relative indentation of section body (can be positive or negative). Default is 2 if section header else 0.
- sep - separator of statements. Default is ',' for comma separated sections else ''.
- line_end - end of line of each statement (default='\\n')
- section_end - end of sql section (default='')
- do_upper_keywords - do upper sql keywords (default=True)
```python
...
q['where'](
    "quality = 'Best'",
    'brand_id = 1',
    header_ind=2,
    body_ind=4,
    # delimeter = sep + line_end
    sep=' AND',
    line_end=' ',
    section_end=';',
    do_upper_keywords=False,
)
...
```

### It is also possible to create SqlQuery instance by dict
```python
from sqlconstructor import SqlQuery


q = SqlQuery(
    {
        'select': (
            'id',
            'name',
        ),
        'from': 'product',
        'where': (
            "quality = 'Best'",
            'and brand_id = 1',
        ),
    }
)
```
But it has certain limitation:
- It is not possible to create query by dict with duplicate headers if headers are strings (because of dict nature).

But it is possible: 
- include SqlCols, SqlVals and SqlEnum instances in query dict (in release >= 1.0.39);
- include SqlCol, SqlVal, SqlFilter, SqlFilters, SqlPlaceholder in query dict (in release >= 1.1.0);
- create query by dict with duplicate headers if headers are SqlSectionHeader class instances (in release >= 1.0.40). See example below;
- insert nested subqueries (wrapped and with text after wrapper) as nested dict (in release >= 1.1.0). More on this later.

Example of using SqlSectionHeader:
```python
from sqlconstructor import SqlQuery, SqlVal, SqlSectionHeader


h = SqlSectionHeader
q = SqlQuery(
    {
        h('select'): "'hello'",
        # it is possible to add sql section without body
        h('union all'): None,
        h('select'): SqlVal('hello'),
        # or create sql section without header
        h(): 'union all',
        h('select'): "'hello'",
    }
)
container: SqlContainer = q()
sql_text: str = str(container)
```
Output of sql_text is:
```sql
SELECT
  'hello'
UNION ALL
SELECT
  'hello'
UNION ALL
SELECT
  'hello'
```

### Iterate through SqlSection instances and change text for ready SqlContainer
```python
from sqlconstructor import SqlQuery


q = SqlQuery()
q['select'](
    'id',
    'name',
)
q['from'](
    'product'
)
q['where'](
    "quality = 'Best'",
    'and brand_id = 1',
)

for section in q:
    # add empty line for "from" statement
    if section.header == 'from':
        # change container's text in place 
        section.container.text += '\n'
...    
```

### Get part of query
It is possible to slice query (in release >= 1.2.10). When you slice you get new SqlQuery instance. 
But it is not deep copied (you get new query but with same SqlSection instance elements).

It is possible to get certain SqlSection instance by getitem with integer argument (in release >= 1.2.11).
SqlQuery has list behavior (except \_\_init\_\_, \_\_iadd\_\_ and \_\_getitem\_\_ methods) in release >= 1.3.0.
```python
from sqlconstructor import SqlQuery


q = SqlQuery()
q['select'](
    'id',
    'name',
)
q['from'](
    'product'
)
q['where'](
    "quality = 'Best'",
    'and brand_id = 1',
)

# get only SELECT and FROM statements
new_query = q[:2]
# get first SqlSection
select = q[0]
...    
```

### Append string to query
It is possible to append string or any SqlContainer to query as new SqlSection without header in this way:
```python
from sqlconstructor import SqlQuery


def main():
    q = SqlQuery()
    q += '-- some comment here'

    with open('./some_file.sql', encoding='utf-8') as file:
        sql_file = file.read().rstrip()
    q += sql_file
    
    q['select'](
        'p.id',
        'p.name',
    )
```

It is possible add extra indentation (positive or negative) for string or SqlContainer by 'add' method (in release >= 1.2.5)
```python
from sqlconstructor import SqlQuery


def main():
    q = SqlQuery()
    q += '-- some comment here'

    with open('./some_file.sql', encoding='utf-8') as file:
        sql_file = file.read().rstrip()
    q.add(sql_file, ind=4)
    ...
```

### Append SqlContainer to query
```python
from sqlconstructor import SqlQuery, SqlContainer


def main():
    q = SqlQuery()
    q['select'](
        'p.id',
        'p.name',
    )
    q += get_from_statement()
    ...


def get_from_statement() -> SqlContainer:
    ...
```

### Append SqlQuery to query
In release >= 1.2.4 it is possible to nest SqlQuery instance (it will be converted to SqlContainer automatically).
```python
from sqlconstructor import SqlQuery, SqlContainer


def main():
    q = SqlQuery()
    q['select'](
        'p.id',
        'p.name',
    )
    q += get_from_statement()
    q += get_where_filters()
    ...


def get_from_statement() -> SqlQuery:
    ...

def get_where_filters() -> SqlQuery:
    ...
```

### Append sections via dict to query with .add method
In release >= 1.3.13
```python
from sqlconstructor import SqlQuery
q = SqlQuery()
q.add(
    {
        'select': (
            'product_id',
            'price'
        ),
        'from': 'prices',
    }
)
```

Add section settings in dict (in release >= 1.4.0)
```python
from sqlconstructor import SqlQuery


q = SqlQuery()
q.add(
    {
        'select': (
            'a',
            'b',
        ),
        '__header_end__': ' ',  # default is '\n'
        '__sep__': ' +',
        '__line_end__': ' ',  # default is '\n'
        '__section_end__': ';',  # default is ''
        '__header_ind__': 2,  # default is 0
        '__body_ind__': 4,  # default is 2 if is header else 0
        '__do_upper_keywords__': False,  # default is True
    }
)
```

### Build query with placeholders to be replaced by variables later
You could add placeholder in query by adding **$variable_name** syntax.
#### Set variable instantly
```python
from sqlconstructor import SqlQuery, SqlContainer


def get_product_query(
    product_quality: str, 
    brand_identifier: int,
) -> SqlContainer:
    q = SqlQuery()
    q['select'](
        'id',
        'name',
    )
    q['from'](
        'product'
    )
    q['where'](
        'quality = $quality',
        'and brand_id = $brand_id'
    )(quality=product_quality, brand_id=brand_identifier)
    q['order by']('name DESC')
    container: SqlContainer = q()
    return container
```

#### or later in SqlContainer
```python
from sqlconstructor import SqlQuery, SqlContainer


def main():
    container: SqlContainer = get_product_query()
    # set variables to existing container
    container(quality='Best', brand_id=1)
    # or
    container.vars['quality'] = 'Best'
    container.vars['brand_id'] = 1

    # if you would like to rewrite all vars
    new_vars = {'quality': 'Medium', 'brand_id': 2}
    container.vars = new_vars

    # if you would like to remove all vars
    container.vars.clear()


def get_product_query() -> SqlContainer:
    q = SqlQuery()
    q['select'](
        'id',
        'name',
    )
    q['from'](
        'product'
    )
    q['where'](
        'quality = $quality',
        'and brand_id = $brand_id'
    )
    container: SqlContainer = q()
    return container
```

### You could cache SqlContainer and set/change variables later
```python
from sqlconstructor import SqlContainer
from functools import cache


def main():
    # you could set default values of variables inside of cached result
    # and reassign them later. 
    # Or do not set them in cached result at all and set them later. 
    container: SqlContainer = get_product_query()
    # set/reassign variables to existing container
    container(quality='Best', brand_id=1)


@cache
def get_product_query() -> SqlContainer:
    ...
```

### Get sql where placeholders are replaced by variables
Use **'dumps'** method of SqlContainer.
Notice that each value of variables will be conveted to sql by SqlVal class. 
If you would like to insert value of variable 'as is' in sql string then save variable as SqlContainer.
```python
from sqlconstructor import SqlContainer
from functools import cache


def main():
    container: SqlContainer = get_product_query()
    container.vars.update(
        {
            'quality': 'Best',  # will be converted by SqlVal to 'Best' (with surrounding single quotes)
            'avg': SqlContainer('price'),  # will be converted by 'str' method and not by SqlVal (because of SqlContainer)
        }
    )
    # to replace placeholders by variables call 'dumps' method
    sql_text: str = container.dumps()


@cache
def get_product_query() -> SqlContainer:
    ...
```
If you would like to get sql without replacing placeholders then call **'\_\_str\_\_'** method of SqlContainer instead of 'dumps':
```python
from sqlconstructor import SqlContainer
from functools import cache


def main():
    container: SqlContainer = get_product_query()
    container.vars.update({'quality': 'Best', 'brand_id': 1})
    # get sql without replacing placeholders by variables
    sql_text: str = str(container)


@cache
def get_product_query() -> SqlContainer:
    ...
```

### Use filters
You could use & or | operator **between filters** or **betweem filter and str (or any object with __str__ method)** (in release >= 1.1.0).
Result of & or | operator is SqlContainer and SqlContainer (and SqlWrap) also can operate & and | (in release >= 1.2.0)
```python
from sqlconstructor import SqlQuery, SqlFilter, SqlContainer, SqlWrap


def get_product_query() -> SqlContainer:
    q = SqlQuery()
    q['select'](
        'id',
        'name',
    )
    q['from']('product')
    q['where'](
        'id <> $identifier'  # add placeholder in string
        &  # AND operator
        SqlContainer('price < 10')
        &
        SqlFilter(
            brand_id=SqlPlaceholder('brand_id')  # add placeholder as value (you could insert SqlPlaceholder anywhere where value is expected)
        )  # will be converted by SqlVal to brand_id=$brand_id
        &
        SqlFilter('quantity > 0')  # string will not be converted by SqlVal and will be passed as is
        &
        SqlWrap(
            SqlFilter(quality='Best')  # value of the keyword argument will be converted by SqlVal to sql string
            |  # OR operator
            SqlFilter({'rating': 'high'})  # dict value will be converted by SqlVal to sql string
        )
    )
    container: SqlContainer = q()
    container(identifier=2, brand_id=1) # set variables after building query for placeholders
    return container
```
Output of str(container)
```sql
SELECT
  id,
  name  
FROM
  product
WHERE
  id <> $identifier
  AND
  price < 10
  AND
  brand_id=$brand_id
  AND
  quantity > 0
  AND
  (
    quality='Best'
    OR
    rating='high'
  )
```

SqlFilters has dict behavior (in release >= 1.1.4). You could set, get, iterate SqlFilters as dict.
```python
from sqlconstructor import SqlFilters

filters = SqlFilters()

filters['a'] = 1
filters['b'] = 2
one = filters['a']

if 'a' in filters:
    del filters['a']

for key, value in filters.items():
    ...
```

You could use SqlFilters if all filters require same operator
```python
from sqlconstructor import SqlFilters, AND, OR

# AND mode is default
SqlFilters(
    {
        'quality': product_quality,  # each value of dict will be converted by SqlVal
        'brand_id': brand_identifier,
    }
)

# explicit AND mode
SqlFilters(
    {
        'quality': product_quality, 
        'brand_id': brand_identifier,
    },
    AND,
)

# OR mode
SqlFilters(
    {
        'quality': product_quality, 
        'brand_id': brand_identifier,
    },
    OR,
)

# Build filters by keyword arguments

# AND as default
SqlFilters(
    quality=product_quality, 
    brand_id=brand_identifier,
)

# OR
SqlFilters(
    None,
    OR,
    quality=product_quality, 
    brand_id=brand_identifier,
)
```

### Build complicated and nested queries
You could make query as nested as you would like to.
#### Build by adding sections
```python
from sqlconstructor import SqlQuery, SqlContainer
from typing import List


def main():
    q = SqlQuery()
    q['select'](
        'p.id',
        'p.name',
        'exp.exp_date'
    )
    q['from'](
        'product as p',
    )
    q['left join lateral'](
        get_left_join_lateral(),
    )
    q['where'](
        'p.quality = $quality',
        'and p.brand_id = $brand_id'
    )(quality='Best', brand_id=1)


def get_left_join_lateral() -> SqlContainer:
    j = SqlQuery()
    j['select'](
        'e.id',
        'e.expiration_date as exp_date',
    )
    j['from']('expiration as e')
    j['where'](*get_filters())
    j['limit'](100)
    """
    You could get SqlContainer with wrapped subquery 
    in some different ways:
    # return r('AS exp ON TRUE')
    or
    # return r(wrap='AS exp ON TRUE')
    """
    # or more explicit
    return j().wrap('AS exp ON TRUE')


def get_filters() -> List[str]:
    """Create filters"""
    where = []
    where.append('p.id = e.id')
    where.append('AND e.expiration_date <= now()')
    return where
```

#### Build nested queries by passing nested dict to main dict in SqlQuery construction time
If you pass nested dict in main query dict then it will be subquery. 
If you add ('\_\_do\_wrap\_\_': True) to nested dict then nested subquery will be wrapped by parenthesis.
If you add ('\_\_wrapper\_text\_\_': any string) to nested dict then nested subquery will be wrapped and wrapper_text will be added after parenthesis (even if you do not add (\_\_do\_wrap\_\_: True)).
```python
from sqlconstructor import SqlQuery
q = SqlQuery(
    {
        'select': (
            'p.id',
            'p.name',
            'exp.exp_date'
        ),
        'from': 'product as p',
        'left join lateral': {
            'select': (
                'e.id',
                'e.expiration_date as exp_date',
            ),
            'from': 'expiration as e',
            'where': (
                'p.id = e.id',
                'AND e.expiration_date <= now()',
            ),
            '__wrapper_text__': 'as exp on true',
        },
        'where': (
            "quality = 'Best'",
            'and brand_id = 1',
        ),
    }
)
```

### Easy ways to handle ctes

#### Create ctes
SqlCte is StringConvertible and ContainerConvertible (in release >= 1.3.0).
1) Create cte and fill it later
```python
from sqlconstructor import SqlQuery, SqlContainer, SqlCte


def get_ctes() -> SqlContainer:
    """
    Build ctes
    """
    ctes = SqlCte()
    # regiter cte and fill it later
    a: SqlQuery = ctes.reg('warehouse_cte')
    a['select'](
        'id',
        'quantity',
    )
    a['from']('warehouse')
    a['where'](
        'id = $id',
        'AND quantity > $quantity',
    )(id=11, quantity=10)
    
    return ctes()
```

2) Or create SqlQuery instance (or SqlContainer in release >= 1.2.5 or dict in release >= 1.3.13) and set it to SqlCte instance
```python
from sqlconstructor import SqlQuery, SqlContainer, SqlCte


def get_ctes() -> SqlContainer:
    """
    Build ctes
    """
    ctes = SqlCte()
    ctes['warehouse_cte'] = get_warehouse_cte()
    # or
    # ctes.reg('warehouse_cte', get_warehouse_cte())
    # or by dict
    # ctes.reg('warehouse_cte', {'select': ('id', 'quantity',) ...})

    # you could also get certain cte by name and append new SqlSection to it
    a = ctes['warehouse_cte']
    a['limit'](1)
    
    return ctes()


def get_warehouse_cte() -> SqlQuery: # or SqlContainer
    a = SqlQuery()
    a['select'](
        'id',
        'quantity',
    )
    a['from']('warehouse')
    a['where'](
         'id = $id',
         'AND quantity > $quantity',
    )(id=11, quantity=10)
    return a  # or a()
```

#### Add ctes to query
It is so easy!
```python
from sqlconstructor import SqlQuery, SqlContainer


def main():
    q = SqlQuery()
    q += get_ctes()
    q['select'](
        'id',
        'name',
    )
    ...


def get_ctes() -> SqlContainer:
    ...
```

or create and add cte to query in one step in release >= 1.3.13
```python
from sqlconstructor import SqlQuery, SqlContainer


def main():
    q = SqlQuery()
    q.ctes['bestsellers'] = {'select': ('id', 'sold',) ...}
    # or set by SqlContainer or SqlQuery
    # q.ctes['bestsellers'] = get_warehouse_cte()
    ...
```

### Build ctes by dict in query construction
In release >= 1.2.5
```python
from sqlconstructor import SqlQuery, SqlContainer


def main():
    q = SqlQuery(        
        {
            'products': {
                '__is_cte__': True,
                'select': 'product_id',
                'from': 'warehouse',
                'where': 'quantity > 0',
            },
            'select': (
                'id',
                'name',
            ),
        },
        ...
    )
    ...
```

In release >= 1.3.13 we add extra syntax
```python
from sqlconstructor import SqlQuery, SqlContainer


def main():
    q = SqlQuery(        
        {
            '__ctes__': {
                'products': {
                    'select': 'product_id',
                    'from': 'warehouse',
                    'where': 'quantity > 0',
                },
                'product_descriptions': {
                    'select': 'description',
                    ...
                },
            },
            'select': (
                'id',
                'name',
            ),
        }
        ...
    )
    ...
```

### Add ctes via dict to query with .add method
In release >= 1.3.13
```python
from sqlconstructor import SqlQuery
q = SqlQuery()
q.add(
    {
        '__ctes__': {
            'products': {
                'select': 'product_id',
                'from': 'warehouse',
                'where': 'quantity > 0',
            },
        },
    },
)
```

### Enumerate columns, values
In release >= 1.0.29 you could enumerate columns and values a little bit easier:
```python
import uuid
from sqlconstructor import SqlQuery, SqlCols, SqlVals


q = SqlQuery()
_uuid = uuid.uuid4()
q['insert into'](
    'product',
    SqlCols(
        'brand_id',
        'name',
        'quality',
        'uuid_id',
    ),
)
q['values'](
    SqlVals(
        1,
        'phone',
        'Best',
        _uuid,
    )
)
sql_text = str(q())
```

sql_text output will be
```sql
INSERT INTO
  product
  (
    "brand_id",
    "name",
    "quality",
    "uuid_id"
  )
VALUES
  (
    1,
    'phone',
    'Best',
    '82611533-25c4-4cbd-8497-3f5024ca29a1'
  )
```
**SqlVals** converts python objects to sql values (same mechanics used in '$value' replacement by 'dumps' method of **SqlContainer**).
- any string will be added with single quotes;
- uuid will be added as string with single quotes;
- list, set, tuple will be converted to array (sql example: ARRAY['xo', 'ox']);
- dict will be converted to json (sql example: E'{"id": 23, "names": ["xo", "ox"]}' ). Character 'E' will be only added if DIALECT constant is 'PostgreSQL' to support escape characters in json. 

If you would like to do not add double quotes to columns then you could use **SqlEnum** class. **SqlEnum** converts to strings as is (without extra processing), and do not add any extra characters (no single quotes either).

Any of this class (**SqlEnum, SqlVals, SqlCols**) has 'inline' and 'multiline' method (return **SqlContainer** which you could wrap by 'wrap' method or do not wrap) in release >= 1.0.29.
Example:
```python
import uuid
from sqlconstructor import SqlQuery, SqlEnum, SqlVals


q = SqlQuery()
_uuid = uuid.uuid4()
q['insert into'](
    'product',
    SqlEnum(
        'brand_id',
        'name',
        'quality',
        'uuid_id',
    ).inline().wrap(),
)
q['values'](
    SqlVals(
        1,
        'phone',
        'Best',
        _uuid,
    ).inline().wrap()
)
sql_text = str(q())
```
sql_text output will be
```sql
INSERT INTO
  product
  (brand_id, name, quality, uuid_id)
VALUES
  (1, 'phone', 'Best', '82611533-25c4-4cbd-8497-3f5024ca29a1')
```

SqlEnum, SqlCols, SqlVals classes have list behavior (in release >= 1.1.4). You could set, get, iterate any of theses classes as list:
```python
from sqlconstructor import SqlVals

sql_vals = SqlVals('a', 'b')

sql_vals[0] = 'f'
f_char = sql_vals[0]

sql_vals.append('c')
sql_vals.extend(['d', 'e'])
sql_vals.pop()

if 'd' in sql_vals:
    sql_vals.remove('d')
```

### SqlVal, SqlCol
It is possible to insert single sql value and column by SqlVal and SqlCol class instance respectively (in release >= 1.1.0).
```python
from sqlconstructor import SqlQuery, SqlCol, SqlVal

# create SqlQuery instance
q = SqlQuery()
# register as many SqlSection instances as you'd like
q['select'](
    SqlCol('id'),
    SqlCol('name'),
)
q['from'](
    'product'
)
q['where'](
    'quality = ' + SqlVal('Best'),
    f"and brand_id = {SqlVal(1)}",
)
```

### SqlContainer
SqlContainer inherits all vars of another SqlContainer if it provided as argument in construction (in release >= 1.1.8). 
You could add inline wrap if you provide 'do_multiline=False' argument in 'wrap' method (in release >= 1.1.8). Multiline type of wrapping is default. 

SqlContainer has 'indent' method to make positive or negative indentation (in release >= 1.2.5).

### SqlWrap
It is possible wrap any str or string convertible object by SqlWrap (in release >= 1.1.1). 
SqlWrap also could operate & or | as SqlFilter (in release >= 1.1.4). 
SqlWrap is subclass of SqlContainer (in release >= 1.1.8). 
SqlWrap has inline and multiline methods (in release >= 1.1.8). It only change type of wrapping and do not make whole text in one line (or in multi lines). 
```python
from sqlconstructor import SqlFilter, SqlWrap
result = str(SqlWrap(SqlFilter(a=1) & SqlFilter(b=2)))
```
result is:
```sql
(
  a=1
  AND
  b=2
)
```

### Sql builtin fuctions in python
In release >= 1.4.0 we add coalesce and nullif in python implementation
```python
from sqlconstructor import coalesce, nullif, SqlVal


a = coalesce(None, 3, 4, None)  # will be 3
b = coalesce(None, None)  # will be None
c = SqlVal(coalesce(None, None))  # will be 'null'

d = nullif(3, 4)  # will be 3
e = nullif(3, 3)  # will be None
f = SqlVal(nullif(3, 3))  # will be 'null'
```

### SqlCase
In release 1.4.1 we add SqlCase class. It is invented to be python implementation of CASE-WHEN-THEN-ELSE-END construction.
Each WHEN-THEN is a tuple. ELSE statement is single value. After ELSE statement construction will be closed even if you add tuples after it.

Example of SqlCase use:
```python
from sqlconstructor import SqlCase


sql_case = SqlCase(('b=1', "'one'"), ('b=2', "'two'"), "'nothing'")
```
result of str(sql_case) will be:
```sql
CASE
  WHEN
    b=1
  THEN
    'one'
  WHEN
    b=2
  THEN
    'two'
  ELSE
    'nothing'
END
```

### StringConvertible
SqlQuery is StringConvertible (in release >= 1.3.0). Now it supports \_\_add\_\_ and \_\_radd\_\_ methods with another StringConvertible subclasses.

\_\_add\_\_ and \_\_radd\_\_ returns SqlContainer and inherits vars of any SqlContainer instance arg.

StringConvertible subclasses:
- SqlCol
- SqlCols
- SqlContainer
- SqlCte
- SqlEnum
- SqlFilter
- SqlFilters
- SqlPlaceholder
- SqlQuery
- SqlSection
- SqlSectionHeader
- SqlVals
- SqlWrap
- SqlCase

### ContainerConvertible
You could convert each instance of classes below into SqlContainer and set sql variables in one step by \_\_call\_\_ method (in release >= 1.1.5):
SqlCol, SqlCols, SqlCte, SqlEnum, SqlFilter, SqlFilters, SqlPlaceholder, SqlSectionHeader, SqlVal, SqlVals, SqlCte (in release >= 1.3.0).

### SqlJson
SqlJson (in release >= 1.2.9) has 'loads' and 'dumps' static methods similar to python 'json' library.
'loads' convert from sql json to python object and 'dumps' convert from python object to sql json.

### Debugging

#### How to find piece of code by produced sql
If you would like to find your piece of code in editor by ready sql which is produced by sqlconstructor 
then you have to mark SqlQuery instances by 'sql_id' parameter in advance (before you have produced ready sql):
```python
from sqlconstructor import SqlQuery, SqlContainer


def main():
    q = SqlQuery()
    q += get_part_of_query()
    q['select'](
        'id',
        'name'
    )
    ...


def get_part_of_query() -> SqlContainer:
    p = SqlQuery(sql_id='25b11c69-ae05-4804-89ea-8ee405f6be8b')
    p['select']('quantity')
    ...
```
Since you added sql_id, now the SqlQuery instance has such value in sql_id attribute and it will add comment to produced sql as:
```sql
-- sql_id='25b11c69-ae05-4804-89ea-8ee405f6be8b'
SELECT
  quantity
...
```
Now when you see sql_id in your logs then it will be easy to find that part of code in your editor!
