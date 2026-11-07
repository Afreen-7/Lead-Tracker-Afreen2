from enum import Enum
import uuid

SOURCES = ("website", "bayut", "property finder")
CATEGORIES = ("studio", "1 bed", "2 bed", "3 bed")

class LeadStatus(Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    WON = "won"
    LOST = "lost"

    def next_options(self):
        pass

    def can_move_to(self, status):
        pass


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
        pass

    @property
    def id(self):
        pass

    @property
    def first_name(self):
        pass

    @property
    def middle_name(self):
        pass

    @property
    def last_name(self):
        pass

    @property
    def full_name(self):
        pass

    @property
    def phone(self):
        pass

    @property
    def email(self):
        pass

    @property
    def source(self):
        pass

    @property
    def status(self):
        pass

    @property
    def budget_min(self):
        pass

    @property
    def budget_max(self):
        pass

    @property
    def category(self):
        pass

    @property
    def interested_locations(self):
        pass

    @property
    def tag(self):
        pass

    @property
    def lowest_price(self):
        pass

    @property
    def follow_up(self):
        pass

    def change_status(self, new_status):
        pass

    def to_dict(self):
        pass

    @classmethod
    def from_dict(cls, data):
        pass

    def __str__(self):
        pass