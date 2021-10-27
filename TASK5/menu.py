from certificate import RegistrationCertificate, InvalidCertificate
from collection import CertificateCollection
from memento import Caretaker


class Menu:
    msg = {
        "choices": "Available commands: \n 0 - finish work \n 1 - print list \n 2 - search by string"
                   " \n 3 - sort by field \n 4 - remove by id \n 5 - add new registration certificate"
                   " \n 6 - edit by id \n 7 - undo \n 8 - redo",
        "field": " a - id \n b - registration number \n c - date of registration \n d - VIN-code \n e - car \n"
                 " f - year_of_manufacture",
        "bad_choice": "There is no such command, please, try again",
        "value": "Enter value: ",
        "id": "Enter id: ",
        "registration_number": "Enter registration number (AA0000AA): ",
        "date_of_registration": "Enter date of registration (in format dd/mm/yyyy): ",
        "VIN_code": "Enter VIN-code (17 numbers + letters): ",
        "car": "Enter car model (Audi / Mercedes / Tesla): ",
        "year_of_manufacture": "Enter year_of_manufacture: ",
        "sort": "Container was sorted by given parameter. Enter 1 to print container.",
        "add": "Certificate was added. Enter 1 to print container",
        "delete": "Certificate was deleted. Enter 1 to print container",
        "edit": "Certificate was edited. Enter 1 to print container",
        "undo": "Last action successfully undone",
        "redo": "Last action successfully redone",
        "no_undo": "Nothing to undo",
        "no_redo": "Nothing to redo",
        "no_id": "There isn`t such id in this file",
        "name_file": "Input name of your file: ",
        "file_not_exist": "File not exists, try again"
    }
    writeable_fields = {
        "a": "id",
        "b": "registration_number",
        "c": "date_of_registration",
        "d": "VIN_code",
        "e": "car",
        "f": "year_of_manufacture"
    }

    def __init__(self, file_name):
        try:
            self.collection = CertificateCollection(file_name)
        except FileNotFoundError:
            print(self.msg["file_not_exist"])
        else:
            self.caretaker = Caretaker(self.collection.container)
            self.caretaker.memorize()
            self.run_menu()

    def command1(self):
        for certificate in self.collection:
            print(certificate, end="")

    def command2(self):
        value = input(self.msg["value"])
        output = self.collection.search(value)
        for certificate in output:
            print(certificate, end="")

    def command3(self):
        print(self.msg["field"])
        field = input()
        if field.lower() not in self.writeable_fields.keys():
            print(self.msg["bad_choice"])
            return
        else:
            self.collection.sort(key=lambda x: getattr(x, self.writeable_fields[field]))
            self.caretaker.memorize()
            print(self.msg["sort"])

    def command4(self):
        try:
            id_ = int(input(self.msg["id"]))
            if not self.collection.check_id(id_):
                raise ValueError
        except ValueError:
            print(self.msg["no_id"])
            return
        else:
            self.collection.remove(id_)
            self.caretaker.memorize()
            print(self.msg["delete"])

    def command5(self):
        obj = dict()
        for field in RegistrationCertificate.fields():
            obj[field] = input(self.msg[field])
        try:
            certificate = RegistrationCertificate(**obj)
        except InvalidCertificate as invalid:
            print(*invalid.list, sep="\n")
            return
        else:
            self.collection.add(certificate)
            self.caretaker.memorize()
            print(self.msg["add"])

    def command6(self):
        try:
            print(self.msg["id"])
            id_ = int(input())
            if not self.collection.check_id(id_):
                raise ValueError
        except ValueError:
            print(self.msg["no_id"])
            return
        else:
            print(self.msg["field"])
            field = input()
            if field.lower() not in self.writeable_fields.keys():
                print(self.msg["bad_choice"])
                return
            try:
                value = input(self.msg[self.writeable_fields[field]])
                self.collection.edit(id_, self.writeable_fields[field], value)
            except InvalidCertificate as invalid:
                print(*invalid.list, sep="\n")
                return
            else:
                self.caretaker.memorize()
                print(self.msg["edit"])

    def command7(self):
        try:
            self.caretaker.undo()
        except IndexError:
            print(self.msg["no_undo"])
        else:
            print(self.msg["undo"])

    def command8(self):
        try:
            self.caretaker.redo()
        except IndexError:
            print(self.msg["no_redo"])
        else:
            print(self.msg["redo"])

    def run_menu(self):
        choices = {
            "0": exit,
            "1": self.command1,
            "2": self.command2,
            "3": self.command3,
            "4": self.command4,
            "5": self.command5,
            "6": self.command6,
            "7": self.command7,
            "8": self.command8,
        }
        print(self.msg["choices"])
        while True:
            command_input = input("Your choice: ")
            if command_input in choices.keys():
                choices[command_input]()
            else:
                print(self.msg["bad_choice"])
                print(self.msg["choices"])
