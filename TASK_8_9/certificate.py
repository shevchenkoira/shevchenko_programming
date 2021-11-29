from validation import *

from date import get_today
from db_init import *


class InvalidCertificate(Exception):
    def __init__(self):
        self.list = []


class RegistrationCertificate(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    registration_number = db.Column(db.String(8), nullable=False)
    date_of_registration = db.Column(db.String(45), nullable=False)
    VIN_code = db.Column(db.String(17), nullable=False)
    car = db.Column(db.String(45), nullable=False)
    year_of_manufacture = db.Column(db.Integer)

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
            @validator(*parameters[field][1:])
            def my_setter(value):
                setattr(self, field, value)

            try:
                my_setter(parameters[field][0])
            except (TypeError, ValueError):
                error.list.append(error_messages[field])
        if len(error.list) != 0:
            raise error
        pairs_of_dates = [(self.year_of_manufacture, self.date_of_registration, "bad_year"),
                          (self.date_of_registration, get_today(), "bad_date")]
        for tup in pairs_of_dates:
            @compare_date(*tup[0:2])
            def empty_checker():
                pass
            try:
                empty_checker()
            except ValueError:
                error.list.append(error_messages[tup[2]])
        if len(error.list) != 0:
            raise error

    def make_dict(self):
        res = dict()
        for field in self.fields():
            res[field] = getattr(self, field)
        return res

    def __repr__(self):
        res = "***\n"
        for field in self.fields():
            res += f"{field.replace('_', ' ')}: {getattr(self, field)}\n"
        res += "---\n"
        return res


class InvalidUser(Exception):
    def __init__(self):
        self.list = []


class User(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    email = db.Column(db.String(45))
    password = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=0)

    @staticmethod
    def fields():
        return ["id", "name", "last_name", "email", "password", "is_admin"]

    def __init__(self, id, name, last_name, email, password, is_admin=False):
        parameters = {
            "id": (id,),
            "name": (name, ),
            "last_name": (last_name,),
            "email": (email,),
            "password": (password, ),
            "is_admin": (is_admin,)
        }
        validators = {
            "id": validate_number,
            "name": validate_text,
            "last_name": validate_text,
            "email": validate_email,
            "password": validate_password,
        }
        error_messages = {
            "id": "Invalid id",
            "name": "Name is not valid (must consist of not number symbols)",
            "last_name": "Last mame is not valid (must consist of not number symbols)",
            "email": "Wrong email format",
            "password": "Invalid password (less than 4 symbols)",
        }

        error = InvalidUser()
        for field, validator in validators.items():
            @validator(*parameters[field][1:])
            def my_setter(value):
                setattr(self, field, value)
            try:
                my_setter(parameters[field][0])
            except (TypeError, ValueError):
                error.list.append(error_messages[field])
        if len(error.list) != 0:
            raise error

    def make_dict(self):
        res = dict()
        for field in self.fields():
            res[field] = getattr(self, field)
        return res


class InvalidOrder(Exception):
    def __init__(self):
        self.list = []


class CarOrder(db.Model):
    item_id = db.Column(db.Integer, unique=True, primary_key=True)
    car = db.Column(db.String(45))
    amount = db.Column(db.Integer)

    @staticmethod
    def fields():
        return ["item_id", "car", "amount"]

    def __init__(self, item_id, car, amount):

        self.list_of_cars = ["Audi", "Tesla", "Mercedes", "BMW"]

        parameters = {
            "item_id": (item_id,),
            "car": (car, self.list_of_cars),
            "amount": (amount,),
        }
        validators = {
            "item_id": validate_number,
            "car": validate_between,
            "amount": validate_number,
        }
        error_messages = {
            "item_id": "Invalid id",
            "car": "Invalid car",
            "amount": "Wrong amount"
        }

        error = InvalidOrder()
        for field, validator in validators.items():
            @validator(*parameters[field][1:])
            def my_setter(value):
                setattr(self, field, value)
            try:
                my_setter(parameters[field][0])
            except (TypeError, ValueError):
                error.list.append(error_messages[field])
        if len(error.list) != 0:
            raise error

    def make_dict(self):
        res = dict()
        for field in self.fields():
            res[field] = getattr(self, field)
        return res
