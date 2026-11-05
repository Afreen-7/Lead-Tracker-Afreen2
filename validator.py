from abc import ABC, abstractmethod


class Validator(ABC):

    @abstractmethod
    def validate(self, value):
        pass


class EmailValidator(Validator):

    def validate(self, value):
        pass


class PhoneValidator(Validator):

    def validate(self, value):
        pass