import json
from sqlconstructor import (
    SqlVal,
    SqlCol,
    SqlCols,
    SqlEnum,
)

def run4():
    if str(SqlVal({'a': SqlEnum('product', 'quantity')})) == '{"a": ["product", "quantity"]}':
        print(True)

def run3():
    if str(SqlVal(SqlCols('product', 'quantity'))) == '"product", "quantity"':
        print(True)


def run2():
    import uuid
    _uuid = uuid.uuid4()
    val = SqlVal({'a': _uuid})
    print(SqlVal.__mro__)
    if str(val) == '{"a": ' + f'"{_uuid}"' + '}':
        print(True)

def run():
    cols = SqlCols('product', 'quantity')
    # if cols.__json_array__() == ['"product"', '"quantity"']:
    #     print(True)
    # if json.dumps(cols.__json_array__()) == '["\\"product\\"", "\\"quantity\\""]':
    #     print(True)
    print(SqlCols.__mro__)
    val = SqlVal({'a': cols})
    if (
        str(val)
        == '{"a": ["\\"product\\"", "\\"quantity\\""]}'
    ):
        print(True)

# run4()
# run3()
run2()
run()
