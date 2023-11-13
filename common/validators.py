from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.deconstruct import deconstructible
from jsonschema import Draft202012Validator, SchemaError, ValidationError, validators


class DefaultValidatorFactory:
    def __init__(self, base_validator):
        """Returns an extended copy of a validator filling in default values.

        Default properties are added to each object before the properties are validated,
        so the default values themselves will need to be valid under the schema.
        """
        self.base_validator = base_validator

    def __call__(self):
        return validators.extend(
            self.base_validator, {"properties": self._set_defaults}
        )

    def _set_defaults(self, validator, properties, instance, schema):
        for property_, subschema in properties.items():
            if "default" in subschema:
                instance.setdefault(property_, subschema["default"])

        # Yield errors
        validate_properties = self.base_validator.VALIDATORS["properties"]
        yield from validate_properties(validator, properties, instance, schema)


@deconstructible
class JSONSchemaValidator:
    VALIDATOR = DefaultValidatorFactory(Draft202012Validator)()

    def __init__(self, schema=None):
        """Build a validator that is used to validate a value against a provided JSON
        schema.

        If no `schema` is provided, the validator will check the validity of the value
        against the `Draft 2020-12` meta-schema itself.
        """
        self.schema = schema

    def __call__(self, value):
        try:
            self.validate(value)
        except (SchemaError, ValidationError) as e:
            raise DjangoValidationError(e.message) from e

    def validate(self, value):
        if self.schema is None:
            return self.VALIDATOR.check_schema(value)

        return self.VALIDATOR(self.schema).validate(value)
