from collections import UserDict
import datetime
from itertools import islice

class Field:
    def __init__(self, value: str):
        self.value = value

    # add for hw 11
    def __str__(self) -> str:
        return f"{self.value}"
    # add for hw 11
    def __repr__(self) -> str:
         return f"{self.value}"

# add for hw 11
class Birthday(Field):
    # add for hw 11
    @property
    def born(self):
        return f"This class Birthday {self.__born}"

    @born.setter
    def born(self, value: str):
        if not value:
            raise ValueError("Birthday is not attaching")
        self.__born = value
            

class Name(Field):
   pass


class Phone(Field):
    # pass
    # add for hw 11
    @property
    def phone_value(self):
        return f"Bad phone number {self.__phone_value}"
    
    @phone_value.setter
    def phone_value(self, value: str):
        if value:
            raise ValueError("Number is not correct")
        self.__phone_value = value
    

class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = []
        self.birthday = birthday # add for hw 11
    
        if phone:
            self.phones.append(phone)

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

# add for hw 11
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

       
class AddressBook(UserDict):
    index = 0 # add for hw 11

    def add_record(self, rec: Record):
        self.data[rec.name.value] = rec
    
    def show_all(self):
        return '\n'.join([f'{r.name.value} : {",".join([str(p) for p in r.phones])}' for r in self.data.values()])
   
    # add for hw 11
    def iteration(self, step=5):
        while AddressBook.index < len(self):
            yield list(islice(self.items(), AddressBook.index, AddressBook.index+step))
            if AddressBook.IndentationError > len(self):
                raise StopIteration()
            AddressBook.index += step