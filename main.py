import csv
import os
import uuid
import phonenumbers
from validators import is_valid_email, is_valid_phone
from phonenumbers import carrier, geocoder, timezone

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leads.csv")
FIELDS = ["id", "first_name", "last_name", "phone_number", "email", "source", "status"]

def save_leads():
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(leads)

def load_leads():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

leads = load_leads()


SOURCES = ("website", "bayut", "property finder")
STATUSES = ("new", "contacted", "qualified", "won", "lost")
TRANSITIONS = {
    "new": ["contacted"],
    "contacted": ["qualified", "lost"],
    "qualified": ["won", "lost"],
    "won": [],
    "lost": [],
}

def add_lead():
    first_name = input("Enter your first name; ")
    last_name = input("Enter your last name: ")    
    phone_number = input("Enter your phone number: ")
    source = input(f"Enter source ({', '.join(s.title() for s in SOURCES)}): ").strip().lower()

  
    cleaned_phone = is_valid_phone(phone_number)
    if not cleaned_phone:
        print("Invalid phone number.")
        return
    phone_number = cleaned_phone

    email = input("Enter your email: ")
    cleaned = is_valid_email(email)

    if not cleaned:
        print("Invalid email")
        return

    email = cleaned     

    if source not in SOURCES:
        print("Invalid Source")
        return

    lead = {
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


def lead_list():
    if not leads:
        print("No leads found.")
        return

    headers = ["ID","First name","Last name","Email","Phone Number","Source","Status"]
    keys = ["id", "first_name", "last_name", "phone_number", "email", "source", "status"]

    widths = [
        max(len(h), *(len(str(lead[k])) for lead in leads))
        for h, k in zip(headers, keys)
    ]

    print(" | ".join(h.ljust(w) for h, w in zip(headers, widths)))

    for lead in leads:
        print(" | ".join(str(lead[k]).ljust(w) for k, w in zip(keys, widths)))

def change_status():
    email = input("Enter lead email: ").strip()
    cleaned = is_valid_email(email)

    if not cleaned:
        print("Invalid email")
        return

    for lead in leads:
        if lead["email"] == cleaned:
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


def searh_lead():
    email = input("enter email to search: ").lower()
    cleaned = is_valid_email(email)

    if not cleaned:
        print("Invalid email")
        return


    for lead in leads:
            if lead["email"] == cleaned:
                print(lead)
                return
    
    print("lead not found")

def delete_lead():
    email = input("Enter your email to delete: ").strip()
    cleaned = is_valid_email(email)

    if not cleaned:
        print("Invalid email")
        return
    
    for lead in leads:
        if lead["email"] == cleaned:
            leads.remove(lead)
            save_leads()
            print("lead remove successfully")
            return 
    
    print("Email not found")


while True:
    print("\n=== PROPERTY LEAD TRACKER ===")
    print("1. Add Lead")
    print("2. List Leads")
    print("3. Search Lead by Name")
    print("4. Change Lead Status")
    print("5. Delete Lead by ID")
    print("6. Quit")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        add_lead()
    elif choice == "2":
        lead_list()
    elif choice == "3":
        searh_lead()
    elif choice == "4":
        change_status()
    elif choice == "5":
        delete_lead()
    elif choice == "6":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Try again.")
