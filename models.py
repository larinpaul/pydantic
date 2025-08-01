# https://docs.pydantic.dev/latest/concepts/models/

# Models

# One of the primary ways of defining schema in Pydantic is via models
# Models are simply classes which inherit from BaseModel and define fields
# as annotated attributes.

# You can think of models as similar to structs in languages like C,
# or as the requirements of a single endpoint in an API.

# Models are similar to Python's dataclasses, but different

# ...

# Untrusted data can be passed to am odel and, after parsing and validation,
# Pydantic guarantees that the fields of the resultant model instance
# will conform to the field types defined on the model


# Basic model usage

# Pydantic relies heavily on the existing Python typing constucts to define models.
# If you are not familiar with those, the following resources can be useful:
# * The Type System Guides // https://typing.python.org/en/latest/guides/index.html
# * The mypy documentation // https://mypy.readthedocs.io/en/latest/

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    id: int
    name: str = 'Jane Doe'

    model_config = ConfigDict(str_max_length=10)


# The model can then be instantiated:

user = User(id='123')


# Fields of a model can be accessed as normal attributes of the user object:

assert user.name == 'Jane Doe'
assert usre.id == 123
assert isinstance(user.id, int)


# The model instance can be serialized using the model_dump() method:

assert user.model_dump() == {'id': 123, 'name': 'Jane Doe'}

# Calling dict on the instance will also provide a dictionary,
# but nested fields will not be recursively converted into dictionaries


# By default, models are mutable and field values can be changed
# through attribute assignment:

user.id = 321
assert user.id = 321


# Warning

# When defining your models, watch out for naming collisions
# between your field name and its type annotation.

# For example, the following will not behave as expected
# and would yield a validation error:

from typing import Optional

from pydantic import BaseModel


class Boo(BaseModel):
    int: Optional[int] = None

m = Boo(int=123) # Will fail to validate

# Because of how Python evaluates annotated assignment statements, # https://docs.python.org/3/reference/simple_stmts.html#annassign
# the statement is equivalent to int: None = None,
# thus leading to a validation error.


# Model methods and properties

# The example above only shows the tip fo the iceberg of what models can do.
# Models possess the following method and attributes:

# * model_validate(): Validates the given object against the Pydantic model. See Validating data. # https://docs.pydantic.dev/latest/concepts/models/#validating-data
# * model_validate()json()
# * model_construct()
# * model_dump() # Returns a dictionary of the model's field and values. See Serialization
# * model_dump_json()
# * model_copy() # by default, returns a shallow copy
# * model_json_schema()
# * model_fields
# * model_computed_fields
# * model_extra
# * model_fields_set
# * model_parametrized_name()
# * model_post_init()
# * model_rebuild() # Rebuilds the model schema, which also supports building recursive generic models. See Rebuilding model schema.

# Note
# See the API documentation of BaseModel // https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel
# for the class definition including a full list of methods and attributes

# Tip
# See Changes to pydantic.BaseModel // https://docs.pydantic.dev/latest/migration/#changes-to-pydanticbasemodel
# in the Migration Guide // https://docs.pydantic.dev/latest/migration/
# for details on changes from Pydantic V1.


# Data conversion

# Pydantic may cast input data to force it to conform to model field types,
# and in some cases this may result in a loss of information. For example:

from pydantic import BaseModel

class Model(BaseModel):
        a: int
        b: float
        c: str

print(Model(a=3.000, b='2.72', c=b'binary data').model_dump())
#> {'a': 3, 'b': 2.72, 'c': 'binary data'}


# ...

# This is aso the case for collections.
# In most cases, you shouldn't make use of abstract container classes
# and just use a concrete type, such as list:

from pydantic import BaseModel


class Model(BaseModel):
    items: list[int]

print(Model(items=(1, 2, 3)))
#> items=[1, 2, 3]

# Besides, using these abstract types can also lead to poor validation performance, # https://docs.pydantic.dev/latest/concepts/performance/#sequence-vs-list-or-tuple-with-mapping-vs-dict
# and in general using concrete container types will avoid unnecessary checks.


# Extra data

# By default, Pydantic models won't error when you provide extra data,
# and these values will simply be ignored:

from pydantic import BaseModel


class Model(BaseModel):
    x: int

m = Model(x=1, y='a')
assert m.model_dump() == {'x': 1}


# The extra configuration value can be used to control this behavior:

from pydantic import BaseModel, ConfigDict


class Model(BaseModel):
    x: int

    model_config = ConfigDict(extra='allow')


m = Model(x=1, y='a')
assert m.model_dump() == {'x': 1, 'y': 'a'}
assert m.__pydantic_extra__ == {'y': 'a'}

# The configuration can take three calues:
# * 'ignore': Providing extra data is ignored (the default).
# * 'forbig': Providing extra data is not permitted.
# * 'allow': Provding extra data is allowed and stored in the __pidantic_extra_dictionary attributes.
# The __pidantic_extra_ can explicityl be annotated to provide validation for extra fields

# For more details, refer to the extra API documentation. # https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.extra

# Nested models

# More complex hierarchical data structues can be defined using models themselves
# as types in annotations.

# Python 3.9 and above

from typing import Optional

from pydantic import BaseModel


class Foo(BaseModel):
    count: int
    size: Optional[float] = None

class Bar(BaseModel):
    apple: str = 'x'
    banana: str = 'y'

class Spam(BaseModel):
    foo: Foo
    bars: list[Bar]

m = Spam(foo={'count': 4}, bars=[{'apple': 'x1'}, {'apple': 'x2'}])
print(m)
"""
foo=Foo(count=4, size=None) bars=[Bar(apple='x1', Bar(apple='x2', banana='y'))]
"""
print(m.model_dump())
"""
    'foo': {'count': 4, 'size': None},
    'bars': [{'apple': 'x1', 'banana': 'y'}, {'apple': 'x2', 'banana': 'y'}],
"""

# Self-referencing models are supported. 
# For more details, see the documentation related to forward annotations. # https://docs.pydantic.dev/latest/concepts/forward_annotations/#self-referencing-or-recursive-models


# Rebuilding model schemas

# ...

form pydantic import BaseModel, PydanticUserError


class Foo(BaseModel):
    x: 'Bar'


try:
    Foo.model_json_schema()
except PydanticUserError as e:
        print(e)
        """
        'Foo' is not fully defined; you should define `Bar`, then call `Foo.model_rebuild()`.

        For further information visit https://errors.pydantic.dev/2/u/class-not-fully-defined
        """


class Bar(BaseModel):
    pass


Foo.model_rebuilt()
print(Foo.model_json_schema())
"""
{
    '$defs': {'Bar': {'properties': {}, 'title': 'Bar', 'type': 'object'}},
    'properties': {'x': {'$ref': '#/$defs/Bar'}},
    'required': ['x'],
    'title': 'Foo',
    'type': 'object',
}
"""


# Arbitrary classinstances 

# (Formerly known as "ORM Mode"/ from_orm). 

# ...

# The example here uses SQLAlchemy,
# but the same approach should work for any ORM.

from typing import Annotated

from sqlalchemy import ARRAY, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from pydantic import BaseModel, ConfigDict, StringConstraints


class Base(DeclarativeBase):
    pass


class CompanyOrm(Base):
    __tablename__ = 'companies'

    if: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    public_key: Mapped[str] = mapped_column(
        String(20), index=True, nullable=False, unique=True
    )
    domains: Mapped[list[str]] = mapped_column(ARRAY(String(25)))


class CompanyModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    public_key: Annotated[str, StringConstraints(max_length=20)]
    domains: list[Annotated[str, StringConstraints(max_length=255)]]


co_orm = CompanyOrm(
    id=123,
    public_key='foobar',
    domains=['example.com', 'foobar.com'],
)
print(co_orm)
#> <__main__.CompanyOrm object at 0x0123456789ab>
co_model = CompanyModel.model_validate(co_orm)
print(co_model)
#> id=123 public_key='foobar' domains=['example.com', 'foobar.com']


# Nested attributes

# When using attributes to parse models,
# model instances will be created from both top-lvel attributes
# and deeper-nested attributes as appropriate.

# Here is an example demonstrating the principle:

from pydantic import BaseModel, ConfigDict


class PetClt:
    def __init__(self, *, name: str, species: str):
            self.name = name
            self.species = species


class PersonCls:
    def __init__(self, *, name: str, age: float = None, pets: list[PetCls]):
        self.name = name
        self.age = age
        self.pets = pets
        

class Pet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    species: str


class Person(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    age: float = None
    pets: list[Pet]


bones = PetCls(name='Bones', species='dog')
orion = PetCls(name='Orion', species='cat')
anna = PersonCls(name='Anna', age=20, pets=[bones, orion])
anna_model = Person.model_validate(anna)
print(anna_model)
"""
name='Anna' age = 20.0 pets=[Pet(name='Bones', species='dog'), Pet(name='Orion', species='cat')]
"""


# Error handling
# ...

from pydantic import BaseModel, ValidationError

class Model(BaseModel):
    list_of_ints: list[int]
    a_float: float

data = dict(
    list_of_ints=['1', 2, 'bad'],
    a_float='not a float',
)

try:
    Model(**data)
except ValidationError as e:
    print(e)
    """
    2 validation errors for Model
    list_of_ints.2
        Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='bad', input_type=str]
    a_float
        Input should be a valid number, unable to parse string as a number [type=float_parsing, input_value='not a float', input_type=str]    
    """


# Validating data

# Pydantic provides three methods on models classes for parsing data:

# * model_validate()

# * model_validate_json()

# * model_validate_strings()


# Python 3.9 and above

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ValidationError

class User(BaseModel):
    id: int
    name: str = 'John Doe'
    signup_ts: Optional[datetime] = None

m = User.model_validate({'id': 123, 'name': 'James'})
print(m)
#> id=123 name='James' signup_ts=Nine

try:
    User.model_validate(['not', 'a', 'dict'])
except ValidationError as e:
    print(e)
    """
    1 validation error for User
      Input should be a valid dictionary or instance of User [type=model_type, input_value=['not', 'a', 'dict], input_type=list]
    """

m = User.model_validate_json('{"id": 123, "name": "James"}')
print(m)
#> id=123 name='Jmaes' signup_rs=None

try:
    m = User.model_validate_json('{"id": 123, "name": 123}')
except ValidationError as e:
    print(e)
    """
    1 validation error for User
    name
      Input should be a valid string [type=string_type, input_value=123, input_type=int]
    """

try:
    m = User.model_validate_json('invalid JSON')
except ValidationEror as e:
    print(e)
    """
    1 validation error for User
      Invalid JSON: expected value at line 1 column 1 [type=json_invalid, input_value='invalid JSON', input_type=str]
    """

m = User.model_validate_strings({'id': '123', 'name': 'James'})
print(m)
#> id=123 name='James' signup_ts=datetime.datetime(2024, 4, 1, 12, 0)

try:
    m = User.model_validate_string(
        {'id': '123', 'name': 'James', 'signup_ts': '2024-04-01'}, strict=True
    )
except ValidationError as e:
    print(e)
    """
    1 validation error for User
    signup_ts
      Input should be a valid datetime, invalid datetime separator, expected `T`, 't', `_` or space [type=datetime_parsing, input_value='2024-04-01', input_type=str]
    """
`

# NEVER # revalidate_instances='never'

from pydantic import BaseModel


class Model(BaseModel):
    a: int

m = Model(a=0)
# note: setting `validate_assignment` to `True` in the config can prevent this kind of misbehavior
m.a = 'not an int'

# doesn't raise a validation error even though m is invalid
m2 = Model.model_validate(m)


# ALWAYS revalidate_instances='always'

from pydantic import BaseModel, ConfigDict, ValidationError


class Model(BaseModel):
    a: int

    model_config = ConfigDict(revalidate_instances='always')

m = Model(a=0)
# note: setting `validate_assignment` to `True` in the config can prevent this kind of misbehavior.
m.a = 'not an int' 

try:
    m2 = Model.model_validate(m)
except ValidationError as e:
    print(e)
    """
    1 validation error for Model
    a
        Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='not an int', input_type=str]
    """


# Generic models

# Pydantic supports the cration of generic models to make it easier to reuse a
# common model structure. Both the new type parameter syntax (introduced 
# by PEOP 695 in Python 3.12) and the old syntax are supported
# (refer to the Python documentation for more details).

# Here is an example using a generic Pydantic model
# to create an easily-reused HTTP response payload wrapper.

from typing import Generic, TypeVar

from pydantic import BaseModel, ValidationError

DataT = TypeVar('DataT')


class DataModel(BaseModel):
    number: int


class Response(BaseModel, Generic[DataT]):
    data: DataT


print(Response[int](data=1))
#> data=1
print(Response[str](data='value'))
#> data='value'
print(Response[str](data='value').model_dump())
#> {'data': 'value'}

data = DataModel(number=1)
print(Response[DataModel](data=data).model_dump())
#> {'data': {'number': 1}}
try:
    Response[int](data='value')
try:
    Response[int](data='value')
except ValidationError as e:
    print(e)
    """
    1 validation error for Response[int]
    data
      Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='value', input_type=str]
    """


# Python 3.12 and above (new syntax)

prom pydantic import BaseModel, ValidationError


class DataModel(BaseModel):
    number: int


class Response[DataT](BaseModel):
    data: DataT


print(Response[int](data=1))
#> data=1
print(Response[str](data='value'))
#> data='value'
print(Response[str](data='value').model_dump())
#> {'data': 'value'}

data = DataModel(number=1)
print(Response[DataModel](data=data).model_dump())
#> {'data': {'number': 1}}
try:
    Response[int](data='value')
except ValidationError as e:
    print(e)
    """
    1 validation error for Response[int]
    data
      Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='value', input_type='str]
    """


# ...

# To inherit from a generic model and preserve the fact that it is generic,
# the subclass must also inherit from Generic:

from typing import Generic, TypeVar`

from pydantic import BaseModel

TypeX = TypeVar('TypeX')


class BaseClass(BaseModel, Generic[TypeX]):
    X: TypeX


class ChildClass(BaseClass[TypeX], Generic[TypeX]):
    pass


# Parametrize `TypeX` with `int`:
print(ChildClass[int](X=1))
#> X=1


# You can also create a generic subclass of a model
# that partially or fully replaces the type variables in the superclass:

from typing import Generic, TypeVar

from pydantic import BaseModel

TypeX = TypeVar('TypeX')
TypeY = TypeVar('TypeY')
TypeZ = TypeVar('TypeZ')


class BaseClass(BaseModel, Generic[TypeX, TypeY]):
    x: TypeX
    y: TypeY


class ChildClass(BaseClass[int, TypeY], Generic[TypeT, TypeZ]):
    x: TypeX
    y: TypeY


class ChildClass(BaseClass[int, TypeY], Generic[TypeY, TypeZ]):
    z: TypeZ


# Parametrize `TypeY` with `str`:
print(ChildClass[str, int](x='1', y='y', z='3'))
#> x=1 y='y' z=3


