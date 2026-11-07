from abc import ABC, abstractmethod
import phonenumbers
from email_validator import EmailNotValidError, validate_email
from phonenumbers import NumberParseException


class ValidationError(Exception):
    pass


class Validator(ABC):

    @abstractmethod
    def validate(self, value):
        pass


class EmailValidator(Validator):

    def validate(self, value):
        try:
            result = validate_email(value, check_deliverability=False)
            return result.normalized
        except EmailNotValidError as e:
            raise ValidationError(str(e))


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

            raise ValidationError("Invalid phone number")

        except NumberParseException as e:
            raise ValidationError(str(e))
