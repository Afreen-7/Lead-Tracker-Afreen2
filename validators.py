import phonenumbers
from email_validator import EmailNotValidError, validate_email
from phonenumbers import NumberParseException


def is_valid_email(email):
    try:
        result = validate_email(email, check_deliverability=False)
        return result.normalized
    except EmailNotValidError:
        return None

def is_valid_phone(phone, region="AE"):
    try:
        num = phonenumbers.parse(phone, region)
        if phonenumbers.is_valid_number(num):
            return phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.E164)
        return None
    except NumberParseException:
        return None