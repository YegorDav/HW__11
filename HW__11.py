from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        self.value = value

    def is_valid(self, value):
        # Перевірка формату телефону (10 цифр)
        return (isinstance(value, str) and value.isdigit() and len(value) == 10)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if not self.is_valid(new_value):
            raise ValueError
        self.__value = new_value


class Birthday(Field):
    def __init__(self, value):
        self.value = value

    def is_valid(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
            return True
        except ValueError:
            return False

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if not self.is_valid(new_value):
            raise ValueError
        self.__value = new_value


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        self.phones = [phone for phone in self.phones if phone.value != phone_number]

    def edit_phone(self, old_phone_number, new_phone_number):
        if not (isinstance(new_phone_number, str) and new_phone_number.isdigit() and len(new_phone_number) == 10):
            raise ValueError("Invalid new phone number format")

        found = False
        for phone in self.phones:
            if phone.value == old_phone_number:
                phone.value = new_phone_number
                found = True
                break

        if not found:
            raise ValueError(f"Phone number {old_phone_number} not found")

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self):
        phones_str = '; '.join(str(phone) for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            next_birthday = datetime(today.year, *map(int, self.birthday.value.split('-'))).date()
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, *map(int, self.birthday.value.split('-'))).date()
            days_left = (next_birthday - today).days
            return days_left
        return None

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, chunk_size=5):
        all_records = list(self.data.values())
        for i in range(0, len(all_records), chunk_size):
            yield all_records[i:i + chunk_size]
