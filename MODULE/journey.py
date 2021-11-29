from validation import *
from date import get_today


class InvalidJourney(Exception):
    def __init__(self):
        self.list = []


class Journey:
    today = get_today()
    list_of_city = ["Rome", "Paris", "Naples", "Vienna"]

    @staticmethod
    def fields():
        return ["city", "budget", "start_date", "end_date", "name"]

    def __init__(self, city, budget, start_date, end_date, name):
        validators = {
            "city": validate_between,
            "budget": validate_number,
            "start_date": validate_date,
            "end_date": validate_date,
            "name": validate_name
        }
        parameters = {
            "city": (city, self.list_of_city),
            "budget": (budget, 0, 500),
            "start_date": (start_date, ),
            "end_date": (end_date, ),
            "name": (name, )
        }
        error_messages = {
            "city": f"Invalid city, must be between these: {', '.join(self.list_of_city)}  ",
            "budget":"Invalid budget, must be less than 500 and in format xx.xx",
            "start_date": "Invalid start_date, must be in format dd/mm/yyyy ",
            "end_date": "Invalid end_date, must be in format dd/mm/yyyy ",
            "name": "Invalid name, must contains only letters",

            "bad_date": "Your date must be after 01/01/2020",
            "bad_end": "Your need to relax minimum 5 days"
        }
        error = InvalidJourney()
        for field, validator in validators.items():
            try:
                setattr(self, field, validator(*parameters[field]))
            except (TypeError, ValueError):
                error.list.append(error_messages[field])
        if len(error.list) != 0:
            raise error
        tup = (self.get_start_date(), self.get_end_date(), "bad_date")
        try:
            compare_date(*tup[0:2])
        except ValueError:
            error.list.append(error_messages[tup[2]])
        if len(error.list) != 0:
            raise error

    def make_dict(self):
        res = dict()
        for field in self.fields():
            res[field] = getattr(self, field)
        return res

    def get_city(self):
        return getattr(self, "city")

    def get_budget(self):
        return getattr(self, "budget")

    def get_name(self):
        return getattr(self, "name")

    def get_start_date(self):
        return getattr(self, "start_date")

    def get_end_date(self):
        return getattr(self, "end_date")

    def __str__(self):
        res = "***\n"
        for field in self.fields():
            res += f"{field.replace('_', ' ')}: {getattr(self, field)}\n"
        res += "---\n"
        return res
