from mongoengine.errors import ValidationError


def not_null(value):
    if not value:
        raise ValidationError("Field cannot be null or empty")