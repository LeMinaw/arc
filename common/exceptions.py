from functools import wraps

from django.core.exceptions import ValidationError
from rest_framework import serializers


def to_serializer_validation_error(function):
    """Catches any Django `ValidationError` and re-raises it as a DRF
    `serializers.ValidationError`."""

    @wraps(function)
    def decorated(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except ValidationError as err:
            raise serializers.ValidationError(
                serializers.as_serializer_error(err)
            ) from err

    return decorated
