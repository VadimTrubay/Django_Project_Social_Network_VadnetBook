import re
from datetime import datetime, date

from django.core.exceptions import ValidationError


def validate_file_size(value):
    max_size = 1024 * 1024
    if value.size > max_size:
        raise ValidationError("No more than 1 MB")


def phone_number_validator(value):
    # Regular expression to validate phone number (e.g. international format)
    phone_regex = re.compile(r"^\+?1?\d{9,15}$")
    if not phone_regex.match(value):
        raise ValidationError(
            'The phone number must be in the format: "+999999999". Up to мах 15 digits are allowed.'
        )


def birth_date_validator(value):
    """
    Валидатор для проверки даты рождения. Убедитесь, что дата рождения соответствует формату 'DD.MM.YYYY',
    не находится в будущем и пользователю не менее 18 лет.
    """
    try:
        # Преобразование строки в дату формата 'DD.MM.YYYY'
        birth_date = datetime.strptime(value, "%d.%m.%Y").date()
    except ValueError:
        raise ValidationError("Дата рождения должна быть в формате 'DD.MM.YYYY'.")

    today = date.today()

    # Проверка, чтобы дата рождения не была в будущем
    if birth_date > today:
        raise ValidationError("Дата рождения не может быть в будущем.")

    # Проверка, чтобы пользователю было не менее 18 лет
    age = (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )
    if age < 18:
        raise ValidationError("Пользователь должен быть старше 18 лет.")
