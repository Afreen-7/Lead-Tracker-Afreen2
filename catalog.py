import json
class PropertyCatalog:

    def __init__(self, file_path):
        self._file_path = file_path

        with open(self._file_path, "r", encoding="utf-8") as file:
            self._data = json.load(file)

    def get_locations(self):
        off_plan = self._data["off_plan_projects"]
        ready = self._data["ready_projects"]

        locations = []
        seen = set()

        for project in off_plan + ready:
            location = (
                project["location"]["area"],
                project["location"]["community"]
        )

            if location not in seen:
                seen.add(location)
                locations.append(location)

        return locations

    def _map_category(self, category):
        categories = {
            "studio": "studio",
            "1 bed": "1_bed",
            "2 bed": "2_beds",
            "3 bed": "3_beds"
        }

        return categories.get(category)

    def get_lowest_price(self, category, locations):
        category_key = self._map_category(category)

        if category_key is None:
            return None

        prices = []

        off_plan = self._data["off_plan_projects"]
        ready = self._data["ready_projects"]

        for project in off_plan + ready:
            location = (
                    project["location"]["area"],
                    project["location"]["community"]
)
            
            if location in locations:
                price = project["prices_by_category"].get(category_key)

                if price is not None:
                    prices.append(price)

        if prices:
            return min(prices)

        return None
