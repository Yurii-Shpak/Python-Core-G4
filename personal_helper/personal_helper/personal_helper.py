from collections import UserDict
import os.path
import pickle
import re


class CustomException(Exception):
    def __init__(self, text):
        self.txt = text


class AddressBook(UserDict):

    def get_values_list(self):
        if self.data:
            return self.data.values()
        else:
            raise CustomException('Address book is empty')

    def get_record(self, name):
        if self.data.get(name):
            return self.data.get(name)
        else:
            raise CustomException(
                'Such contacts name doesn\'t exist (Command format: <command> <name> <information>)')

    def remove(self, name):
        if self.data.get(name):
            self.data.pop(name)
        else:
            raise CustomException(
                'Such contacts name doesn\'t exist (Command format: <command> <name> <information>)')

    def load_from_file(self, file_name):
        if os.path.exists(file_name):
            with open(file_name, 'rb') as fh:
                self.data = pickle.load(fh)
                if len(self.data):
                    return f'The contacts book is loaded from the file "{file_name}".'
                else:
                    return 'This is empty contacts book. Add contacts to it.'
        else:
            return 'This is empty contacts book. Add contacts into it.'

    def save_to_file(self, file_name):
        with open(file_name, 'wb') as fh:
            pickle.dump(self.data, fh)
        return f'The contacts book is saved in the file "{file_name}".'


contacts = AddressBook()


class Record:

    def __init__(self, name, address=None, phones_list=None, email=None, birthday=None):
        self.name = name
        self._address = address
        self._phones_list = []
        self._email = email
        self._birthday = birthday

    def append_phone(self, phone):
        if re.search('\(0\d{2}\)\d{3}-\d{2}-\d{2}', phone):
            self._phones_list.append(phone)
        else:
            raise CustomException(
                'Wrong phone number format. Use (0XX)XXX-XX-XX format!')

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = address

    def delete_address(self):
        self._address = None

    @property
    def phones_list(self):
        return self._phones_list

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if re.search('[a-zA-Z][\w.]+@[a-zA-z]+\.[a-zA-Z]{2,}', email):
            self._email = email
        else:
            raise CustomException(
                'Wrong email format. Should be as same as: aaaa@ddd.cc')

    def delete_email(self):
        self._email = None

    @property
    def birthday(self):
        return self._birthday

    @birthday.setter
    def birthday(self, birthday):
        if re.search('\d{2}\.\d{2}.\d{4}', birthday):
            self._birthday = birthday
        else:
            raise CustomException(
                'Wrong date format. Should be as same as: dd.mm.yyyy')

    def delete_birthday(self):
        self._birthday = None


def input_error(func):

    def inner(command_line):

        try:
            result = func(command_line)

        except CustomException as warning_text:
            result = warning_text

        except:
            if func.__name__ == 'save_func':
                result = f'Error while saving.'
            elif func.__name__ == 'remove':
                result = f'Error while removing record.'
            elif func.__name__ == 'delete_address':
                result = f'Error while deleting address.'
            elif func.__name__ == 'delete_birthday':
                result = f'Error while deleting birthday.'
            elif func.__name__ == 'delete_email':
                result = f'Error while deleting email.'
            elif func.__name__ == 'delete_phone':
                result = f'Error while deleting phone.'

        return result

    return inner


@input_error
def exit_func(command_line):

    return 'Good bye!'


@input_error
def save_func(command_line):

    return contacts.save_to_file('contacts.bin')


# если нет имени, будет ошибка Such contacts name doesn't exist
def prepare_value(command_line):
    if command_line:
        key = command_line.pop(0)
        value = ' '.join(command_line)
        return key, value
    else:
        raise CustomException(
            'With command must to be INFORMATION you want to add (Commands format: <command> <name> <information>)')


@input_error
def add_name(command_line):  # если имя уже существует?
    if command_line:
        name = ' '.join(command_line)
        record = Record(name)
        contacts[name] = record
        return f'Contact with the name "{name}" has been successfully added'
    else:
        raise CustomException(
            'The command must be with a NAME you want to add (Format: <add> <name>)')


@input_error
def add_address(command_line):
    key, address = prepare_value(command_line)
    contacts.get_record(key).address = address
    return f'Contacts address has been successfully added'


@input_error
def add_birthday(command_line):
    key, birthday = prepare_value(command_line)
    contacts.get_record(key).birthday = birthday
    return f'Contacts birthday date has been successfully added'


@input_error
def add_email(command_line):
    key, email = prepare_value(command_line)
    contacts.get_record(key).email = email
    return f'Contacts email has been successfully added'


@input_error
def add_phone(command_line):
    print(command_line)
    key, phone = prepare_value(command_line)
    if not phone in contacts.get_record(key).phones_list:
        contacts.get_record(key).append_phone(phone)
        return f'Contacts phone number has been successfully added'
    else:
        raise CustomException('Such phone number has been already added!!!')

@input_error
def remove(command_line):
    key, _ = prepare_value(command_line)
    if contacts.get_record(key):
        contacts.remove(key)
        return f'Contact {key} has been successfully removed'
    else:
        raise CustomException('Such contact does not exist!!!')

@input_error
def delete_address(command_line):
    key, _ = prepare_value(command_line)
    address = contacts.get_record(key).address
    contacts.get_record(key).delete_address()
    return f'Contacts address {address} for {key} has been successfully deleted'

@input_error
def delete_birthday(command_line):
    key, _ = prepare_value(command_line)
    birthday = contacts.get_record(key).birthday
    contacts.get_record(key).delete_birthday()
    return f'Contacts birthday date {birthday} for {key} has been successfully deleted'

@input_error
def delete_email(command_line):
    key, _ = prepare_value(command_line)
    email = contacts.get_record(key).email
    contacts.get_record(key).delete_email()
    return f'Contacts {email} for {key} has been successfully deleted'

@input_error
def delete_phone(command_line):
    key, phone = prepare_value(command_line)
    if phone in contacts.get_record(key).phones_list:
        ix = contacts.get_record(key).phones_list.index(phone)
        if ix >= 0:
            contacts.get_record(key).phones_list.pop(ix)
        return f'Contacts {phone} has been successfully deleted'
    else:
        raise CustomException('Such contact does not exist!!!')

@input_error
def change_email(command_line):
    key, email = prepare_value(command_line)
    contacts.get_record(key).email = email
    return f'Contacts email {key} has been successfully changed to {email}'

@input_error
def change_birthday(command_line):
    key, birthday = prepare_value(command_line)
    contacts.get_record(key).birthday = birthday
    return f'Contacts birthday {key} has been successfully changed to {birthday}'

@input_error
def change_address(command_line):
    key, address = prepare_value(command_line)
    contacts.get_record(key).address = address
    return f'Contacts address {key} has been successfully changed to {address}'

@input_error
def change_phone(command_line):
    key, phone = prepare_value(command_line)
    phones = phone.split()
    if len(phones) != 2:
        raise CustomException(
            '''The command must be with a NAME and 2 phones you want to change 
            (Format: <change> <name> <old phone> <new phone>)''')
    if phones[0] in contacts.get_record(key).phones_list:
        ix = contacts.get_record(key).phones_list.index(phones[0])
        if ix >= 0:
            contacts.get_record(key).phones_list[ix] = phones[1]
        return f'Contacts phone {key} has been successfully changed to {phones[1]}'
    else:
        raise CustomException('Such contact does not exist!!!')

@input_error
def coming_birthday(command_line=7):  # in progress
    list_bithday = [i for i in contacts.get_values_list()]
    return contacts.get_values_list()

@input_error
def show_all(command_line):
    contact_book = contacts.get_values_list()
    print(contact_book)
    for key in contact_book:

        print(key)  
    return contacts  

@input_error
def find_contact(command_line):
    print(command_line)
    print(contacts)

COMMANDS = {
    'close': exit_func,
    'exit': exit_func,
    'good bye': exit_func,
    'save': save_func,
    'add': add_name,
    'add address': add_address,
    'add birthday': add_birthday,
    'add email': add_email,
    'add phone': add_phone,
    'remove': remove,
    'delete address': delete_address,
    'delete birthday': delete_birthday,
    'delete email': delete_email,
    'delete phone': delete_phone,
    'change email': change_email,
    'change birthday': change_birthday,
    'change address': change_address,
    'change phone': change_phone,
    'coming birthday': coming_birthday,
    'show all': show_all,
    'find': find_contact,
}

ONE_WORD_COMMANDS = ['add', 'close', 'exit', 'save', 'remove', 'find']
TWO_WORDS_COMMANDS = ['add address', 'add birthday', 'add email', 'add phone',
                      'delete address', 'delete birthday', 'delete email', 'delete phone',
                      'change email', 'change birthday', 'change address', 'change phone',
                      'coming birthday', 'good bye', 'show all']


def get_handler(command):
    return COMMANDS[command]


def main():

    print(contacts.load_from_file('contacts.bin'))

    while True:
        command_line = []
        while not command_line:
            command_line = input('>>> ').split()

        right_command = False

        if len(command_line) > 1 and \
           f'{command_line[0].lower()} {command_line[1].lower()}' in TWO_WORDS_COMMANDS:
            command = f'{command_line.pop(0).lower()} {command_line.pop(0).lower()}'
            right_command = True

        if not right_command:
            command = command_line.pop(0).lower()
            right_command = command in ONE_WORD_COMMANDS

        if not right_command:
            print(
                f'The "{command}" command is wrong! The allowable commands are {", ".join(ONE_WORD_COMMANDS + TWO_WORDS_COMMANDS)}.')
            continue

        handler = get_handler(command)
        print(handler(command_line))
        if handler is exit_func:
            print(contacts.save_to_file('contacts.bin'))
            break


if __name__ == '__main__':
    main()
