from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from errors import LeadNotFoundError

from models import Lead
from repository import LeadRepository


class PostgresLeadRepository(LeadRepository):

    def __init__(self, database):
        self._database = database

    def add(self, lead):

        query = """
            INSERT INTO leads (
                id,
                first_name,
                middle_name,
                last_name,
                phone,
                email,
                source,
                status,
                budget_min,
                budget_max,
                category,
                interested_locations,
                tag,
                lowest_price,
                follow_up
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            )
        """

        with self._database.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        lead.id,
                        lead.first_name,
                        lead.middle_name,
                        lead.last_name,
                        lead.phone,
                        lead.email,
                        lead.source,
                        lead.status.value,
                        lead.budget_min,
                        lead.budget_max,
                        lead.category,
                        Jsonb(lead.interested_locations),
                        lead.tag,
                        lead.lowest_price,
                        Jsonb(lead.follow_up)
                    )
                )

        return lead

    def get_all(self):

        query = "SELECT * FROM leads ORDER BY first_name"

        with self._database.connect() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

        return [Lead.from_dict(row) for row in rows]

    def find_by_email(self, email):

        query = "SELECT * FROM leads WHERE email = %s"

        with self._database.connect() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query, (email,))
                row = cursor.fetchone()

        if row is None:
            return None

        return Lead.from_dict(row)

    def find_by_phone(self, phone):

        query = "SELECT * FROM leads WHERE phone = %s"

        with self._database.connect() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query, (phone,))
                row = cursor.fetchone()

        if row is None:
            return None

        return Lead.from_dict(row)

    def get_by_id(self, lead_id):

        query = "SELECT * FROM leads WHERE id = %s"

        with self._database.connect() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query, (lead_id,))
                row = cursor.fetchone()

        if row is None:
            return None

        row["id"] = str(row["id"])
        return Lead.from_dict(row)

    def update(self, lead):

        query = """
            UPDATE leads
            SET
                first_name = %s,
                middle_name = %s,
                last_name = %s,
                phone = %s,
                email = %s,
                source = %s,
                status = %s,
                budget_min = %s,
                budget_max = %s,
                category = %s,
                interested_locations = %s,
                tag = %s,
                lowest_price = %s,
                follow_up = %s
            WHERE id = %s
        """

        with self._database.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        lead.first_name,
                        lead.middle_name,
                        lead.last_name,
                        lead.phone,
                        lead.email,
                        lead.source,
                        lead.status.value,
                        lead.budget_min,
                        lead.budget_max,
                        lead.category,
                        Jsonb(lead.interested_locations),
                        lead.tag,
                        lead.lowest_price,
                        Jsonb(lead.follow_up),
                        lead.id
                    )
                )

                return cursor.rowcount > 0

    def delete(self, lead_id):

        query = "DELETE FROM leads WHERE id = %s"

        with self._database.connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (lead_id,))

                return cursor.rowcount > 0

    def search(self, keyword):

        query = """
            SELECT * FROM leads
            WHERE
                first_name ILIKE %s
                OR middle_name ILIKE %s
                OR last_name ILIKE %s
                OR email ILIKE %s
                OR phone ILIKE %s
        """

        search_value = f"%{keyword}%"

        with self._database.connect() as connection:
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    query,
                    (
                        search_value,
                        search_value,
                        search_value,
                        search_value,
                        search_value
                    )
                )

                rows = cursor.fetchall()

        return [Lead.from_dict(row) for row in rows]
