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
        pass

    def check_email(self, email):
        pass

    def get_locations(self):
        pass

    def add_lead(
        self,
        first_name,
        middle_name,
        last_name,
        phone,
        email,
        source,
        budget_min,
        budget_max,
        category,
        interested_locations
    ):
        pass

    def list_leads(self):
        pass

    def search(self, text):
        pass

    def find_by_contact(self, contact):
        pass

    def change_status(self, lead_id, new_status):
        pass

    def delete_lead(self, lead_id):
        pass

    def _calculate_tag(self, budget_max, lowest_price):
        pass

    def _get_follow_up_channels(self, tag):
        pass