from collections import UserDict
import os.path
import pickle
import re
from datetime import datetime

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

 # блок кода касающийся заметок###########
@input_error
def add_note(command_line):
    """ Сама структура заметок это обычный текстовый файл, каждая строка
        которого это есть одна заметка
        В качестве идентификатора выступет дата и время создания заметки,
        приведенные к строковому виду - чтобы файл можно было открывать
        обычным текстовым редактором. Далее этот идентификатор используется
        для индексации по заметкам (редактирование, удаление, поиск)
    """
    note = ' '.join(command_line)
    current_id = datetime.now()
    crt = current_id.strftime("%d.%m.%Y - %H:%M:%S") # преобразовали в строку дату вемя создания
    with open("note.txt", "a+") as file:
        file.write(crt+" :: "+note+"\n")  # первые 21 символ - строка
    return "note added"

@input_error
def find_note(command_line):
    """ Поиск задается по трем переменным
        ключевое слово - без этого слова заметка не интересует
        дата старта - ранее этой даты заметки не интересуют
        дата конца - позже этой даты заметки не интересуют

        сейчас ограничиваем поиск датами, но не временем. Исключительно для удобства пользователя
        после вывода массива заметок он найдет интересующую, скопирует ее полный идентификатор и перейдет к ней
        непосредственно, если нужно
    """
     # разбираем команду в формат (keyword:str, start:'start date' = '', end:'end_date' = ''):
    if len(command_line) >= 3:
        keyword = command_line[0].lower()
        start = command_line[1]
        end = command_line[2]
    elif len(command_line) == 2:
        keyword = command_line[0]
        start = command_line[1]
        end = ''
    elif len(command_line) == 1:
        keyword = command_line[0]
        start = ''
        end = ''
    else:
        keyword = ''
        start = ''
        end = ''

    try:
        start_date = datetime.strptime(start, "%d.%m.%Y")
    except:
        print("Дата старта поиска задано не в формате dd.mm.YYYY, будет\
 проведен поиск с начала")
        start_date = datetime.strptime("01.01.1970", "%d.%m.%Y")  # начало поиска с даты начала Эпохи

    try:
        end_date = datetime.strptime(end, "%d.%m.%Y")
    except:
        print("Дата конца поиска задано не в формате dd.mm.YYYY, будет\
 проведен поиск до конца")
        end_date = datetime.now()   # конец поиска до текущего момента
        
    if (type(keyword) == str) and (keyword != ''):
        pass
    else:
        print("Ключевое слово для поиска не задано поиск по всем заметкам")

    with open("note.txt", "r+") as file:
        lines = file.readlines()            #список строк из файла заметок
        
    msg = "no one note finded"
    for i in lines:
       date_id = i[:10] # вырезали кусок строки - дата создание заметки
       n_id = datetime.strptime(date_id, "%d.%m.%Y") # конверт в объект, чтобы сравнивать
       if (n_id >= start_date) and (n_id <= end_date):
           if (type(keyword) == str) and (keyword != ''):
               j = i.lower()      # приводим оригинальную строку к нижнеему регистру
               if keyword in j:        # если есть ключ(нижний регистр) в строке (нижний регистр ) выводим оригинальную
                   print(i[:len(i)-1]) #забили последний символ переноса строки - для красивого вывода
                   msg = "note finded"
           else:
               print(i[:len(i)-1]) #выводим все строки - нет ключа
               msg = "note finded"
    return msg

@input_error
def change_note(command_line):
    """Для изменения заметки нужно дать аргументом ее полный идентификатор со временем,
       его удобно скопировать после общего поиска
       а также данные которые должны быть записаны в эту заметку с этим же идентификатором
   
    """
    # разбираем команду в формат (dt_id:"%d.%m.%Y - %H:%M:%S" = '', data:str = '')
    if len(command_line) >= 4:
        dt_id = command_line[0]+' '+command_line[1]+' '+command_line[2]
        command_line.pop(0)
        command_line.pop(0)
        command_line.pop(0)
        data = ' '.join(command_line)
    elif len(command_line) == 3:
        dt_id = command_line[0]+command_line[1]+command_line[2]
        data = ''
    else:
        dt_id = ''
        data = ''

    msg = "no one note changed"    
    try:
        loc_id = datetime.strptime(dt_id, "%d.%m.%Y - %H:%M:%S") #проверка что идентификатор задан в формате
        try:
            with open("note.txt", "r") as file:
                buffer = file.readlines()
            for i in range(len(buffer)):
                d_id = buffer[i][:21] #полный идентификатор
                n_id = datetime.strptime(d_id, "%d.%m.%Y - %H:%M:%S")
                if n_id == loc_id:  # совпадение текущего ид с заданным
                    if data != '':
                        buffer[i] = d_id+" :: "+data+"\n"  # замена строки, идентификатор остается
                        msg = "note changed"
                        break
                    else:
                        in_q = input("Поле для замены пустое, вы уверены y or n?")
                        if in_q == 'y':
                            buffer[i] = d_id+" :: "+data+"\n"  # замена строки, идентификатор остается
                            msg = "note changed"
                        break
            with open("note.txt", "w") as file: #удаляем содержимое старого файла, пишем заново
                file.writelines(buffer)  # пишем построчно из буфера
        except:
            print("ошибка выделения идентификатора, вероятно в результате ручного\
 редактирования файла")
                        
    except:
        print("Идентификатор задан не в формате dd.mm.YYYY - hh.mm.ss, скопируйте\
 идентификатор из результатов поиска")
    return msg

@input_error
def delete_note(command_line):
    """Для удаления заметки нужно дать аргументом ее полный идентификатор со временем,
       его удобно скопировать после общего поиска - вместе с кавычками
    """
    # разбираем команду в формат (dt_id:"%d.%m.%Y - %H:%M:%S" = '')
    if len(command_line) == 3:
        dt_id = command_line[0]+' '+command_line[1]+' '+command_line[2]
    else:
        dt_id = ''

    msg = "no one note deleted"    
    try:
        loc_id = datetime.strptime(dt_id, "%d.%m.%Y - %H:%M:%S") #проверка что идентификатор задан в формате
        try:
            with open("note.txt", "r") as file:
                buffer = file.readlines()
            for i in range(len(buffer)):
                d_id = buffer[i][:21] #полный идентификатор
                n_id = datetime.strptime(d_id, "%d.%m.%Y - %H:%M:%S")
                if n_id == loc_id:  # совпадение текущего ид с заданным
                    buffer.pop(i)
                    msg = "note deleted"
                    break
            with open("note.txt", "w") as file: #удаляем содержимое старого файла, пишем заново
                file.writelines(buffer)  # пишем построчно из буфера
        except:
            print("ошибка выделения идентификатора, вероятно в результате ручного\
 редактирования файла")
                        
    except:
        print("Идентификатор задан не в формате dd.mm.YYYY - hh.mm.ss, скопируйте\
 идентификатор из результатов поиска")
    return msg

@input_error
def tag_note(command_line):
    pass


@input_error
def help_common(command_line):

    try:
        file = open("help.txt", 'r')
        help_lines = file.readlines()
        for i in help_lines:
            print(i[:len(i)-1]) #забили последний символ переноса строки - для красивого вывода
        file.close()
        msg = "End of help"
    except:
        msg = "Файла help.txt не найдено"
    return msg


def start_note(): #проверка что файл существует или его создание
    
    try:
        file = open("note.txt", 'r')
        print("Файл с заметками note.txt загружен")
    except:
        file = open("note.txt", 'w') #создаем новый
        print("Файл с заметками note.txt создан")
    finally:
        file.close()

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
    "add note": add_note,
    "find note": find_note,
    "change note": change_note,
    "delete note": delete_note,
    "tag note": tag_note,
    "hlp me": help_common
}

ONE_WORD_COMMANDS = ['add', 'close', 'exit', 'save', 'remove']
TWO_WORDS_COMMANDS = ['add address', 'add birthday', 'add email', 'add phone',
                      'delete address', 'delete birthday', 'delete email', 'delete phone',
                      'change email', 'change birthday', 'change address', 'change phone',
                      'coming birthday', 'good bye', "add note", "find note", "change note",
                      "delete note", "tag note", "hlp me"]


def get_handler(command):
    return COMMANDS[command]


def main():

    start_note()
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