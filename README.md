# sqlconstructor
**sqlconstructor** is simple, yet very flexible, sql building tool.

## How to install
You could install from PyPi:
```console
$ python3 -m pip install sqlconstructor
```
## Little bit of theory
1) Each sql building starts with SqlQuery - class instance that helps us to register into it as many SqlSection instances as we would like to.
2) SqlSection - it is part of SqlQuery. It process data and store it to SqlContainer.
3) SqlContainer holds result of processed data. SqlContainer contains sql text (as string), optional wrapper (usually required for nested subqueries), and optional variables (to be replaced with placeholders).
4) When you build query (call \_\_call\_\_ method of SqlQuery) then you union all SqlContainer instances (of each SqlSection) into one SqlContainer which inherits variables of united instances.


## How to use
### Build simple query
```python
import sqlconstructor as sc


# create SqlQuery instance
q = sc.SqlQuery()
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
container: sc.SqlContainer = q()
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

Output of sql_text is
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
### Another portion of theory
1) Because of sql headers ('select', 'from' and etc.) cannot be unique that's why it is only possible to append sql sections (but not get it back by index).
2) We register (i.e. append) SqlSection by \_\_getitem\_\_ method of SqlQuery. It is possible to add sections with duplicate header. Header can be any string! SqlSection instances will be written in query in order you set them.
3) When we call \_\_call\_\_ method of SqlSection we build SqlContainer of SqlSection (combining sql header with values passed by arguments).


### Build query with placeholders to be replaced by variables later
You could add placeholder in query by adding **$variable_name** syntax.
#### Set variable instantly
```python
import sqlconstructor as sc


def get_product_query(
    product_quality: str, 
    brand_identifier: int,
) -> sc.SqlContainer:
    q = sc.SqlQuery()
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
    container: sc.SqlContainer = q()
    return container
```

#### or later in SqlContainer
```python
import sqlconstructor as sc


def main():
    container: sc.SqlContainer = get_product_query()
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


def get_product_query() -> sc.SqlContainer:
    q = sc.SqlQuery()
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
    container: sc.SqlContainer = q()
    return container
```

### You could cache SqlContainer and set/change variables later
```python
import sqlconstructor as sc
from functools import cache


def main():
    # you could set default values of variables inside of cached result
    # and reset it later. 
    # Or do not set them in cached result at all and set them later. 
    container: sc.SqlContainer = get_product_query()
    # set/reset variables to existing container
    container(quality='Best', brand_id=1)


@cache
def get_product_query() -> sc.SqlContainer:
    ...
```

### Get sql where placeholders are replaced by variables
```python
import sqlconstructor as sc
from functools import cache


def main():
    container: sc.SqlContainer = get_product_query()
    container.vars.update({'quality': 'Best', 'brand_id': 1})
    # to replace placeholders by variables call 'dumps' method
    sql_text: str = container.dumps()


@cache
def get_product_query() -> sc.SqlContainer:
    ...
```
If you would like to get sql without replacing placeholders then call '\_\_str\_\_' method of SqlContainer instead of 'dumps':
```python
import sqlconstructor as sc
from functools import cache


def main():
    container: sc.SqlContainer = get_product_query()
    container.vars.update({'quality': 'Best', 'brand_id': 1})
    # get sql without replacing placeholders by variables
    sql_text: str = str(container)


@cache
def get_product_query() -> sc.SqlContainer:
    ...
```

### Build complicated and nested queries
You could make query as nested as you would like to.
```python
import sqlconstructor as sc
from typing import List


def main():
    q = sc.SqlQuery()
    q['select'](
        'p.id',
        'p.name',
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


def get_left_join_lateral() -> sc.SqlContainer:
    j = sc.SqlQuery()
    j['select'](
        'e.id',
        'e.expiration_date',
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
### Append string to query

It is possible to append string or any SqlContainer to query as new SqlSection without header in this way:
```python
import sqlconstructor as sc


def main():
    q = sc.SqlQuery()
    q += '-- some comment here'
    q['select'](
        'p.id',
        'p.name',
    )
```
### Append SqlContainer to query
```python
import sqlconstructor as sc


def main():
    q = sc.SqlQuery()
    q['select'](
        'p.id',
        'p.name',
    )
    q += get_from_statement()
    ...


def get_from_statement() -> sc.SqlContainer:
    ...
```

### Easy ways to handle ctes

#### Create ctes
1) Create cte and fill it later
```python
import sqlconstructor as sc


def get_ctes() -> sc.SqlContainer:
    """
    Build ctes
    """
    ctes = sc.SqlCte()
    # regiter cte and fill it later
    a: sc.SqlQuery = ctes.reg('warehouse_cte')
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
import sqlconstructor as sc


def get_ctes() -> sc.SqlContainer:
    """
    Build ctes
    """
    ctes = sc.SqlCte()
    ctes['warehouse_cte'] = get_warehouse_cte()
    # or
    # ctes.reg('warehouse_cte', get_warehouse_cte())

    # you could also get certain cte by name and append new SqlSection to it
    a = ctes['warehouse_cte']
    a['limit'](1)
    
    return ctes()


def get_warehouse_cte() -> sc.SqlQuery:
    a = sc.SqlQuery()
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
import sqlconstructor as sc


def main():
    q = sc.SqlQuery()
    q += get_ctes()
    q['select'](
        'id',
        'name',
    )
    ...


def get_ctes() -> sc.SqlContainer:
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

### Debugging

#### How to find piece of code by produced sql
If you would like to find your piece of code in editor by ready sql which is produced by sqlconstructor then you have to mark SqlQuery instances by 'sql_id' parameter in advance (before you have produced ready sql):
```python
import sqlconstructor as sc


def main():
    q = sc.SqlQuery()
    q += get_part_of_query()
    q['select'](
        'id',
        'name'
    )
    ...


def get_part_of_query() -> sc.SqlContainer:
    p = sc.SqlQuery(sql_id='25b11c69-ae05-4804-89ea-8ee405f6be8b')
    ...
```
It adds comment to produced sql as
```sql
-- sql_id='25b11c69-ae05-4804-89ea-8ee405f6be8b'
...
```
Now when you see sql_id in your logs then it will be easy to find that part of code in your editor!
