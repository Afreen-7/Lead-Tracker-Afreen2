from abc import ABC, abstractmethod
import json
import os
import tempfile

from models import Lead
from errors import LeadNotFoundError


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
        self._file_path = file_path
        self._leads = self._read()

    def get_all(self):
        return list(self._leads)

    def get_by_id(self, lead_id):
        for lead in self._leads:
            if lead.id == lead_id:
                return lead

        return None

    def find_by_email(self, email):
        if email is None:
            return None

        email = email.lower()

        for lead in self._leads:
            if lead.email and lead.email.lower() == email:
                return lead

        return None

    def find_by_phone(self, phone):
        if phone is None:
            return None

        for lead in self._leads:
            if lead.phone == phone:
                return lead

        return None

    def add(self, lead):
        self._leads.append(lead)
        self._write()

    def update(self, lead):
        for index, existing_lead in enumerate(self._leads):

            if existing_lead.id == lead.id:
                self._leads[index] = lead
                self._write()
                return

        raise LeadNotFoundError(
            f"Lead with ID {lead.id} was not found."
        )

    def delete(self, lead_id):
        for index, lead in enumerate(self._leads):

            if lead.id == lead_id:
                del self._leads[index]
                self._write()
                return

        raise LeadNotFoundError(
            f"Lead with ID {lead_id} was not found."
        )

    def _read(self):

        if not os.path.exists(self._file_path):
            return []

        try:
            with open(self._file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

        except json.JSONDecodeError as error:
            raise ValueError(
                f"Invalid JSON in {self._file_path}: {error}"
            ) from error

        if not isinstance(data, list):
            raise ValueError(
                f"Invalid data in {self._file_path}: "
                "Expected a list of leads."
            )

        return [Lead.from_dict(item) for item in data]

    def _write(self):

        directory = os.path.dirname(
            os.path.abspath(self._file_path)
        )

        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=directory,
                suffix=".tmp",
                delete=False
            ) as temp_file:

                temp_path = temp_file.name

                json.dump(
                    [lead.to_dict() for lead in self._leads],
                    temp_file,
                    indent=2
                )

            os.replace(temp_path, self._file_path)

        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

