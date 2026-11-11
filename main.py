import json
import os
import uuid

from validators import EmailValidator, PhoneValidator
from errors import ValidationError

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leads.json")

def save_leads():
    tmp = DATA_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=4)
    os.replace(tmp, DATA_FILE)


def load_leads():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise SystemExit(f"{DATA_FILE} is broken. Fix or restore it, then run again.")
    
leads = load_leads()


PROJECTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "property_locations.json")

email_validator = EmailValidator()
phone_validator = PhoneValidator("AE")


def validate_email_input(prompt):
    while True:
        email = input(prompt).strip().lower()

        try:
            return email_validator.validate(email)
        except ValidationError as e:
            print(e)


def validate_phone_input(prompt):
    while True:
        phone = input(prompt).strip()

        try:
            return phone_validator.validate(phone)
        except ValidationError as e:
            print(e)

def load_locations(projects):
    seen = []

    for project in projects:
        loc = project["location"]
        pair = (loc["area"], loc["community"])

        if pair not in seen:
            seen.append(pair)

    return seen

SOURCES = ("website", "bayut", "property finder")
STATUSES = ("new", "contacted", "qualified", "won", "lost")
TRANSITIONS = {
    "new": ["contacted", "lost"],
    "contacted": ["qualified", "lost"],
    "qualified": ["won", "lost"],
    "won": [],
    "lost": [],
}

CATEGORIES = ("studio", "1 bed", "2 bed", "3 bed")

def ask_name():
    while True:
        full_name = " ".join(input("Enter your name: ").split()).title()
        if not full_name:
            print("Name cannot be empty.")
            continue
        parts = full_name.split(" ")
        first_name = parts[0]
        last_name = parts[-1] if len(parts) > 1 else ""
        middle_name = " ".join(parts[1:-1])
        return full_name, first_name, middle_name, last_name

def ask_number(prompt):
    while True:
        raw = input(prompt).strip().replace(",", "")
        if raw.isdigit() and int(raw) > 0:
            return int(raw)
        print("Please enter a valid positive number.")

def ask_budget():
    min_budget = ask_number("Enter minimum budget: ")
    while True:
        max_budget = ask_number("Enter maximum budget: ")
        if max_budget >= min_budget:
            return {"min": min_budget, "max": max_budget}
        print(f"Maximum budget must be at least {min_budget}.")

def ask_category():
    print("\nApartment category:")
    for i, c in enumerate(CATEGORIES, 1):
        print(f"  {i}. {c.title()}")

    while True:
        choice = input("Choose a category (number): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            return CATEGORIES[int(choice) - 1]
        print("Invalid choice. Enter a number from the list.")

def choose_locations(locations):
    for i, (area, community) in enumerate(locations, start=1):
        print(f"{i}. {area} / {community}")

    while True:
        raw = input("Choose 2 or more locations (e.g. 1,3,5): ")
        parts = [p.strip() for p in raw.split(",") if p.strip()]

        if not all(p.isdigit() for p in parts):
            print("Please enter numbers only.")
            continue

        numbers = sorted({int(p) for p in parts})

        if any(n < 1 or n > len(locations) for n in numbers):
            print(f"Numbers must be between 1 and {len(locations)}.")
            continue

        if len(numbers) < 2:
            print("Please choose at least 2 different locations.")
            continue

        return [
            {"area": locations[n - 1][0], "community": locations[n - 1][1]}
            for n in numbers
        ]

HOT_PERCENT = 90
WARM_PERCENT = 50
FOLLOW_UP_CHANNELS = ["email", "sms", "whatsapp"]

CATEGORY_KEYS = {
    "studio": "studio",
    "1 bed": "1_bed",
    "2 bed": "2_beds",
    "3 bed": "3_beds",
}

def load_projects():
    try:
        with open(PROJECTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

    except FileNotFoundError:
        raise SystemExit("property_locations.json not found")

    return data.get("off_plan_projects", []) + data.get("ready_projects", [])

projects = load_projects()
locations = load_locations(projects)

def get_lowest_price(category, interested_locations):
    key = CATEGORY_KEYS[category]
    prices = []
    for project in projects:
        loc = project["location"]
        for chosen in interested_locations:
            if loc["area"] == chosen["area"] and loc["community"] == chosen["community"]:
                price = project.get("prices_by_category", {}).get(key)
                if price:
                    prices.append(price)
    return min(prices) if prices else None

def get_tag(budget, category, interested_locations):
    lowest_price = get_lowest_price(category, interested_locations)
    if lowest_price is None:
        return "cold", None

    percent = budget["max"] / lowest_price * 100

    if percent >= HOT_PERCENT:
        return "hot", lowest_price
    if percent >= WARM_PERCENT:
        return "warm", lowest_price
    return "cold", lowest_price

def add_lead():
    _full_name, first_name, middle_name, last_name = ask_name()
    source = input(f"Enter source ({', '.join(s.title() for s in SOURCES)}): ").strip().lower()

    if source not in SOURCES:
        print("Invalid Source")
        return
  
    phone_number = validate_phone_input("Enter your phone number: ")

    while True:
        email = validate_email_input("Enter your email: ")

        if any(lead.get("email", "").lower() == email.lower() for lead in leads):
            print("This email is already used. Try with a new email.")
            continue

        break

    budget = ask_budget()
    category = ask_category()
    interested_locations = choose_locations(locations)
    tag, lowest_price = get_tag(budget, category, interested_locations)
    follow_up = list(FOLLOW_UP_CHANNELS) if tag == "cold" else []    
    lead = {
        "middle_name": middle_name,
        "budget": budget,
        "category": category,
        "interested_locations": interested_locations,
        "tag": tag,
        "lowest_price": lowest_price,
        "follow_up": follow_up,
        "id" : str(uuid.uuid4()),
        "first_name" : first_name,
        "last_name" : last_name,
        "phone_number": phone_number,
        "source" : source,
        "email" : email,
        "status" : "new"
    }

    leads.append(lead)
    save_leads()                     
    print("lead successfully added")
    print(f"Lead Generated Successfuly ID: {lead['id']}")
    print(f"Tag: {tag.upper()}")

def lead_list():
    if not leads:
        print("No leads found.")
        return

    headers = ["ID","First name","Last name","Phone Number","Email","Source","Status","Tag"]
    keys = ["id", "first_name", "last_name", "phone_number", "email", "source", "status","tag"]

    widths = [
        max(len(h), *(len(str(lead.get(k, ""))) for lead in leads))
        for h, k in zip(headers, keys)
    ]

    print(" | ".join(h.ljust(w) for h, w in zip(headers, widths)))

    for lead in leads:
        print(" | ".join(str(lead.get(k, "")).ljust(w) for k, w in zip(keys, widths)))
        
def change_status():
    
    email = validate_email_input("Enter lead email: ")

    for lead in leads:
        if lead["email"] == email:
            current = lead["status"]
            options = TRANSITIONS[current]

            if not options:
                print(f"Lead is already '{current}'. Status can't be changed.")
                return

            print(f"Current status: {current}")
            status = input(f"Enter new status ({'/'.join(options)}): ").strip().lower()

            if status not in options:
                print(f"Invalid status. From '{current}' you can only move to: {', '.join(options)}")
                return

            lead["status"] = status
            save_leads()                     
            print("Status updated successfully")
            return

    print("Lead not found")


def search_lead():
    email = validate_email_input("Enter email to search: ")


    for lead in leads:
            if lead["email"] == email:
                print(lead)
                return
    
    print("lead not found")

def delete_lead():
    email = validate_email_input("Enter your email to delete: ")
    
    for lead in leads:
        if lead["email"] == email:
            leads.remove(lead)
            save_leads()
            print("lead removed successfully")
            return 
    
    print("Email not found")

def main():    
    while True:
        print("\n=== PROPERTY LEAD TRACKER ===")
        print("1. Add Lead")
        print("2. List Leads")
        print("3. Search Lead by Email")
        print("4. Change Lead Status")
        print("5. Delete Lead by Email")
        print("6. Quit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_lead()
        elif choice == "2":
            lead_list()
        elif choice == "3":
            search_lead()
        elif choice == "4":
            change_status()
        elif choice == "5":
            delete_lead()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")
if __name__ == "__main__":
    main()
