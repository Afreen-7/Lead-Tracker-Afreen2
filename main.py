
from repository import JsonLeadRepository
from catalog import PropertyCatalog
from service import LeadService
from console_app import ConsoleApp

from validators import EmailValidator, PhoneValidator


def main():


    repository = JsonLeadRepository("leads.json")


    catalog = PropertyCatalog("property_locations.json")


    email_validator = EmailValidator()
    phone_validator = PhoneValidator(region="AE")


    service = LeadService(
        repository=repository,
        catalog=catalog,
        email_validator=email_validator,
        phone_validator=phone_validator
    )

    app = ConsoleApp(service)

    app.run()


if __name__ == "__main__":
    main()
