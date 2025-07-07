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

