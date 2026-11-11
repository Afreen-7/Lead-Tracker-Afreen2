from enum import Enum
import uuid

from errors import ValidationError


SOURCES = ("website", "bayut", "property finder")
CATEGORIES = ("studio", "1 bed", "2 bed", "3 bed")


class LeadStatus(Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    WON = "won"
    LOST = "lost"

    def next_options(self):
        transitions = {
            LeadStatus.NEW: (LeadStatus.CONTACTED,),

            LeadStatus.CONTACTED: (
                LeadStatus.QUALIFIED,
                LeadStatus.LOST
            ),

            LeadStatus.QUALIFIED: (
                LeadStatus.WON,
                LeadStatus.LOST
            ),

            LeadStatus.WON: (),
            LeadStatus.LOST: ()
        }

        return transitions[self]

    def can_move_to(self, status):
        return status in self.next_options()


class Lead:

    def __init__(
        self,
        first_name,
        last_name,
        phone,
        email,
        source,
        status,
        budget_min,
        budget_max,
        category,
        interested_locations,
        middle_name=None,
        tag=None,
        lowest_price=None,
        follow_up=None,
        lead_id=None
    ):

        if budget_max < budget_min:
            raise ValidationError(
                "Maximum budget cannot be less than minimum budget."
            )

        if source not in SOURCES:
            raise ValidationError("Invalid lead source.")

        if category not in CATEGORIES:
            raise ValidationError("Invalid property category.")

        if isinstance(status, str):
            try:
                status = LeadStatus(status)
            except ValueError:
                raise ValidationError("Invalid lead status.")

        if not isinstance(status, LeadStatus):
            raise ValidationError("Invalid lead status.")

        self._id = str(uuid.uuid4()) if lead_id is None else lead_id
        self._first_name = first_name
        self._middle_name = middle_name
        self._last_name = last_name
        self._phone = phone
        self._email = email
        self._source = source
        self._status = status
        self._budget_min = budget_min
        self._budget_max = budget_max
        self._category = category
        self._interested_locations = tuple(interested_locations)
        self._tag = tag
        self._lowest_price = lowest_price
        self._follow_up = follow_up

    @property
    def id(self):
        return self._id

    @property
    def first_name(self):
        return self._first_name

    @property
    def middle_name(self):
        return self._middle_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def full_name(self):
        return " ".join(
            name for name in (
                self._first_name,
                self._middle_name,
                self._last_name
            ) if name
        )

    @property
    def phone(self):
        return self._phone

    @property
    def email(self):
        return self._email

    @property
    def source(self):
        return self._source

    @property
    def status(self):
        return self._status

    @property
    def budget_min(self):
        return self._budget_min

    @property
    def budget_max(self):
        return self._budget_max

    @property
    def category(self):
        return self._category

    @property
    def interested_locations(self):
        return self._interested_locations

    @property
    def tag(self):
        return self._tag

    @property
    def lowest_price(self):
        return self._lowest_price

    @property
    def follow_up(self):
        return self._follow_up

    def change_status(self, new_status):

        if isinstance(new_status, str):
            try:
                new_status = LeadStatus(new_status)
            except ValueError:
                raise ValidationError("Invalid lead status.")

        if not isinstance(new_status, LeadStatus):
            raise ValidationError("Invalid lead status.")

        if not self._status.can_move_to(new_status):
            raise ValidationError(
                f"Cannot change status from "
                f"{self._status.value} to {new_status.value}."
            )

        self._status = new_status

    def to_dict(self):
        return {
            "id": self._id,
            "first_name": self._first_name,
            "middle_name": self._middle_name,
            "last_name": self._last_name,
            "phone": self._phone,
            "email": self._email,
            "source": self._source,
            "status": self._status.value,
            "budget_min": self._budget_min,
            "budget_max": self._budget_max,
            "category": self._category,
            "interested_locations": list(self._interested_locations),
            "tag": self._tag,
            "lowest_price": self._lowest_price,
            "follow_up": self._follow_up
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            lead_id=data.get("id"),
            first_name=data["first_name"],
            middle_name=data.get("middle_name"),
            last_name=data["last_name"],
            phone=data.get("phone"),
            email=data.get("email"),
            source=data["source"],
            status=data["status"],
            budget_min=data["budget_min"],
            budget_max=data["budget_max"],
            category=data["category"],
            interested_locations=data["interested_locations"],
            tag=data.get("tag"),
            lowest_price=data.get("lowest_price"),
            follow_up=data.get("follow_up")
        )

    def __str__(self):
        return (
            f"Lead: {self.full_name} | "
            f"Phone: {self._phone} | "
            f"Email: {self._email} | "
            f"Status: {self._status.value} | "
            f"Budget: {self._budget_min}-{self._budget_max}"
        )
