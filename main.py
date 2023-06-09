import functools
from classes import AddressBook, Phone, Name, Birthday, Record

# import pickle


CONTACTS_ARRAY = AddressBook()
pages = []


def error_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = False

        try:
            result = func(*args, **kwargs)
        except TypeError:
            print("""You have not entered all data!!!
-----------------------------------------------------------------------------------------------------------------------
for adding new phone number please input:   add name tel.                   (example: add Denys 345-45-45)
for change please input:                    change name old tel. new tel.   (example: change Denys 234-57-89 584-25-12)
for reading please input:                   phone name                      (example: phone Denys)
for delete number:                          delete name tel.                (example: phone Denys 345-45-45)
-----------------------------------------------------------------------------------------------------------------------
""")
        except KeyError:
            print("This user was not found in the contact book!")
        except ValueError:
            print("Invalid value. Try again.")
        except IndexError:
            print("Invalid value. Try again.")
        return result
    return wrapper

def welcome_bot(func):
    def inner(*args, **kwargs):
        greeting = "\nWelcome to Assistant Console Bot\n"
        print("-"*(len(greeting)-2)+greeting+"-"*(len(greeting)-2))
        return func(*args, **kwargs)
    return inner

#add name and number in dict
@error_handler
def attach(name: str, number: str):
    user_name = Name(name)
    phone = Phone(number)

    rec:Record = CONTACTS_ARRAY.get(user_name.value)

    if rec:
        rec.add_phone_field(phone)
        return f"Phone number {phone} added successfully to contact {user_name}"
    
    rec = Record(user_name, [phone])
    CONTACTS_ARRAY.add_record(rec)
    return f'Contact with name {name} and phone {phone} add successful'
   
@error_handler
def attach_birthday(name, birthday):
    user_name = Name(name)
    when_born = Birthday(birthday)

    rec:Record = CONTACTS_ARRAY.get(user_name.value)

    if rec:
       return rec.add_birthday_field(when_born)

   
@error_handler
def delete(name: str, number: str):
    user_name = Name(name)
    phone = Phone(number)
    rec:Record = CONTACTS_ARRAY.get(user_name.value)

    if rec:
        return rec.delete_phone_field(phone)

@error_handler  # change number contact
def change(name: str, old_number:str, new_number: str):

    user_name = Name(name) 
    old = Phone(old_number)
    new = Phone(new_number)
    rec:Record = CONTACTS_ARRAY.get(user_name.value)

    if old_number:
        return rec.change_phone_field(old, new)

# take phone from dict 
@error_handler
def get_phone(name: str):
    return str(CONTACTS_ARRAY[name])

# ask get phone give phone by name
@error_handler
def show_phone(name: str):
    user_name = Name(name)

    look_phone = get_phone(user_name.value)
    if look_phone: 
        return look_phone
    
# read dict with contact
def reader():
    if not CONTACTS_ARRAY:
        return "Your contact list is empty."
    return CONTACTS_ARRAY.show_all()

# say good bye and exit
@error_handler
def say_good_bye():
    return "Bye! Bye!"

def no_command(*args):
    return 'Unknown command. Try again'

@error_handler
def page_pagination(*argv):
    gen = CONTACTS_ARRAY.iteration(*argv)

    for key in gen:
        pages.append(key)
    print(f"page {int(argv[0][0])} of {len(pages)}")

    if pages:
      return "this pagination don't work"
    
@error_handler
def search(user_input):
    input_list = user_input.strip().split(" ")
    param = input_list[0]

    if len(param) > 0:
        return "search", search_handler(param)
    raise ValueError


@error_handler
def search_handler(param):
    search_string = "The following contacts match the search:\n "
    contact_lines = "\n".join(str(record) for record in list(CONTACTS_ARRAY.search(param)))

    if len(contact_lines) > 0:
        return search_string + contact_lines
    return "Your contact doesn't search"
    

COMMAND_ARRAY = {
    "hello": lambda: print("May I help you?"),
    "add": attach,
    "birthday": attach_birthday,
    "change": change,
    "delete": delete,
    "phone": show_phone,
    "show all":reader,
    "page": page_pagination,
    "exit": say_good_bye,
	"bye": say_good_bye,
	"quit": say_good_bye,
	"close": say_good_bye,
	".": say_good_bye,
    "search": search
}


@error_handler
def parser(command):
    for key in COMMAND_ARRAY.keys():
        if command.startswith(key):
            new_line = command[len(key):].title()
            return COMMAND_ARRAY[key], new_line.split()
    return no_command, []
            

@ welcome_bot
def main():
    CONTACTS_ARRAY.open_file()
    while True:
        user_input = input("Please enter your command: ").lower().strip()
        command, data = parser(user_input)
        
        print(command(*data))
        
        if command == say_good_bye:
            CONTACTS_ARRAY.save_to_file()
            break

if __name__ == "__main__":

    main()
 
