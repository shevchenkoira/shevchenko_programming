from certificate import RegistrationCertificate, InvalidCertificate
from json import load, dump


class CertificateNotFound(Exception):
    pass


class CertificateCollection:
    def __init__(self, file_name: str):
        self.container = []
        self.file_name = file_name
        self.file_name_for_errors = file_name.replace(".", "_") + ".json"
        self._read()

    def __iter__(self):
        return iter(self.container)

    def __len__(self):
        return len(self.container)

    def _find_index(self, id_):
        for index, elem in enumerate(self.container):
            if elem.id == id_:
                return index
        raise CertificateNotFound

    def _read(self):
        with open(self.file_name, "rt") as f:
            lst = load(f)
        broken_objects = []
        for obj in lst:
            try:
                self.container.append(RegistrationCertificate(**obj))
            except InvalidCertificate as error:
                obj["errors"] = error.list
                broken_objects.append(obj)
        if len(broken_objects) != 0:
            with open(self.file_name_for_errors, "wt") as f:
                dump(broken_objects, f, indent=2, default=str)

    def _update_file(self):
        res = []
        for elem in self.container:
            res.append(elem.make_dict())
        with open(self.file_name, "wt") as f:
            dump(res, f, indent=2, default=str)

    def check_id(self, id_):
        for index, elem in enumerate(self.container):
            if elem.id == id_:
                return True
        else:
            return False

    def search(self, text: str):
        res = []
        for elem in self.container:
            for field in elem.fields():
                if text.lower() in str(getattr(elem, field)).lower():
                    res.append(elem)
                    break
        return res

    def sort(self, key, reverse=False):
        self.container.sort(key=key, reverse=reverse)
        self._update_file()

    def remove(self, id_):
        index = self._find_index(id_)
        self.container.pop(index)
        self._update_file()

    def add(self, certificate: RegistrationCertificate):
        if not isinstance(certificate, RegistrationCertificate):
            raise ValueError
        else:
            self.container.append(certificate)
            self._update_file()

    def edit(self, id_, field, val):
        index = self._find_index(id_)
        to_edit = self.container[index].make_dict()
        to_edit[field] = val
        new_obj = RegistrationCertificate(**to_edit)
        self.container[index] = new_obj
        self._update_file()
