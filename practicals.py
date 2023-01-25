hutton = "Henry"
print(type(hutton))

for x in range(100):
    print(x)

def superduper(x,y):
    print(x+y)

print(superduper(1,2))

print("This print statement was created in Python")

age = 52
print(f'my age is {age}')

print("This is a comment")

print("This print statement was created in Python")

my_string = "Hello world"
my_length = len(my_string)
print(my_length)

my_number=5


def void_function():
    print("This is a void function")

void_result=void_function()
print(void_result)

def in_range(lower_bound,upper_bound,number):
    if number >= lower_bound and number <= upper_bound:
        print (f"{number} is between {lower_bound} and {upper_bound}.")
        return True
    else:
        print(f"{number} is NOT between {lower_bound} and {upper_bound}.")
        return False
    
in_range(1,66,77)



def print_clothing_attributes(clothing, attributes_to_print='all'):
    if attributes_to_print != 'all':
        for key in attributes_to_print:
            if key in clothing:
                print(key, ":", clothing[key])
            else:
                print(f"{key} doesn't exist in this clothing.")
    else:
        for key, value in clothing.items():
            print(key, ":", value)

# Example usage
clothing = {'color': 'red', 'material': 'cotton', 'size': 'large'}
print_clothing_attributes(clothing, ['color', 'size'])


def create_profile(name, age, email):
    if not check_name(name) or not check_email(email) or not check_age(age):
        print("nothing entered!")
        return
    # create the profile here
    
def check_name(name):
    special_characters = "!@£$%^&*()"
    for char in special_characters:
        if char in name:
            print("Error: Name cannot contain special characters")
            return False
    return True

def check_email(email):
    if "@" not in email:
        print("Error: Email is invalid")
        return False
    return True

def check_age(age):
    if age <= 12:
        print("Error: User must be older than 12")
        return False
    return True