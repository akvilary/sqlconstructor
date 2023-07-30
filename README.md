# sql_constructor
**sql_constructor** is simple, yet very flexible, sql building tool.

## How to install
You could install from PyPi:
```console
$ python3 -m pip install sql-constructor
```
## Little bit of theory
1) Each sql building starts with SqlQuery - class instance that helps us to register into it as many SqlSection instances as we would like to.
2) SqlSection - it is part of SqlQuery. It process data and store it to SqlContainer.
3) SqlContainer - hold result of processed data. SqlContainer contains sql text (as string), optional wrapper (usually required for nested subqueries), and optional variables (to be replaced with placeholders).
4) When you build query (call \_\_call\_\_ method of SqlQuery) then you union all SqlContainer instances (of each SqlSection) into one SqlContainer which inherits variables of united instances.


## How to use
### Build simple query
```python
import sql_constructor as sc


# create SqlQuery instance
q = sc.SqlQuery()
# register as many SqlSection instances as you'd like
q['select'](
    'id',
    'name',
)
q['from'](
    'catalog'
)
q['where'](
    "name = 'Smart'"
)

# build query into SqlContainer
container: sc.SqlContainer = q()
# get sql as string
sql_text: str = str(container)
```
### Another portion of theory
1) Because of sql headers ('select', 'from' and etc.) cannot be unique that's why it is only possible to append sql sections (but not get it back by index).
2) We register (i.e. append) SqlSection by \_\_getitem\_\_ method of SqlQuery. It is possible to add sections with duplicate header. Header can be any string! SqlSection instances will be written in query in order you set them.
3) When we call \_\_call\_\_ method of SqlSection we build SqlContainer of SqlSection (combining sql header with values passed by arguments).


### Build query with placeholders to be replaced by variables later
You could add placeholder in query by adding **!variable_name** syntax.
#### Set variable instantly
```python
import sql_constructor as sc


def get_product_query(prod_name: str) -> sc.SqlContainer:
    q = sc.SqlQuery()
    q['select'](
        'id',
        'name',
    )
    q['from'](
        'catalog'
    )
    q['where'](
        'name = !product_name'
    )(product_name=prod_name)
    q['order by']('name DESC')
    container: sc.SqlContainer = q()
    return container
```

#### or later in SqlContainer
```python
import sql_constructor as sc


def main():
	container: sc.SqlContainer = get_product_query()
	# set variables to existing container
	container.vars['product_name'] = 'Smart'


def get_product_query() -> sc.SqlContainer:
	q = sc.SqlQuery()
	q['select'](
	    'id',
	    'name',
	)
	q['from'](
	    'catalog'
	)
	q['where'](
	    'name = !product_name'
	)
	container: sc.SqlContainer = q()
	return container
```

### You could cache SqlContainer and set/change variables later
```python
import sql_constructor as sc
from functools import cache

def main():
	container: sc.SqlContainer = get_product_query()
	container.vars['product_name'] = 'Smart'

@cache
def get_product_query() -> sc.SqlContainer:
	...
```

### Get sql where placeholders are replaced by variables
```python
import sql_constructor as sc
from functools import cache

def main():
	container: sc.SqlContainer = get_product_query()
	container.vars['product_name'] = 'Smart'
	# to replace placeholders by variables call 'dumps' method
	sql_text: str = container.dumps()

@cache
def get_product_query() -> sc.SqlContainer:
	...
```
If you would like to get sql without replacing placeholders then call '\_\_str\_\_' method of SqlContainer instead of 'dumps':
```python
import sql_constructor as sc
from functools import cache

def main():
	container: sc.SqlContainer = get_product_query()
	container.vars['product_name'] = 'Smart'
	# get sql without replacing placeholders by variables
	sql_text: str = str(container)

@cache
def get_product_query() -> sc.SqlContainer:
	...
```

### Build complicated and nested queries
You could make query as nested as you would like to.
```python
import sql_constructor as sc
from typing import List


def main():
	q = sc.SqlQuery()
    q['select'](
        'c.id',
        'c.name',
    )
    q['from'](
        'catalog as c',
    )
    q['left join lateral'](
        get_left_join_lateral(),
    )
    q['where']('c.name = !product_name')(product_name='Smart')


def get_left_join_lateral() -> sc.SqlContainer:
    j = SqlQuery()
    j['select'](
        'id',
        'expiration_date',
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
    where.append('c.id = e.id')
    where.append('AND expiration_date <= now()')
    return where
```
### Append simple sql statements to query

It is possible to append string or any SqlContainer to query as new SqlSection without header in this way:
```python
import sql_constructor as sc


def main():
	q = sc.SqlQuery()
	q += '-- some comment here'
    q['select'](
        'c.id',
        'c.name',
    )
```
### Append nested sql statements or subqueries to query
```python
import sql_constructor as sc


def main():
	q = sc.SqlQuery()
	q['select'](
	    'c.id',
        'c.name',
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
import sql_constructor as sc


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
        'id = !id',
        'AND quantity > !quantity',
    )(id=11, quantity=10)
    
    return ctes()
```

2) Or create SqlQuery instance and set it
```python
import sql_constructor as sc


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
        'id = !id',
        'AND quantity > !quantity',
    )(id=11, quantity=10)
	return a
```

#### Add ctes to query
It is so easy!
```python
import sql_constructor as sc

def main():
	q = sc.SqlQuery()
    q += get_ctes()
    q['select'](
	    'id',
	    'name'
    )
    ...


def get_ctes() -> sc.SqlContainer:
	...
```
### Debugging

#### How to find piece of code by produced sql
If you would like to find your piece of code in editor by sql produced by sql_constructor then you could mark SqlQuery instances by 'sql_id' parameter before you produce ready sql:
```python
def main():
	q = sc.SqlQuery()
    q += get_part_of_query()
    q['select'](
	    'id',
	    'name'
    )
    ...


def get_part_of_query() -> sc.SqlContainer:
	p = SqlQuery(sql_id='25b11c69-ae05-4804-89ea-8ee405f6be8b')
	...
```
It add comment to produced sql as
```sql
-- sql_id='25b11c69-ae05-4804-89ea-8ee405f6be8b'
...
```
Now when you see sql_id in your logs then it will be easy to find that part of code in your editor!
