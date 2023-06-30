# -*- coding: utf-8 -*-
"""
gen_member_data.py

The script will take arguments in the following format
“python gen_member_data.py -no <no of members> -fname <filename>”
<no of members> is number of random members to be generated in file with <filename>

If no arguments are given, generate by default 1000 members and save them 
in a new file “memberdata.csv”
While generating the memberdata, keep the following checks in mind.
All required attributes need to be randomly generated for each member.
All the generated members attributes should pass the checks stated in the previous slide. 
The file should have the header with attribute keys listed on slide 3. 

The following attributes are generated:
    Membership number
    First name
    Middle name
    Last name
    Date of birth
    Status
    Membership start date
    Membership end date (if status = none)
    Renewal date
    Phone

Created on %(date)s

@author: %('Ben Morris')s
"""

import sys
import datetime
from dateutil.relativedelta import relativedelta
import re
import csv

EARLIEST_START_DATE = datetime.datetime(1981, 1, 1).date()
TODAY = datetime.datetime.now().date()
FILENAME = "memberdata.csv"
NUM_MEMBERS = 100


class Record:
    def __init__(self, n:str, first, last, dob, status, start, renewal, phone:str, middle="", 
                 address="", end="", email="", notes=""):
        self.mem_num = n
        self.first_name = first
        self.middle_name = middle
        self.last_name = last
        self.birthday = dob
        self.address = address
        self.status = status
        self.start_date = start
        self.end_date = end
        self.renewal_date = renewal
        self.phone_num = phone
        self.email = email
        self.notes = notes
        
    def __repr__(self):
        return (f'Student({self.mem_num}, {self.first_name}, {self.middle_name}, {self.last_name}, '
               f'{self.birthday}, {self.address}, {self.status}, {self.start_date}, {self.end_date}, '
               f'{self.renewal_date}, {self.phone_num}, {self.email}, {self.notes})')
    
    def __str__(self):
        return (f'{self.mem_num}, {self.first_name}, {self.middle_name}, {self.last_name}, '
               f'{self.birthday}, {self.address}, {self.status}, {self.start_date}, {self.end_date}, '
               f'{self.renewal_date}, {self.phone_num}, {self.email}, {self.notes}')
    
    def as_dict(self):
        return ({
            'Membership number': self.mem_num,
            'First name': self.first_name,
            'Middle name': self.middle_name,
            'Last name': self.last_name,
            'Date of birth': self.birthday, 
            'Address': self.address, 
            'Status': self.status,
            'Membership start date': self.start_date, 
            'Membership end date': self.end_date, 
            'Renewal date': self.renewal_date,
            'Phone': self.phone_num, 
            'Email': self.email, 
            'Notes': self. notes
            } )

def check_mem_num(number:str, df):
    """
    Checks member number to make sure it is all numeric and 6 digits

    Parameters
    ----------
    number : str
        membership number
    df: DataFrame
        DataFrame to check for duplicate

    Returns
    -------
    bool
        True if the format is correct, False otherwise.
    """
       
    try:
        if type(number) == int:
            number = str(number)
        if len(number) == 6 and number.isdigit():          
            return True
        else:
            return False
    except AttributeError:
        print(f"\nCheck member number: Invalid input: {number}")
        sys.exit(-1)
        

def check_name(name:str):
    """    
    Returns True if name is only english letters with no numbers or special characters.

    Parameters
    ----------
    name: str
        a name

    Returns
    -------
    bool
        True if the name is in the proper format, False otherwise.
    """
    try:        
        if name.isalpha():
            return True
        else:
            print(f"Invalid name: {name}")
            return False
    except AttributeError:
        print(f"\nCheck name: Invalid input: {name}")
        return False


def convert_date(date):
      
    # List of valid months
    valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 
                    'september', 'october', 'november', 'december']

    try:
        # Split date
        split_date = re.split(' ', date)
        month = split_date[0]
        day = split_date[1]
        year = split_date[2]
        
        # Set up for comparison
        month = month.casefold()
             
        # Check if month is a valid month
        if month in valid_months:
            # Add one to the index to get the month number.
            month_num = valid_months.index(month) +  1
        else:
            # If it isn't a valid month, return None.
            print(f"Not a valid month: {month}")
            return None
        
        # Convert to datetime format of YYYY-MM-DD
        conv_date = year + '-' + str(month_num) + '-' + day        
        # Convert to a date object
        conv_date = datetime.datetime.strptime(conv_date, '%Y-%m-%d').date()        
        
        return conv_date
    
    except:
        print(f"\nConvert date: Invalid input: {date}")
        return None

#print(convert_date('June 36 2023'))    


def check_date(date:str):
    """    
    Returns True if date is in proper format and is a real date, False otherwise.
    
    Date must have format <Month DD Year> e.g. June 15 1996 

    Parameters
    ----------
    date : str
        a date

    Returns
    -------
    bool
        True if the date is in the proper format, False otherwise.
    """
    try:
        # Attempts to convert date to datetime format
        conv_date = convert_date(date)
    
        if not conv_date:
            print(f"Invalid date {date}")
            return False
        else:
            return True
    except:
        print(f"\nCheck date: Invalid input: {date}")
        return False

        
def check_dob(dob):
    """
    Returns True if dob is in proper format and is a real date, False otherwise.
    
    Date must have format <Month DD Year> e.g. June 15 1996 

    Parameters
    ----------
    dob : str
        a date

    Returns
    -------
    bool
        True if the date is in the proper format, False otherwise.
    """
    
    try:                    
        # Ensure the dob is at least 18 years ago                     
        if type(dob) == str:
            dob = convert_date(dob)
        
        if dob > TODAY - relativedelta(years=18):
            print(f"Member is not at least 18 years old: {dob}")
            return False
        else:
            return True      
    except:
        print(f"\nCheck dob: Invalid input: {dob}")
        return False

"""Testing
check_dob(datetime.datetime(2005, 6, 8).date())
check_dob(datetime.datetime(2005, 6, 9).date())
"""


def check_address(address:str):
    """
    Returns True if the address is a string with numbers, words. 
    Commas and dashes are allowed. No other special characters. False otherwise.

    Parameters
    ----------
    address: str
        an address

    Returns
    -------
    bool
        True if the address is in the proper format, False otherwise.
    """
    try:
        if address == "":
            return True
        
        m = re.findall("[0-9]+\s[ a-zA-Z0-9,-]+", address)
                
        # Check that findall returned the same string as address
        #if len(address_ok) == 1 and len(address_ok[0] == len(address)):
        if len(m) == 1 and m[0] == address:
            return True
        else:
            print(f"Improper address: {address}")
            return False        
    except:
        print(f"\nCheck_address: Invalid input: {address}")
        return False

"""
# Testing
print(check_address("209 S Williams Avenue"))
print(check_address("600 Erkwood Drive Hendersonville NC 29739"))
print(check_address("209 .S Williams Avenue"))
print(check_address("- , lkasdfasd"))
print(check_address("%$#"))
"""

def check_status(status:str):
    """
    Returns True if datus is in the given in the set {'basic', 'silver', 'gold', 'platinum', 'none'}

    Parameters
    ----------
    status: str
        Member status

    Returns
    -------
    bool
        True if the status is in the proper format, False otherwise.
    """
    # Status has to be one of the given in the set {'basic', 'silver', 'gold', 'platinum', 'none'}
    try:
        valid_status = ['basic', 'silver', 'gold', 'platinum', 'none']
        if status.lower() in valid_status:
            return True
        else:
            print(f"Invalid status: {status}")
            return False
    except:
        print(f"\nCheck_status: Invalid input: {status}")
        return False
            
""" Testing
v = 18
check_status('Basic')
check_status('Silver')
check_status('Gold')
check_status('Platinum')
check_status('None')
check_status('Rock Star')
check_status(v)
"""


def check_start_date(start_date, dob):
    """
    Returns True if the date is in proper format and is a real date, False otherwise.
    Membership start date should be a valid date after Dec 1980 and member should be at 
    least 18 years of age on the date of membership
    
    Date must have format <Month DD Year> e.g. June 15 1996 

    Parameters
    ----------
    start_date : str
        Member start date
        
    dob : str
        Member birthday

    Returns
    -------
    bool
        True if the start date is valid, False otherwise.
    """
    try:
        if type(start_date) == str:
            #start_date = datetime.datetime.strptime(start_date, '%B %d %Y').date()
            start_date = convert_date(start_date)
        if type(dob) == str:
            dob = convert_date(dob)
        
        # Check for start date today at the latest
        if start_date <= TODAY:
            # Check for start date beginning Jan 1 1981
            if start_date >= EARLIEST_START_DATE:            
                # Check that member was at least 18 at the start date
                if dob + relativedelta(years=18) <= start_date:
                    return True
                else:
                    print("Member was not 18 years old at membership start date.")
                    print(f"Birthdate: {dob}  Start date: {start_date}")
                    return False
            else:
                print(f"Start date was not equal to or greater than January 1, 1981: {start_date}")
                return False
        start_date = convert_date_to_format(start_date)
    except:
        print(f"\nCheck start date: Invalid input: {start_date}, {dob}")
        return False

""" Testing
#check_start_date(datetime.datetime(1980, 12, 31).date(), datetime.datetime(1962, 12, 31).date())
#check_start_date(datetime.datetime(1980, 12, 31).date(), datetime.datetime(1963, 12, 31).date())
#check_start_date(datetime.datetime(1981, 1, 1).date(), datetime.datetime(1963, 1, 2).date())
#check_start_date(datetime.datetime(1981, 1, 1).date(), datetime.datetime(1963, 1, 1).date())
#check_start_date(datetime.datetime(1981, 1, 1).date(), datetime.datetime(1962, 12, 31).date())
#check_start_date(datetime.datetime(2023, 6, 8).date(), datetime.datetime(1962, 12, 31).date())
#check_start_date(datetime.datetime(2023, 6, 8).date(), datetime.datetime(2005, 6, 8).date())
#check_start_date(datetime.datetime(2023, 6, 8).date(), datetime.datetime(2005, 6, 9).date())
"""


def check_end_date(end_date, start_date):
    """
    Returns True if the date is in proper format and is a real date, False otherwise.
    End date must be after the start date and today at the latest.
    
    Date must have format <Month DD Year> e.g. June 15 1996 

    Parameters
    ----------
    end_date : str
        Member end date    
    
    start_date : str
        Member start date    

    Returns
    -------
    bool
        True if the end date is valid, False otherwise.
    """
    try:
        
        if end_date == "":
            return True
        
        elif type(end_date) == str:
            end_date = convert_date(end_date)

        if type(start_date) == str:
            start_date = convert_date(start_date)
                
        if start_date < end_date and end_date <= TODAY:
            return True
        else:
            print(f"\nInvalid end date: {end_date}\n"
                  f"start_date: {start_date}\n"
                  f"today's date: {TODAY}")
            
            return False
        
        end_date = convert_date_to_format(end_date)
        
    except:
        print(f"\nCheck end date: Invalid input: {end_date}")
        return False

"""
# Testing
print(check_end_date('June 8 2023'))
print(check_end_date('June 8, 2023'))
print("cswsv:", check_end_date(""))
print(check_end_date(TODAY))
print(check_end_date('June 9 2023'))
"""



def check_renewal_date(renewal_date, start_date):
    """
    Returns True if the date is in proper format and is a real date, False otherwise.
    Renewal date should be a valid date in the future but not more than 5 years in future.
    
    Date must have format <Month DD Year> e.g. June 15 1996 

    Parameters
    ----------
    renewal_date : str
        Member renewal date    
    
    start_date : str
        Member start date    

    Returns
    -------
    bool
        True if the renewal date is valid, False otherwise.
    """
    try:                    
        if type(renewal_date) == str:
            renewal_date = convert_date(renewal_date)

        if type(start_date) == str:           
            start_date = convert_date(start_date)
        
        # Ensure the renewal date is within 5 years and after start date.                    
        if renewal_date > TODAY + relativedelta(years=5) and renewal_date > start_date:
            print(f"Renewal date is more than 5 years from now: {renewal_date}")
            return False
        else:
            return True
        
        renewal_date = convert_date_to_format(renewal_date)
    except:
        print(f"\nCheck renewal date: Invalid input: {renewal_date}")
        return False

""" Testing
check_renewal_date(datetime.datetime(2028, 6, 8).date())
check_renewal_date(datetime.datetime(2028, 6, 9).date())
"""


def check_phone_number(phone_number:str):
    """
    Returns True if the phone number is a 10-digit number, False otherwise.
    
    Parameters
    ----------
    phone_number : str
        Member phone number

    Returns
    -------
    bool
        True if the phone number is valid, False otherwise.
    """
    try:                    
        # Ensure the phone number is a string
        if type(phone_number) == int:
            phone_number = str(phone_number)
        
        # Ensure the phone number is all digits                   
        if phone_number.isdigit():
            # Ensure the length is 10
            if len(phone_number) == 10:
                return True
            else:
                print(f"The phone number is the wrong length: {phone_number}")
                return False
        else:
            print(f"Improper format for phone nummber: {phone_number}")
            return False
    except:
        print(f"\nCheck phone number: Invalid input: {phone_number}")
        return False

""" Testing
check_phone_number('123456789')
check_phone_number('1234567890')
check_phone_number('123-456-7890')
check_phone_number('(123)456-7890')
check_phone_number('123 456 7890')
"""


def check_email(email:str):
    """
    Returns True if the email address is a <string>@<string>.<string>, False otherwise.
    
    Parameters
    ----------
    email : str
        Member email address

    Returns
    -------
    bool
        True if the email address is valid, False otherwise.
    """
    try:
        if email == "":
            return True
        
        m = re.findall('[\w.]+@[\w]+\.\w+', email)

        if(len(m) == 1 and m[0] == email):
            return True
        else:
            print(f"Not a valid email address: {email}")
            return False        
    except:
        print(f"\nCheck email: Invalid input: {email}")
        return False


def check_notes(notes:str):
    """
    No check for notes. Returns True always.

    Parameters
    ----------
    notes : str
        Notes for member account

    Returns
    -------
    bool
        True always.
    """
    return True

""" Testing
check_email('a.b@gmail.com')
check_email('a.b@gmail.com ben')
check_email('ben a.b@gmail.com')
check_email('c_d@gmail.com')
check_email('jhdfjsdf.jhasg@ncsu.edu')
check_email('56_gg@')
check_email('gg_s@ncsu.org')
check_email('gasf_gs.d@rti.com')
check_email('g.56hhg_dg@yahoo.com')
check_email('gstrt_gg@aol')
"""


def check_record(r, df):
    """
    Calls all of the checks for the record

    Parameters
    ----------
    r : Record
        member Record.
        
    df: DataFrame
        for check_mem_num()

    Returns
    -------
    bool
        True if all checks pass, False otherwise.

    """
    
    # Initialize that the record is okay. Check the attributes and set to False if any requirements
    # aren't met
    record_ok = True;
    
    # Check membership number for 6 digit integer
    record_ok = record_ok and check_mem_num(r.mem_num, df)
    
    # Check entire name for only english letters and no numbers or special characters
    record_ok = record_ok and check_name(r.first_name + r.middle_name + r.last_name)
    
    # Check for valid date of birth
    record_ok = record_ok and check_dob(r.birthday)
    
    # Check address for alphanumeric, "," and "-" only
    record_ok = record_ok and check_address(r.address)
    
    # Check status
    record_ok = record_ok and check_status(r.status)
    
    # Check start date. Must be today at the latest and member must have been 18 years old at the
    # start date
    record_ok = record_ok and check_start_date(r.start_date, r.birthday)

    # Check that end date is a valid date.
    record_ok = record_ok and check_end_date(r.end_date, r.start_date)
    
    # Check that renewal date is at most 5 years from today.
    record_ok = record_ok and check_renewal_date(r.renewal_date, r.start_date)
    
    # Check that phone number is 10 digits
    # Check that renewal date is at most 5 years from today.
    record_ok = record_ok and check_phone_number(r.phone_num)
    
    # Check that email is <username@domain name> where domain is <string.string>
    record_ok = record_ok and check_email(r.email)
    
    return record_ok


def convert_date_to_format(date):
    """
    Converts date to <Month:Str> <day:int> <year:int>

    Parameters
    ----------
    date : datetime.datetime.date
        Date to convert

    Returns
    -------
    date : TYPE
        date in <Month:Str> <day:int> <year:int> format

    """
    
    date = date.strftime("%B X%d %Y").replace('X0','X').replace('X','')
    
    return date

def gen_faker_record():
    """
    Generates a record of random data.
    Field:
        Membership number* (Mno^): 6 digit number
        Name: First name^*, middle name (MI^), Last name^*
        Date of birth*(DoB^): Date with format <Month DD Year> e.g. June 15 1996 
        Address^: String
        Status^*: {Basic, Silver, Gold, Platinum, None}
        Membership start date* (msd^):
        Membership end date (med^)
        Renewal date* (rdate^):
        Phone^*:  10 digit number with format (##########)
        Email^: String
        Notes^: 

    Parameters
    ----------
    None

    Returns
    -------
    record: Record
        Class Record with attributes randomly assigned with faker

    """
    from faker import Faker
    import random
    import re
           
    # Create faker instance
    fake = Faker('en_US')
    
    # Random membership number. Leaving room for new membership numbers.
    mem_num = str(random.randint(100000, 700000)).zfill(6)
        
    # Random name
    name = fake.name()
    while not check_name(name.replace(' ', '')):
        name = fake.name()
    names = re.split(' ', name)
    first_name = names[0]
    last_name = names[1]
    
    # Random birthday
    birthday = fake.date_between('-100y', '-18y')
    
    # Random status
    status_list = ('Basic', 'Silver', 'Gold', 'Platinum', 'None')
    member_status = random.choice(status_list)
    
    # Make random start date at least birthday + 18 years
    earliest = max(EARLIEST_START_DATE, birthday + relativedelta(years=18))
    start_date = fake.date_between(earliest, TODAY)
    
    # If member_status is None, create an end date between start date and today
    end_date = ""
    if member_status == 'None':
        end_date = fake.date_between(start_date, TODAY)
    
    # Make random renewal date between now and five years from now
    renewal_date = fake.date_between(TODAY, 
                                     TODAY + relativedelta(years=5))
    
    # Random 10-digit phone number
    phone_number = []

    phone_number = str(random.randint(200, 999)).zfill(3) + \
                   str(random.randint(200, 999)).zfill(3) + \
                   str(random.randint(0, 9999)).zfill(4)
        

    # Convert dates to Month Day Year strings
    birthday = convert_date_to_format(birthday)
    start_date = convert_date_to_format(start_date)
    if end_date != "":
        end_date = convert_date_to_format(end_date)
    renewal_date = convert_date_to_format(renewal_date)

    # Create a record with the required data    
    record = Record(mem_num, first_name, last_name, birthday, member_status,
                  start_date, renewal_date, phone_number, end=end_date)        
    """
    # For testing
    print("membership number:", mem_num)
    print("name:", name) 
    print("birthday:", birthday)
    print("member status:", member_status)
    print("start date:", start_date)
    print("renewal data:", renewal_date)
    print("phone number:", phone_number)
    
    print()
    print(record)
    """
    
    return record


def gen_file_data(num_members):
    """
    Generates and returns a list of num_members random Records.
    Parameters
    ----------
    num_members : int
        Number of random members to create.

    Returns
    -------
    data : list of Records
        List of num_memember random Records.

    """
    
    # Initialize blank data list
    data = []
    print("num_members:", num_members)
    
    # Check for data constraints
    for i in range(0, int(num_members)):
        record = gen_faker_record()
        while not check_record(record, data):
            record = gen_faker_record()
        data.append(record)
  
    return data
    

def main(arg):
    """
    Runs gen_member_data.py
    
    The script will take arguments in the following format   
        “python gen_member_data.py -no <no of members> -fname <filename>”
        <no of members> is number of random members to be generated in file with <filename>
        If no arguments are given, generate by default 1000 members and 
            save them in a new file “memberdata.csv”

    All required attributes are randomly generated for each member.
    All the generated members attributes pass the validation checks

    Parameters
    ----------
    arg : command line arguments
        Command line arguments.

    Returns
    -------
    None.

    """
    #Eliminate program call from argument list
    if len(sys.argv) != 1:
        arg = sys.argv[1:]
    else:
        # default values
        num_members = 1000
        filename = 'memberdata.csv'

    # Initialize n to argument 1 (the first option)
    n = 0
    
    # Loop through arguments
    while n < len(arg):
        # If the option is 'o', get the number of members to create
        if arg[n] == "-o":
            # Num of members is the subsequent argument
            if not arg[n+1].isdigit:
                print("Noninteger argument for number of members")
                sys.exit(-1)
            num_members = arg[n+1]
            print("Number of members:", num_members)
            # Increment argument count by 2
            n = n + 2            
        # If the option is 'fname', get the filename to write
        elif arg[n] == "-fname":
            # Filename is the subsequent argument
            filename = arg[n+1]
            print ("Create file:", filename)
            # Increment argument count by 2
            n = n + 2
        # Else, the argument is invalid
        else:
            print("Invalid argument")
            sys.exit(-1)

    # Genereate the data for the file
    print(num_members)
    data = gen_file_data(num_members)

    fields = ['Membership number', 'First name', 'Middle name', 'Last name', 'Date of birth', 
              'Address', 'Status', 'Membership start date', 'Membership end date', 'Renewal date',
              'Phone', 'Email', 'Notes']

    # Write data to csv
    try:
        with open(filename, 'w', newline='') as file:
            # Create a writer object
            writer = csv.writer(file, delimiter=',')
            
            # Write the headers
            writer.writerow(fields)
            
            # Write the data
            for r in data:                
                writer.writerow([r.mem_num, r.first_name, r.middle_name, r.last_name, r.birthday,
                                 r.address, r.status, r.start_date, r.end_date, r.renewal_date,
                                 r.phone_num, r.email, r.notes])
    # If the file cannot complete the writing, exit.
    except IOError:
        print(f"Creating {filename} failed. Exiting program.")
        sys.exit(-1)
        
    # End the program
    sys.exit(0)
        
# For testing
#arg = ["-o", NUM_MEMBERS, "-fname", FILENAME]
arg = []
    
if __name__ == "__main__":
    main(arg)
        
# main()


    
     
