import uuid

leads = []

SOURCES = ("website", "bayut", "propertyfinder")
STATUSES = ("new", "contacted", "qualified", "won", "lost")

def add_lead():
    first_name = input("Enter your first name; ")
    last_name = input("Enter your last name: ")    
    phone_number = input("Enter your phone number: ")
    source = input("Enter source (Website, Property Finder, Bayut): ").strip().lower()
    email = input("Enter your email: ")
    if not first_name or not last_name or not phone_number or not email:
        print("First_name, Last_name, phone, email are required")
        return

    phone_digits = phone_number[1:] if phone_number.startswith("+") else phone_number
    
    if not phone_digits or not phone_digits.isdigit():
        print("Invalid phone. Use digits only, with an optional + at the start.")
        return

    if email.count("@") != 1:
        print("Invalid email. Email must contain exactly one @.")
        return

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
    print("lead successfully added")
    print(f"Lead Generated Successfuly ID: {lead['id']}")


def lead_list():
    if not leads:
        print("No leads found.")
        return

    print("-" * 145)
    print(
        f"{'ID':<38}"
        f"{'FIRST NAME':<15}"
        f"{'LAST NAME':<15}"
        f"{'PHONE':<17}"
        f"{'EMAIL':<28}"
        f"{'SOURCE':<18}"
        f"{'STATUS':<12}"
    )
    print("-" * 145)

    for lead in leads:
        print(
            f"{lead['id']:<38}"
            f"{lead['first_name']:<15}"
            f"{lead['last_name']:<15}"
            f"{lead['phone_number']:<17}"
            f"{lead['email']:<28}"
            f"{lead['source']:<18}"
            f"{lead['status']:<12}"
        )

    print("-" * 145)

def change_status():
    lead_id = input("Enter lead ID")

    for lead in leads:
        if lead["id"] == lead_id:
            status = input(" Enter status (new/contacted/qualified/won/lost):")
                            
        if status not in STATUSES:
            print("invalid status")
            return
        
        lead["status"] = status
        print("status update sucessfully")
        return

    print("Lead Id not found")


def searh_lead():
    first_name = input("enter name for search").lower()
    found = False

    for lead in leads:
            if first_name in lead["first_name"].lower():
                print(lead)
                found = True

    if not found:
        print("lead not found")

def delete_lead():
    lead_id = input("Enter thelead ID to delete")

    for lead in leads:
        if lead["id"] == lead_id:
            leads.remove(lead)
            print("lead remove successfully")
            return 
    
    print("lead ID not found")


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