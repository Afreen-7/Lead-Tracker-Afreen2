
from catalog import PropertyCatalog
from unittest.mock import patch


catalog = PropertyCatalog("property_locations.json")

locations = catalog.get_locations()

assert len(locations) == len(set(locations))

dubai_marina = [
    location for location in locations
    if location[1] == "Dubai Marina"
]

assert len(dubai_marina) == 1

print("Test 1 passed: Locations are unique!")


selected_locations = [
    location for location in locations
    if location[1] in ("Arjan", "Business Bay")
]

lowest_price = catalog.get_lowest_price(
    "studio",
    selected_locations
)

assert lowest_price == 550000

print("Test 2 passed: Lowest studio price is 550000!")


fake_location = [("Dubai", "Nonexistent Community")]

result = catalog.get_lowest_price("studio", fake_location)

assert result is None

print("Test 3 passed: Non-existing location returns None!")


with patch("builtins.open", wraps=open) as mocked_open:

    catalog = PropertyCatalog("property_locations.json")

    assert mocked_open.call_count == 1

    catalog.get_locations()
    catalog.get_lowest_price("studio", selected_locations)
    catalog.get_lowest_price("2 bed", selected_locations)

    assert mocked_open.call_count == 1

print("Test 4 passed: File opened only once!")
