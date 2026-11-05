from abc import ABC, abstractmethod


class LeadRepository(ABC):

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, lead_id):
        pass

    @abstractmethod
    def find_by_email(self, email):
        pass

    @abstractmethod
    def find_by_phone(self, phone):
        pass

    @abstractmethod
    def add(self, lead):
        pass

    @abstractmethod
    def update(self, lead):
        pass

    @abstractmethod
    def delete(self, lead_id):
        pass


class JsonLeadRepository(LeadRepository):

    def __init__(self, file_path):
        pass

    def get_all(self):
        pass

    def get_by_id(self, lead_id):
        pass

    def find_by_email(self, email):
        pass

    def find_by_phone(self, phone):
        pass

    def add(self, lead):
        pass

    def update(self, lead):
        pass

    def delete(self, lead_id):
        pass

    def _read(self):
        pass

    def _write(self):
        pass