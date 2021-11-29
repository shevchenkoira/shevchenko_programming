from date import Date
import re


def validate_number(text: str, least=None, largest=None):
    try:
        v = float(text)
        if re.match(r'[+-]?[0-9]+\.[0-9]+', str(text)):
            raise ValueError
        if isinstance(least, int) and least > int(text):
            raise ValueError
        elif isinstance(largest, int) and largest < int(text):
            raise ValueError
    except:
        raise TypeError
    else:
        return float(text)


def validate_name(name):
    if not isinstance(name, str):
        raise TypeError
    else:
        name_cont = name.split(" ")
        if name_cont[0].isalpha() and name_cont[1].isalpha():
            return name
        else:
            raise ValueError


def validate_pattern(text: str, pattern: str):
    letter_patterns = ["x", "z"]
    digit_patterns = ["y", "z"]
    if not isinstance(text, str) or not isinstance(pattern, str):
        raise TypeError
    elif len(text) != len(pattern):
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
        return text


def validate_between(text: str, lst: list):
    if text not in lst:
        raise ValueError
    else:
        return text


def validate_date(date: str):
    if isinstance(date, str):
        validate_pattern(date, "yy/yy/yyyy")
        day, month, year = date.split("/")
        return Date(day, month, year)
    elif isinstance(date, Date):
        return date
    else:
        raise TypeError


def date_to_day(date: Date):
    leap_year = (date.year % 400 == 0) or (date.year % 4 == 0 and date.year % 100 != 0)
    month_list31 = [1, 3, 5, 7, 8, 10, 12]
    month_list30 = [4, 6, 9, 11]
    result = 0
    if leap_year :
        result += date.year * 366
    else:
        result += date.year * 365
    if date.month in month_list31:
        result += date.month * 31
    elif date.month in month_list30:
        result += date.month * 30
    elif date.month == 2 and not leap_year:
        result += date.month * 28
    else:
        result += date.month * 29
    result += date.day
    return result


def compare_date(start: Date, end: Date):
    if isinstance(start, Date) and isinstance(end, Date):
        if date_to_day(end) - date_to_day(start) < 6:
            raise ValueError
    else:
        raise TypeError
