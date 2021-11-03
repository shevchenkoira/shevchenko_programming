import certificate
import collection
import date
import memento
from collection import *
from date import *
import unittest


def valid1():
    value_to_ret = "***\n\
id: 222\n\
registration number: BC7777CD\n\
date of registration: 11/11/2011\n\
VIN code: 1111222211112222q\n\
car: Audi\n\
year of manufacture: 2007\n\
---\n"
    return value_to_ret


class TestMyClass(unittest.TestCase):
    def test_validators(self):
        cert_col = RegistrationCertificate(222, "BC7777CD", "11/11/2011", "1111222211112222q", "Audi", 2007)
        cert_col_dict = cert_col.make_dict()
        cert_col_dict["date_of_registration"] = str(cert_col_dict["date_of_registration"])

        self.assertEqual(str(cert_col), valid1())
        self.assertEqual(cert_col_dict, {"id": 222, "registration_number": "BC7777CD", "date_of_registration": "11/11/2011", "VIN_code": "1111222211112222q", "car": "Audi", "year_of_manufacture": 2007})

    def test_validators_invalid(self):
        cur_year = date.today().year
        list_of_cars = RegistrationCertificate.list_of_cars
        with self.assertRaises(certificate.InvalidCertificate) as context:
            RegistrationCertificate("222s", "qq7777888", "11/11/2011", "1111222211112222q8798", "Bentley", 2023)
        self.assertTrue("Invalid VIN-code, must be in format 17 numbers + letters" in context.exception.list)
        self.assertTrue("Invalid registration number, must be in format AA0000AA" in context.exception.list)
        self.assertTrue(f"Invalid year_of_manufacture, must be between 1950 and {cur_year} " in context.exception.list)
        self.assertTrue(f"Invalid car model, must be between these: {', '.join(list_of_cars)} " in context.exception.list)
        self.assertTrue("Invalid id " in context.exception.list)

        with self.assertRaises(certificate.InvalidCertificate) as context_second:
            RegistrationCertificate(222, "BC7777CD", "11/11/2022", "1111222211112222q", "Audi", 2021)
        self.assertTrue("Your date of registration can't be in the future" in context_second.exception.list)

        with self.assertRaises(certificate.InvalidCertificate) as context_second:
            RegistrationCertificate(222, "BC7777CD", "11/11/2019", "1111222211112222q", "Audi", 2021)
        self.assertTrue("Your year of manufacture is later than date of registration" in context_second.exception.list)

    def test_date(self):
        cur_date = date.today().strftime('%d/%m/%Y')
        self.assertEqual(str(get_today()), str(cur_date))
        self.assertEqual(str(Date(10, 2, 2021)), "10/02/2021")
        self.assertRaises(ValueError, Date.check_date, 10, 13, 2021)
        self.assertRaises(ValueError, Date.check_date, 32, 10, 2021)
        self.assertRaises(ValueError, Date.check_date, 10, 10, 2022)
        self.assertTrue(Date(10, 7, 2020) < Date(2, 4, 2021))

    def test_collection(self):
        cert_col = CertificateCollection("list_of_certificates.json")
        caretaker = memento.Caretaker(cert_col.container)
        self.assertRaises(IndexError, caretaker.redo)
        caretaker.memorize()
        my_cert = RegistrationCertificate(25, "TT6969TT", "31/01/2021", "oleksiidatisuk228", "Mercedes", 1997)
        a = []
        for certificates in cert_col:
            a.append(certificates.id)

        self.assertEqual(a, [23, 1234])
        cert_col.add(my_cert)
        caretaker.memorize()
        a = []
        for certificates in cert_col:
            a.append(certificates.id)
        self.assertEqual(a, [23, 1234, 25])
        cert_col.sort(lambda x: x.id, False)
        a = []
        for certificates in cert_col:
            a.append(certificates.id)
        self.assertEqual(a, [23, 25, 1234])
        caretaker.undo()
        a = []
        for certificates in cert_col:
            a.append(certificates.id)
        self.assertEqual(a, [23, 1234])
        caretaker.redo()
        cert_col.remove(25)
        a = []
        for certificates in cert_col:
            a.append(certificates.id)
        self.assertEqual(a, [23, 1234])

        self.assertEqual(len(cert_col), 2)
        self.assertRaises(collection.CertificateNotFound, cert_col._find_index, 22222)
        self.assertFalse(cert_col.check_id(2222))
        self.assertEqual(cert_col.search("BC7777CD")[0].registration_number, "BC7777CD")
        self.assertEqual(cert_col.search("BC7777SD"), [])
        self.assertRaises(ValueError, cert_col.extend, [1, 23])

        cert_col.edit(23, "car", "Audi")

        self.assertEqual(cert_col.search("Audi")[0].car, "Audi")
        cert_col.edit(23, "car", "Mercedes")
