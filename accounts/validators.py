import re
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
import os


def valid_email(value):
    try:
        EmailValidator()(value)
    except ValidationError as e:
        raise ValidationError('Invalid email address')


def allow_only_images_validator(value):
    ext = os.path.splitext(value.name)[1]  # cover-image.jpg
    print(ext)
    valid_extensions = ['.png', '.jpg', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Allowed extensions: ' + str(valid_extensions))


def validate_csv_file_extension(value):
    allowed_extensions = ['.xls', '.xlsx']
    if not value.name.endswith(tuple(allowed_extensions)):
        raise ValidationError('Only XLS or XLSX files are allowed.')


def validate_numeric(value):
    pattern = r'^\d+$'
    if not re.match(pattern, value):
        raise ValidationError('Please enter a numeric value.')


def validate_length(value):
    if len(value) < 10:
        raise ValidationError('The value must have a minimum length of 10 characters.')
    elif len(value) > 10:
        raise ValidationError('The value cannot exceed 10 characters.')
