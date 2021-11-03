from validation import *
from date import get_today


class InvalidCertificate(Exception):
    def __init__(self):
        self.list = []


class RegistrationCertificate:
    today = get_today()
    this_year = get_today().year
    list_of_cars = ["Audi", "Mercedes", "Tesla"]

    @staticmethod
    def fields():
        return ["id", "registration_number", "date_of_registration",
                "VIN_code", "car", "year_of_manufacture"]

    def __init__(self, id, registration_number, date_of_registration, VIN_code, car, year_of_manufacture):
        validators = {
            "id": validate_number,
            "registration_number": validate_pattern,
            "date_of_registration": validate_date,
            "VIN_code": validate_pattern,
            "car": validate_between,
            "year_of_manufacture": validate_number
        }
        parameters = {
            "id": (id, ),
            "registration_number": (registration_number, "xxyyyyxx"),
            "date_of_registration": (date_of_registration, ),
            "VIN_code": (VIN_code, "zzzzzzzzzzzzzzzzz"),
            "car": (car, self.list_of_cars),
            "year_of_manufacture": (year_of_manufacture, 1950, self.this_year)
        }
        error_messages = {
            "id": "Invalid id ",
            "registration_number": "Invalid registration number, must be in format AA0000AA",
            "date_of_registration": "Invalid date of registration, must be in format dd/mm/yyyy ",
            "VIN_code": "Invalid VIN-code, must be in format 17 numbers + letters",
            "car": f"Invalid car model, must be between these: {', '.join(self.list_of_cars)} ",
            "year_of_manufacture": f"Invalid year_of_manufacture, must be between 1950 and {self.this_year} ",
            
            "bad_year": "Your year of manufacture is later than date of registration",
            "bad_date": "Your date of registration can't be in the future"
        }
        error = InvalidCertificate()
        for field, validator in validators.items():
            try:
                setattr(self, field, validator(*parameters[field]))
            except (TypeError, ValueError):
                error.list.append(error_messages[field])
        if len(error.list) != 0:
            raise error
        pairs_of_dates = [(self.year_of_manufacture, self.date_of_registration, "bad_year"),
                          (self.date_of_registration, get_today(), "bad_date")]
        for tup in pairs_of_dates:
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

    def __str__(self):
        res = "***\n"
        for field in self.fields():
            res += f"{field.replace('_', ' ')}: {getattr(self, field)}\n"
        res += "---\n"
        return res
