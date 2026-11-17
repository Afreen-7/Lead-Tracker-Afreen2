from pathlib import Path

from database import Database
from postgres_repository import PostgresLeadRepository
from catalog import PropertyCatalog
from validators import EmailValidator, PhoneValidator
from service import LeadService
from console_app import ConsoleApp


BASE_DIR = Path(__file__).resolve().parent


def main():

    database = Database()

    repository = PostgresLeadRepository(database)

    catalog = PropertyCatalog(BASE_DIR / "property_locations.json")

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
