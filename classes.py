from collections import UserDict
from datetime import datetime
from itertools import islice
import csv

class Field:
    def __init__(self, value: str):
        self._value = None
        self.value = value

    def __str__(self) -> str:
        return f"{self._value}"

    def __repr__(self) -> str:
         return f"{self._value}"

class Birthday(Field):
  
    @property
    def value(self) -> datetime.date:
        return self._value

    @value.setter
    def value(self, value):

        if value is None:
            return f"You don't add birthday"

        try: 
            self._value = datetime.strptime(value, "%d-%m-%Y").date()
        except ValueError:
           print(f"Entered {value} is not correct date. Please use format: 'dd-mm-yyyy'")

    def __repr__(self) -> str:
        return datetime.strftime(self._value, "%d-%m-%Y")
            
class Name(Field):
   @property
   def value(self):
       return self._value
   
   @value.setter
   def value(self, value):
       self._value = value


class Phone(Field):

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        phone_number = (value.strip()
                        .removeprefix("+")
                        .replace("-", "")
                        .replace(" ", ""))
      
        if not (phone_number.isdigit() 
                and phone_number.startswith("380") 
                and len(phone_number) == 12):
            raise ValueError
        self._value = phone_number


class Record:
    def __init__(self, name: Name, phones: list[Phone] = [], birthday: Birthday = None):
        self.name = name
        self.phones = phones
        self.birthday = birthday


    def add_phone_field(self, phone_number: Phone):
        self.phones.append(phone_number)
   
        
    def delete_phone_field(self, phone_number: Phone):
        for i in self.phones:
            if i.value == phone_number.value:
                self.phones.remove(i)
                return f'Phone {i.value} delete successful.'
            return f'Phone {phone_number.value} not found'


    def change_phone_field(self, old_number: Phone, new_number: Phone):
        for i, p in enumerate(self.phones):
            if p.value == old_number.value:
                self.phones[i] = new_number
                return f"Phone {old_number.value} changed on {new_number.value}"
        return f"Contact does not contain such phone number: {old_number}"


    def add_birthday_field(self, birthday: Birthday):
        self.birthday = birthday


    def days_to_birthday(self):
        current_date = datetime.now()

        if self.birthday is not None:
           birthday: datetime.date = self.birthday.value.date()
           
           next_birthday = datetime(
               year=current_date.year, 
               month=birthday.month, 
               day=birthday.day
               ).date()

           if next_birthday < current_date:
               next_birthday = datetime(
                   year=next_birthday.year + 1,
                   month=next_birthday.month,
                   day=next_birthday.day
                   )
               return (next_birthday - current_date).days
           return None
        
    def __str__(self) -> str:
        return f"Name {self.name} phones: {';'.join([str(p) for p in self.phones])} {str(self.birthday) if self.birthday else ''}"
       
class AddressBook(UserDict):
    index = 0 # add for hw 11
    filename = "contacts_book.csv"

    def add_record(self, rec: Record):
        self.data[rec.name.value] = rec
    
    def show_all(self):
        return '\n'.join([f'{r.name.value} : {",".join([str(p) for p in r.phones])}' for r in self.data.values()])

    def iteration(self, step=5):
        while AddressBook.index < len(self):
            yield list(islice(self.items(), AddressBook.index, AddressBook.index+step))
            if AddressBook.IndentationError > len(self):
                raise StopIteration()
            AddressBook.index += step

    def open_file(self):
        with open(self.filename, "r") as file:
            reader = csv.DictReader(file, delimiter=',')
            for row in reader:
                self.add_record(Record(Name(row['name']),
                                       [Phone(p) for p in row['phones'].split(';')],
                                       Birthday(row['birthday']) if row['birthday'] != 'None' else None))

    def save_to_file(self):
        with open(self.filename, 'w', newline='') as file:
            header_names = ['name', 'phones', 'birthday']
            writer = csv.DictWriter(file, fieldnames=header_names, delimiter=',')
            writer.writeheader()
            for rec in self.data.values():
                writer.writerow({'name': str(rec.name), 
                                 'phones': ';'.join([str(p) for p in rec.phones]), 
                                 'birthday': str(rec.birthday)})

    def search(self, ask_me):
        result = ""
        if len(ask_me) <3: 
            result = "The request must consist of 3 or more characters"

            for k, v in self.data.items():
                if (ask_me in k) or (ask_me in v['phone']):
                    result += (f" Found: {k} :\t\t{v}\n")
                for i in v['phones']:
                    if ask_me in i:
                        result += (f" Found: {k} :\t\t{v}\n")
            if result:
                print(result)
            else:
                print("Nothing found")
