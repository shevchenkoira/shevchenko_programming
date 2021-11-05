from journey import Journey, InvalidJourney
from json import load, dump
from validation import *
import menu


class VaccinationPointNotFound(Exception):
    pass


class VaccinationPointCollection:
    def __init__(self, file_name: str):
        self.container = []
        self.file_name = file_name
        self.file_name_for_errors = file_name.replace(".json", "_error") + ".json"
        self._read()

    def __iter__(self):
        return iter(self.container)

    def __len__(self):
        return len(self.container)

    def _find_index(self, id_):
        for index, elem in enumerate(self.container):
            if elem.id == id_:
                return index
        raise VaccinationPointNotFound

    def _read(self):
        with open(self.file_name, "rt") as f:
            lst = load(f)
        broken_objects = []
        error = InvalidJourney()
        for obj in lst:
            try:
                list_of_person = self.search(obj["name"])
                sum = 0
                for i in list_of_person:
                    sum += i.get_budget()
                if sum < 500:
                    self.container.append(Journey(**obj))
                else:
                    error = InvalidJourney()
                    error.list.append("You can`t spend more than 500")
                    raise error
            except InvalidJourney as error:
                obj["errors"] = error.list
                broken_objects.append(obj)
        if len(broken_objects) != 0:
            with open(self.file_name_for_errors, "wt") as f:
                dump(broken_objects, f, indent=2, default=str)

    def _update_file(self):
        res = []
        for elem in self.container:
            res.append(elem.make_dict())
        with open(self.file_name, "wt") as f:
            dump(res, f, indent=2, default=str)

    def check_id(self, id_):
        for index, elem in enumerate(self.container):
            if elem.id == id_:
                return True
        else:
            return False

    def add(self, trip: Journey):
        error = InvalidJourney()
        broken_objects = []
        if not isinstance(trip, Journey):
            raise ValueError
        else:
            try:
                list_of_person = self.search(trip.get_name())
                sum = 0
                for i in list_of_person:
                    sum += i.get_budget()
                if sum > 500:
                    self.container.append(trip)
                else:
                    error.list.append("You can`t spend more than 500")
                    raise error
            except InvalidJourney as error:
                a = trip.make_dict()
                a["errors"] = error.list
                broken_objects.append(a)
                if len(broken_objects) != 0:
                    with open(self.file_name_for_errors, "wt") as f:
                        dump(broken_objects, f, indent=2, default=str)

    def search(self, text: str):
        res = []
        for elem in self.container:
            for field in elem.fields():
                if text.lower() in str(getattr(elem, field)).lower():
                    res.append(elem)
                    break
        return res

    def popular_city(self, file_name: str):
        dict_of_city = {}
        for field_val in Journey.list_of_city:
            dict_of_city[field_val] = len(self.search(field_val))
        item_max_value = max(dict_of_city.items(), key=lambda x: x[1])
        list_of_keys = list()
        for key, value in dict_of_city.items():
            if value == item_max_value[1]:
                list_of_keys.append(key)
        final_tup = [item_max_value[1], list_of_keys]
        with open(file_name, "wt") as f:
            dump(final_tup, f, indent=2, default=str)

    def expensive_city(self, file_name: str):
        dict_of_city = {}
        sum = 0
        for field_val in Journey.list_of_city:
            sum = 0
            a = self.search(field_val)
            for i in a:
                sum += i.get_budget()
            dict_of_city[field_val] = sum

        dict_of_city = sorted(dict_of_city.items(), key=lambda x: x[1], reverse=True)

        with open(file_name, "wt") as f:
            dump(dict_of_city, f, indent=2, default=str)
