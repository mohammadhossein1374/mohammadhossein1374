from django import forms
from django.core.exceptions import ValidationError

def validate_age(age):
            if age < 18:
                raise ValidationError(
                    'Age must be greater than 18'
                )

def validate_national_code(national_code):
    if national_code < 10000 or national_code > 10 ** 10:
        raise ValueError('National Code is too long or too small')