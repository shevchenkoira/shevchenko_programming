from journey import Journey, InvalidJourney
from collection import VaccinationPointCollection


class Menu:
    msg = {
        "choices": "Available commands: \n 0 - finish work \n 1 - print list \n 2 - add new journey"
                   " \n 3 - find the busiest city \n 4 - find the most expensive city \n",
        "field": " a - id \n b - point \n c - time \n d - date \n e - name \n",
        "bad_choice": "There is no such command, please, try again",

        "value": "Enter value: ",
        "id": "Enter id: ",
        "point": "Enter point (Forum / Victoria Garden / Arena Lviv / Cinema center Dovzhenka / Ivan Franko Lviv University):  ",
        "time": "Enter time from 10:00 to 18:00 in step by 20 minutes ",
        "date": "Enter date (in format dd/mm/yyyy): ",
        "name": "Enter name: ",

        "add": "Vaccination point request was added. Enter 1 to print container",

        "name_file": "Input name of your file: ",
        "file_not_exist": "File not exists, try again"
    }
    writeable_fields = {
        "a": "id",
        "b": "point",
        "c": "time",
        "d": "date",
        "e": "name"
    }

    def __init__(self, file_name):
        try:
            self.collection = VaccinationPointCollection(file_name)
        except FileNotFoundError:
            print(self.msg["file_not_exist"])
        else:
            self.run_menu()

    def command1(self):
        for certificate in self.collection:
            print(certificate, end="")

    def command2(self):
        obj = dict()
        for field in Journey.fields():
            obj[field] = input(self.msg[field])
        try:
            vaccination_point = Journey(**obj)
        except InvalidJourney as invalid:
            print(*invalid.list, sep="\n")
            return
        else:
            self.collection.add(vaccination_point)

    def command3(self):
        self.collection.popular_city("popular_city.json")

    def command4(self):
        self.collection.expensive_city("list_of_city_price.json")

    def run_menu(self):
        choices = {
            "0": exit,
            "1": self.command1,
            "2": self.command2,
            "3": self.command3,
            "4": self.command4,
        }
        print(self.msg["choices"])
        while True:
            command_input = input("Your choice: ")
            if command_input in choices.keys():
                choices[command_input]()
            else:
                print(self.msg["bad_choice"])
                print(self.msg["choices"])
