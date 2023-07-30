# sql_constructor
**sql_constructor** is simple, yet very flexible, sql building tool.

## How to install
You could install from PyPi:
```console
$ python3 -m pip install sql-constructor
```

## How to use
### Build simple query
```python
import sql_constructor as sc
# create SqlQuery instance
q = sc.SqlQuery()
# Because of sql headers (select, from and etc.) cannot be unique that's why it is possible only to add sql sections (not get created one by indexing). We make it by __getitem__ (which create named sql section and add to query) and call sql section with arguments (to set values to sql section's body).
# It is possible to add sections with not unique header. Header can be any string! It will be written in query in order you set it.  
q['select'](
    'c.identifier as id',
    'c.name',
)
q['from'](
    'catalog as c'
)
q['where'](
    "c.name = 'Smart'"
)

# get SqlContainer
container: sc.SqlContainer = q()
# get sql text to be ready to use
sql_text: str = container.dumps()
```

### Build query with variables to be set
You could add variable in query by adding **!variable_name** syntax.
#### Set variable instantly
```python
import sql_constructor as sc
def get_select_product_query(product_name: str) -> sc.SqlQuery:
    q = sc.SqlQuery()
    q['select'](
        'c.identifier as id',
        'c.name',
    )
    q['from'](
        'catalog as c'
    )
    q['where'](
        'c.name = !product_name'
    )(product_name=product_name)
    q['order by']('name DESC')
    return q
```

#### or later in SqlContainer
```python
import sql_constructor as sc
q = sc.SqlQuery()
q['select'](
    'c.identifier as id',
    'c.name',
)
q['from'](
    'catalog as c'
)
q['where'](
    'c.name = !product_name'
)
container: sc.SqlContainer = q()
# you could cache container and set container's variables later
container.vars['product_name'] = 'Smart'
sql_text: str = container.dumps()
```

### Build complicated and nested queries
You could add string or SqlContainer to every SqlQuery and make it as nested as you would like to:
```python
import sql_constructor as sc
def build_main_query() -> str:
	"""
	Build main query
	"""
	r = sc.SqlQuery()
    r += get_ctes()
    r['select'](
        'c.identifier as id',
        'c.name',
    )
    r['from'](
        'catalog as c',
    )
    r['left join lateral'](
        get_left_join_lateral(),
    )
    r['where']('c.name = !product_name')(product_name='Smart')


def get_ctes() -> sc.SqlContainer:
	"""
	Build ctes
	"""
    ctes = sc.SqlCte()
    # regiter cte and fill it later
    a: sc.SqlQuery = ctes.reg('warehouse')
    a['select'](
        'id',
        'quantity',
    )
    a['from']('warehouse')
    a['where'](
        'id = !id',
        'AND quantity > !quantity',
    )(id=11, quantity=10)

    # or build query and pass it in as cte
    b = sc.SqlQuery()
    # pass in now (commented code below):
    # ctes.reg('pricelist', b)
    b['select'](
        'id',
        'price',
    )
    b['from']('pricelist')
    b['where'](
        'id = ANY(!ids)',
        'AND "price" > !price',
    )(ids=[15, 16, 17], price=1.00)
    # or later (bot variants work)
    ctes.reg('pricelist', b)
    # it is also possible to use __setitem__ (commented code below)
    # ctes['pricelist'] = b
    # or get created query by __getitem__ (commented code below)
    # b = ctes['pricelist']
    # because of name of cte is unique it is possible to use __setitem__, __getitem__.

    return ctes()

def get_left_join_lateral() -> SqlContainer:
    r = SqlQuery()
    r['select'](
        'id',
        'is_valid',
    )
    r['from']('big_table as bt')

    # where
    where = []
    where.append('bt.id = c.id')
    where.append('AND is_valid = true')
    r['where'](*where)
    r['limit'](100)
    # You could get SqlContainer with wrapped subquery in some different ways:
    # return r('AS some_condition ON TRUE')
    # or
    # return r(wrap='AS some_condition ON TRUE')
    # or
    return r().wrap('AS some_condition ON TRUE')
```
