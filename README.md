# sqlconstructor
**sqlconstructor** is simple, yet very flexible, sql building tool.

## How to install
You could install from PyPi:
```console
$ python3 -m pip install sqlconstructor
```
## Little bit of theory
1) Each sql building starts with SqlQuery - class instance that helps us to register into it as many SqlSection instances as we would like to.
2) SqlSection - it is part of SqlQuery. It process data and store it to SqlContainer (which located as SqlSection instance attribute).
3) SqlContainer holds result of processed data. SqlContainer contains sql text (as string), optional wrapper (usually required for nested subqueries), and optional variables (to be replaced with placeholders).
4) We register (i.e. append) SqlSection by \_\_getitem\_\_ method of SqlQuery. It is possible to add sections with duplicate header. Header can be any string! SqlSection instances will be written in query in order you set them.
5) Because of sql headers ('select', 'from' and etc.) cannot be unique that's why it is only possible to append sql sections (but not get it back by index).
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
- include SqlCols, SqlVals and SqlEnum instances in query dict (in release >= 1.0.39).
- include SqlCol, SqlVal, SqlFilter, SqlFilters, SqlPlaceholder in query dict (in release >= 1.1.0)
- create query by dict with duplicate headers if headers are SqlSectionHeader class instances (in release >= 1.0.40). See example below.
- insert nested subqueries (wrapped and with text after wrapper) as nested dict (in release >= 1.1.0). More on this later.

Example of using SqlSectionHeader:
```python
from sqlconstructor import SqlQuery, SqlVal, SqlSectionHeader


H = SqlSectionHeader
q = SqlQuery(
    {
        H('select'): "'hello'",
        # create sql section without header by SqlSectionHeader instance constructed without arguments
        H(): 'union all',
        H('select'): SqlVal('hello'),
        # it is possible to add sql section without header if header is empty string
        '': 'union all',
        H('select'): "'hello'",
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
Use **'dumps'** method of SqlContainer:
```python
from sqlconstructor import SqlContainer
from functools import cache


def main():
    container: SqlContainer = get_product_query()
    container.vars.update({'quality': 'Best', 'brand_id': 1})
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
You could use & or | operator **between filters** or **betweem filter and str (or object with __str__ method)** (in release >= 1.1.0).

SqlFilter and SqlFilters insert value in query instantly if you use string as value in keyword argument or dict.

If you you would like to insert value after building query then:
  - use SqlPlaceholder instance as value in filter keyword argument or dict.
  - or add placeholder by syntax in string as filter value (neither in dict nor in keyword argument, because they are converted to sql value)
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
        SqlFilter(
            brand_id=SqlPlaceholder('brand_id')  # add placeholder as value (you could insert SqlPlaceholder anywhere where value is expected)
        )  # will be converted to brand_id=$brand_id
        &
        SqlFilter('quantity > 0')  # string will not be converted by SqlVal and will be passed as is
        &
        SqlWrap(
            SqlFilter(quality='Best')  # value will be converted to sql string by SqlVal
            |  # OR operator
            SqlFilter({'rating': 'high'})  # each value of dict will be converted by SqlVal
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

You could use SqlFilters if all filters require same operator
```python
from sqlconstructor import SqlFilters

# AND mode is default
SqlFilters(
    {
        'quality': product_quality, 
        'brand_id': brand_identifier,
    }
)

# explicit AND mode
SqlFilters(
    {
        'quality': product_quality, 
        'brand_id': brand_identifier,
    },
    'AND',
)

# OR mode
SqlFilters(
    {
        'quality': product_quality, 
        'brand_id': brand_identifier,
    },
    'OR',
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
    'OR',
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
If you add ('__do_wrap__': True) to nested dict then nested subquery will be wrapped by parenthesis.
If you add ('__wrapper_text__': any string) to nested dict then nested subquery will be wrapped and wrapper_text will be added after parenthesis (even if you do not add (__do_wrap__: True)).
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

2) Or create SqlQuery instance and set it
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

    # you could also get certain cte by name and append new SqlSection to it
    a = ctes['warehouse_cte']
    a['limit'](1)
    
    return ctes()


def get_warehouse_cte() -> SqlQuery:
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
    return a
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
- dict will be converted to json (sql example: '{"id": 23, "names": ["xo", "ox"]}')

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
  (
    brand_id, name, quality, uuid_id
  )
VALUES
  (
    1, 'phone', 'Best', '82611533-25c4-4cbd-8497-3f5024ca29a1'
  )
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

### SqlWrap
It is possible wrap any str or string convertible object by SqlWrap (in release >= 1.1.1).
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

### Debugging

#### How to find piece of code by produced sql
If you would like to find your piece of code in editor by ready sql which is produced by sqlconstructor then you have to mark SqlQuery instances by 'sql_id' parameter in advance (before you have produced ready sql):
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
It adds comment to produced sql as
```sql
-- sql_id='25b11c69-ae05-4804-89ea-8ee405f6be8b'
SELECT
  quantity
...
```
Now when you see sql_id in your logs then it will be easy to find that part of code in your editor!
