from errors import ValidationError, LeadNotFoundError, DuplicateLeadError


class ConsoleApp:

    def __init__(self, service):
        self._service = service

    def run(self):
        while True:
            print("\n========== PROPERTY LEAD TRACKER ==========")
            print("1. Add Lead")
            print("2. List Leads")
            print("3. Search Lead")
            print("4. Change Lead Status")
            print("5. Delete Lead")
            print("6. Exit")

            choice = input("\nEnter your choice: ").strip()

            try:
                if choice == "1":
                    self.add_lead()
                elif choice == "2":
                    self.list_leads()
                elif choice == "3":
                    self.search_lead()
                elif choice == "4":
                    self.change_status()
                elif choice == "5":
                    self.delete_lead()
                elif choice == "6":
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice. Please try again.")

            except (
                ValidationError,
                LeadNotFoundError,
                DuplicateLeadError,
                ValueError
            ) as error:
                print(f"Error: {error}")

    
    def add_lead(self):
        print("\n---------- ADD NEW LEAD ----------")

        full_name = input("Enter your name: ").strip()
        phone = input("Enter phone number: ").strip()
        email = input("Enter email: ").strip()

        print("\nEnter your sources:")
        print("1. website")
        print("2. bayut")
        print("3. property finder")

        source_options = {
            "1": "website",
            "2": "bayut",
            "3": "property finder"
        }

        source_choice = input("Choose source: ").strip()
        source = source_options.get(source_choice)

        if source is None:
            print("Invalid source.")
            return

        try:
            budget_min = float(input("Enter minimum budget: "))
            budget_max = float(input("Enter maximum budget: "))
        except ValueError:
            print("Budget must be a number.")
            return

        print("\nAvailable categories:")
        print("1. studio")
        print("2. 1 bed")
        print("3. 2 bed")
        print("4. 3 bed")

        category_options = {
            "1": "studio",
            "2": "1 bed",
            "3": "2 bed",
            "4": "3 bed"
        }

        category_choice = input("Choose category: ").strip()
        category = category_options.get(category_choice)

        if category is None:
            print("Invalid category.")
            return

        locations = self._service.get_locations()

        if not locations:
            print("No property locations are available.")
            return

        print("\nAvailable locations:")

        for index, (area, community) in enumerate(locations, start=1):
            print(f"{index}. {area} - {community}")

        selected_locations = input(
            "\nEnter location numbers separated by commas (e.g. 1,2): "
        ).strip()

        try:
            selected_indexes = [
                int(number.strip()) - 1
                for number in selected_locations.split(",")
                if number.strip()
            ]

            if len(selected_indexes) < 2:
                print("Please select at least two locations.")
                return

            if len(set(selected_indexes)) != len(selected_indexes):
                print("You selected a location more than once.")
                return

            if any(index < 0 or index >= len(locations) for index in selected_indexes):
                print("Invalid location number.")
                return

        except ValueError:
            print("Please enter valid location numbers.")
            return

        interested_locations = [
            locations[index] for index in selected_indexes
        ]

        lead = self._service.add_lead(
            full_name=full_name,
            phone=phone,
            email=email,
            source=source,
            budget_min=budget_min,
            budget_max=budget_max,
            category=category,
            interested_locations=interested_locations
        )

        print("\nLead added successfully!")
        print(f"Lead ID: {lead.id}")
        print(f"Name: {lead.full_name}")
        print(f"Email: {lead.email}")
        print(f"Phone: {lead.phone}")
        print(f"Tag: {lead.tag}")
        print(f"Lowest property price: {lead.lowest_price}")


    def list_leads(self):
        leads = self._service.list_leads()

        if not leads:
            print("\nNo leads found.")
            return

        print("\n---------- ALL LEADS ----------")

        for lead in leads:
            self.display_lead(lead)

    def search_lead(self):
        contact = input("\nEnter email or phone number: ").strip()

        lead = self._service.find_by_contact(contact)

        print("\n---------- LEAD FOUND ----------")
        self.display_lead(lead)

    def change_status(self):
        contact = input("\nEnter lead email or phone number: ").strip()

        lead = self._service.find_by_contact(contact)

        print(f"\nCurrent status: {lead.status.value}")

        print("\nEnter status:")
        print("1. contacted")
        print("2. qualified")
        print("3. won")
        print("4. lost")

        status_options = {
            "1": "contacted",
            "2": "qualified",
            "3": "won",
            "4": "lost"
        }

        choice = input("Choose new status: ").strip()
        new_status = status_options.get(choice)

        if new_status is None:
            print("Invalid status.")
            return

        updated_lead = self._service.change_status(
            lead.id,
            new_status
        )

        print(f"\nStatus updated to: {updated_lead.status.value}")

    def delete_lead(self):
        contact = input("\nEnter lead email or phone number: ").strip()

        lead = self._service.find_by_contact(contact)

        confirmation = input(
            f"Are you sure you want to delete {lead.full_name}? (yes/no): "
        ).strip().lower()

        if confirmation != "yes":
            print("Deletion cancelled.")
            return

        deleted_lead = self._service.delete_lead(lead.id)

        print(f"\n{deleted_lead.full_name} deleted successfully.")

    @staticmethod
    def display_lead(lead):
        print("\n-----------------------------------")
        print(f"ID: {lead.id}")
        print(f"Name: {lead.full_name}")
        print(f"Email: {lead.email}")
        print(f"Phone: {lead.phone}")
        print(f"Source: {lead.source}")
        print(f"Status: {lead.status.value}")
        print(f"Budget: {lead.budget_min} - {lead.budget_max}")
        print(f"Category: {lead.category}")
        print(f"Tag: {lead.tag}")
        print(f"Lowest price: {lead.lowest_price}")
        print(f"Interested locations: {lead.interested_locations}")
        print(f"Follow-up: {lead.follow_up}")
        print("-----------------------------------")

