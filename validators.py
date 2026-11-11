from abc import ABC, abstractmethod

import phonenumbers
from email_validator import EmailNotValidError, validate_email
from phonenumbers import NumberParseException
from errors import ValidationError

class Validator(ABC):

    @abstractmethod
    def validate(self, value):
        pass


class EmailValidator(Validator):

    def validate(self, value):
        try:
            result = validate_email(
                value.strip(),
                check_deliverability=False
            )
            return result.normalized.lower()

        except (EmailNotValidError, TypeError, ValueError):
            raise ValidationError("Invalid email.")

class PhoneValidator(Validator):

    def __init__(self, region):
        self._region = region

    def validate(self, value):
        try:
            num = phonenumbers.parse(value, self._region)

            if phonenumbers.is_valid_number(num):
                return phonenumbers.format_number(
                    num,
                    phonenumbers.PhoneNumberFormat.E164
                )

            raise ValidationError("Invalid phone number.")

        except NumberParseException:
            raise ValidationError("Invalid phone number.")

