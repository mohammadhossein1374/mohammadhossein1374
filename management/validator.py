from django import forms
from django.core.exceptions import ValidationError

def validate_length(length):
            if not length > 0:
                raise ValidationError(
                    'Length must be greater than zero'
                )
def validate_load_volume(load_volume):
    if not load_volume > 0:
        raise ValidationError(
            'load_volume must be greater than zero'
        )

def validate_type_volume(type, volume):
    if type == 'small' and not volume :
        raise ValidationError(
            'Small Type cars can not have volum_load'
        )

