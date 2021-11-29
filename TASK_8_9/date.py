from datetime import date


def get_today():
    today_date = date.today()
    return Date(today_date.day, today_date.month, today_date.year)


class Date:
    def __init__(self, day, month, year):
        self.day = int(day)
        self.month = int(month)
        self.year = int(year)
        self.check_date(self.year, self.month, self.day)

    def __str__(self):
        date_day = str(self.day) if self.day >= 10 else "0" + str(self.day)
        date_month = str(self.month) if self.month >= 10 else "0" + str(self.month)
        return date_day + "/" + date_month + "/" + str(self.year)

    @staticmethod
    def check_date(year, month, day):
        month_list31 = [1, 3, 5, 7, 8, 10, 12]
        month_list30 = [4, 6, 9, 11]
        leap_year = (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)
        if month in month_list31:
            if not 31 >= day >= 1:
                raise ValueError
        elif month in month_list30:
            if not 30 >= day >= 1:
                raise ValueError
        elif month == 2 and not leap_year:
            if not 28 >= day >= 1:
                raise ValueError
        elif month == 2 and leap_year:
            if not 29 >= day >= 1:
                raise ValueError
        else:
            raise ValueError

    def __lt__(self, other):
        return self.year < other.year or \
            self.year == other.year and self.month < other.month or \
            self.year == other.year and self.month == other.month and self.day < other.day
