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


