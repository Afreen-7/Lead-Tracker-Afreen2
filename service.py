from models import Lead, LeadStatus
from errors import ValidationError, LeadNotFoundError, DuplicateLeadError


class LeadService:

    HOT_PERCENT = 90
    WARM_PERCENT = 50

    FOLLOW_UP_CHANNELS = ("email", "sms", "whatsapp")

    def __init__(self, repository, catalog, email_validator, phone_validator):
        self._repository = repository
        self._catalog = catalog
        self._email_validator = email_validator
        self._phone_validator = phone_validator

    def check_phone(self, phone):
        return self._phone_validator.validate(phone)

    def check_email(self, email):
        return self._email_validator.validate(email)

    def get_locations(self):
        return self._catalog.get_locations()

    
    def add_lead(
        self,
        full_name,
        phone,
        email,
        source,
        budget_min,
        budget_max,
        category,
        interested_locations
    ):

        name_parts = full_name.split()

        if not name_parts:
            raise ValidationError("Name cannot be empty.")

        first_name = name_parts[0]
        last_name = name_parts[-1] if len(name_parts) > 1 else None
        middle_name = " ".join(name_parts[1:-1]) or None

        phone = self.check_phone(phone)
        email = self.check_email(email)

        if self._repository.find_by_email(email):
            raise DuplicateLeadError("This email is already registered.")

        if self._repository.find_by_phone(phone):
            raise DuplicateLeadError("This phone number is already registered.")

        lowest_price = self._catalog.get_lowest_price(
            category,
            interested_locations
        )

        budget = {
            "min": budget_min,
            "max": budget_max
        }

        tag = self._calculate_tag(budget_max, lowest_price)

        follow_up = self._get_follow_up_channels(tag)

        lead = Lead(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            phone=phone,
            email=email,
            source=source,
            status=LeadStatus.NEW,
            budget_min=budget_min,
            budget_max=budget_max,
            category=category,
            interested_locations=interested_locations,
            tag=tag,
            lowest_price=lowest_price,
            follow_up=follow_up
        )

        self._repository.add(lead)

        return lead


    def list_leads(self):
        return self._repository.get_all()

    def search(self, text):
        text = text.strip().lower()

        if not text:
            return []

        return [
            lead for lead in self._repository.get_all()
            if text in lead.full_name.lower()
            or text in lead.email.lower()
            or text in lead.phone.lower()
        ]

    def find_by_contact(self, contact):

        contact = contact.strip()

        lead = self._repository.find_by_email(contact)

        if lead is None:
            lead = self._repository.find_by_phone(contact)

        if lead is None:
            raise LeadNotFoundError("No lead found with this contact.")

        return lead

    def change_status(self, lead_id, new_status):

        lead = self._repository.get_by_id(lead_id)

        if lead is None:
            raise LeadNotFoundError(
                f"Lead with ID {lead_id} was not found."
            )

        lead.change_status(new_status)

        self._repository.update(lead)

        return lead

    def delete_lead(self, lead_id):

        lead = self._repository.get_by_id(lead_id)

        if lead is None:
            raise LeadNotFoundError(
                f"Lead with ID {lead_id} was not found."
            )

        self._repository.delete(lead_id)

        return lead

    def _calculate_tag(self, budget_max, lowest_price):

        if lowest_price is None:
            return "cold"

        percent = budget_max / lowest_price * 100

        if percent >= self.HOT_PERCENT:
            return "hot"

        if percent >= self.WARM_PERCENT:
            return "warm"

        return "cold"

    def _get_follow_up_channels(self, tag):

        if tag == "cold":
            return list(self.FOLLOW_UP_CHANNELS)

        return []