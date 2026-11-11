from repository import JsonLeadRepository
from models import Lead, LeadStatus


repository = JsonLeadRepository("temp_file.json")

lead = Lead(
    first_name="Afia",
    middle_name=None,
    last_name="Tahir",
    phone="03001234567",
    email="Afia.test@gmail.com",
    source="website",
    status=LeadStatus.NEW,
    budget_min=50000,
    budget_max=100000,
    category="2 bed",
    interested_locations=["JVC", "Dubai Marina"]
)

repository.add(lead)

print("Lead added successfully!")

print(repository.get_all())

print(repository.get_by_id(lead.id))

print(repository.find_by_email("afreen.test@gmail.com"))

print(repository.find_by_phone("03001234567"))