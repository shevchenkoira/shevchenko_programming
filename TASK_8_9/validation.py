from date import Date
import re


def validate_number(least=None, largest=None):
    def decorate_function(func):
        def function(text: str, *args, **kwargs):
            if isinstance(least, int) and least > int(text):
                raise ValueError
            elif isinstance(largest, int) and largest < int(text):
                raise ValueError
            else:
                return func(int(text), *args, **kwargs)
        return function
    return decorate_function


def validate_pattern(pattern: str):
    def decorate_function(func):
        def function(text: str, *args, **kwargs):
            letter_patterns = ["x", "z"]
            digit_patterns = ["y", "z"]
            if not isinstance(text, str):
                text = str(text)

            if not isinstance(pattern, str):
                raise TypeError

            if len(text) != len(pattern):
                raise ValueError
            else:
                for i, j in zip(text, pattern):
                    if i.isdigit() and j in digit_patterns:
                        continue
                    elif j.isalpha() and j in letter_patterns:
                        continue
                    elif i == j:
                        continue
                    else:
                        raise ValueError
                return func(text, *args, **kwargs)
        return function
    return decorate_function


def validate_between(lst: list):
    def decorate_function(func):
        def function(text: str, *args, **kwargs):
            if text not in lst:
                raise ValueError
            else:
                return func(text, *args, **kwargs)
        return function
    return decorate_function


def validate_date():
    def decorate_function(func):
        @validate_pattern("yy/yy/yyyy")
        def function(date: str, *args, **kwargs):
            if isinstance(date, str):
                day, month, year = date.split("/")
                return func(Date(day, month, year), *args, **kwargs)
            elif isinstance(date, Date):
                return func(date, *args, **kwargs)
            else:
                raise TypeError
        return function
    return decorate_function


def compare_date(year, date: Date):
    def decorate_function(func):
        def function(*args, **kwargs):
            if isinstance(year, int):
                if date.year < year:
                    raise ValueError
                else:
                    return func(*args, **kwargs)
            elif isinstance(year, Date):
                if date < year:
                    raise ValueError
                else:
                    return func(*args, **kwargs)
            else:
                raise TypeError
        return function
    return decorate_function


def validate_email():
    def decorator_func(func):
        def wrapper(value,*args, **kwargs):
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if not re.fullmatch(regex, value):
                raise ValueError
            else:
                return func(value, *args, **kwargs)
        return wrapper
    return decorator_func


def validate_password():
    def decorator_func(func):
        def wrapper(password,*args, **kwargs):
            if not isinstance(password, str):
                raise ValueError
            if len(password) < 4:
                raise ValueError

            return func(password, *args, **kwargs)
        return wrapper
    return decorator_func


def validate_text():
    def decorator_func(func):
        def wrapper(value: str, *args, **kwargs):
            if not value.isalpha():
                raise ValueError
            return func(value, *args, **kwargs)
        return wrapper
    return decorator_func
