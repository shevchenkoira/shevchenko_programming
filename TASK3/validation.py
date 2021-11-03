from date import Date


def validate_number(text: str, least=None, largest=None):
    if isinstance(least, int) and least > int(text):
        raise ValueError
    elif isinstance(largest, int) and largest < int(text):
        raise ValueError
    else:
        return int(text)


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


def compare_date(year, date: Date):
    if isinstance(year, int):
        if date.year < year:
            raise ValueError
    elif isinstance(year, Date):
        if date < year:
            raise ValueError
    else:
        raise TypeError
