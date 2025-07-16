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
    

