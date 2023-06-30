# -*- coding: utf-8 -*-
"""
The is a membership management program. The program will read the data at memberdata.csv. 
The input file can be changed at DATA_FILE below. The import file's path is at IMPORT_FILE

py Mange_members.py --graph <mode> has three options:
    <status>:  This will plot a bar graph of number of members vs membership status
    <age>:  This will plot bar graph of number of active members in following age category, 
            18-25, 25-35, 35-50, 50-65, >=65
    <year>:  Bar graph of number of new members added and number of members left vs year 
            {1981 to 2019}.
            
The application has the following options.
a. Add a new member
b. Remove member
c. Upgrade/Downgrade membership
d. Modify member data
e. Import members (csv or a text file)
f. Search for a member
g. Bulk operation
h. Help
q. Quit application

Created on %(date)s

@author: %('Ben Morris')s
"""
import sys
import pandas as pd
import numpy as np
import re
import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt

import gen_member_data

# Global variable to store file contents, edit user data, and write back to the file
member_df = pd.DataFrame()

# Options for displaying DataFrames
pd.options.display.show_dimensions = False
pd.options.display.max_columns = None
pd.options.display.max_rows = None
pd.options.display.max_colwidth = None
pd.options.display.expand_frame_repr = False

# Constant to store data file
DATA_FILE = 'memberdata.csv'
IMPORT_FILE = 'memberdata2.csv'

# Dictionary converting attribute shortcuts to data headers
attributes = {
    'mbo': 'Membership number', 
    'fname': 'First name', 
    'mi': 'Middle name', 
    'lname': 'Last name', 
    'dob': 'Date of birth', 
    'address': 'Address', 
    'status': 'Status', 
    'msd': 'Membership start date', 
    'med': 'Membership end date', 
    'rdate': 'Renewal date',              
    'Phone': 'Phone', 
    'email': 'Email', 
    'notes': 'Notes'
    }


def quit_app():
    """
    Quits application

    Returns
    -------
    None.

    """
    print("Quitting application.")    
    sys.exit()
    
    return


def menuInput(prefix=""):
    """
    Checks input for q or Q at every input at the main menu. Exits the application.
    
    Returns
    -------
    a : string
        user input other than 'q' or 'Q'
    """
    a = input(prefix)
    
    if a == 'q' or a == 'Q':
        quit_app()
    else:
        return a
    
    
def submenu_input(prefix):
    """
    Checks input for q or Q at every input in the submenus. Exits to the main menu.
    Resourced from: https://stackoverflow.com/questions/47337872/how-would-i-code-q-to-quit-python-3-6
    
    Returns
    -------
    a : string
        user input other than 'q' or 'Q'
    """
    a = input(prefix)
    
    if a == 'q':
        main_menu()
    else:
        return a
    
def add_member_input(prefix:str):
    """
    Checks input for q or Q or h or H at every input in the function.
    Resourced from: https://stackoverflow.com/questions/47337872/how-would-i-code-q-to-quit-python-3-6
    
    Returns
    -------
    a : string
        user input other than 'q' or 'Q'
    """
    a = input(prefix).lower()
    
    if a == 'q':
        main_menu()
    elif a == 'h':
        add_member_help()
    else:
        return a


def remove_member_input(prefix:str):
    """
    Checks input for q or Q or h or H at every input in the function.
    Resourced from: https://stackoverflow.com/questions/47337872/how-would-i-code-q-to-quit-python-3-6
    
    Returns
    -------
    a : string
        user input other than 'q' or 'Q'
    """
    a = input(prefix).lower()
    
    if a == 'q':
        main_menu()
    elif a == 'h':
        remove_member_help()
    else:
        return a
    
    
def change_status_input(prefix:str):
    """
    Checks input for q or Q or h or H at every input in the function.
    Resourced from: https://stackoverflow.com/questions/47337872/how-would-i-code-q-to-quit-python-3-6
    
    Returns
    -------
    a : string
        user input other than 'q' or 'Q'
    """
    a = input(prefix).lower()
    
    if a == 'q':
        main_menu()
    elif a == 'h':
        change_status_help()
    else:
        return a
    

def modify_data_input(prefix:str):
    """
    Checks input for q or Q or h or H at every input in the function.
    Resourced from: https://stackoverflow.com/questions/47337872/how-would-i-code-q-to-quit-python-3-6
    
    Returns
    -------
    a : string
        user input other than 'q' or 'Q'
    """
    a = input(prefix).lower()
    
    if a == 'q':
        main_menu()
    elif a == 'h':
        modify_member_help()
    else:
        return a
    
    
def import_input(prefix:str):
    """
    Checks input for q or Q or h or H at every input in the function.
    Resourced from: https://stackoverflow.com/questions/47337872/how-would-i-code-q-to-quit-python-3-6
    
    Returns
    -------
    a : string
        user input other than 'q' or 'Q'
    """
    a = input(prefix).lower()
    
    if a == 'q':
        main_menu()
    elif a == 'h':
        import_help()
    else:
        return a
    
    
def search_input(prefix:str):
    """
    Checks input for q or Q or h or H at every input in the function.
    Resourced from: https://stackoverflow.com/questions/47337872/how-would-i-code-q-to-quit-python-3-6
    
    Returns
    -------
    a : string
        user input other than 'q' or 'Q'
    """
    a = input(prefix).lower()
    
    if a == 'q':
        main_menu()
    elif a == 'h':
        search_help()
    else:
        return a


def bulk_input(prefix:str):
    """
    Checks input for q or Q or h or H at every input in the function.
    Resourced from: https://stackoverflow.com/questions/47337872/how-would-i-code-q-to-quit-python-3-6
    
    Returns
    -------
    a : string
        user input other than 'q' or 'Q'
    """
    a = input(prefix).lower()
    
    if a == 'q':
        main_menu()
    elif a == 'h':
        bulk_help()
    else:
        return a

    
def add_member_help():
    """
    Prints help for the function.

    Returns
    -------
    None.

    """
    print("\nYou must enter information for all required attributes.\n"
          "\tEnter <q> to quit or <h> for help.\n\n"
          "New mbo (membership number) will be the largest previous number plus 1.\n"
          "to the file only if it passes all the checks with a new Mno which is the largest no +1.\n" 
          "Msd (membership start date)3 if not stated would be today’s date.\n"
          "The renewal date if not provided would be one year from Msd.\n")
    
    input("Press <enter> to continue.")
    
    return


def add_member():
    """
    Asks member attributes one after the other except the Mno, which will be created.  
    Validates the format of the value entered for each attribute, 
    give user a warning and remind the required format and give an opportunity to enter the 
    same attribute again. The user can simply press enter not to specify a value for 
    non-required attributes. A new member should be successfully added to the file only if 
    it passes all the checks with a new Mno which is the largest no +1. Msd if not stated would 
    be today’s date. The renewal date if not provided would be one year from Msd.
    
    Returns
    -------
    None.

    """
    # df storing user records
    global member_df
    
    print("\n********************************************************************\n"
          "Adding a member.\n"
          "Select q to return to the main menu or h for help\n"
          "********************************************************************\n")
       
    # Create a membership number.
    max_mem_num = member_df['Membership number'].max() 
    # Find the max membership #, convert it to integer, add one, and convert it back to a string
    new_mem_num = str(int(max_mem_num) + 1)

    # Get user's first name. Required.
    fname = ""
    input_valid = False
    while not fname or not input_valid:
        fname = add_member_input("REQUIRED: Please enter the user's first name> ")
        if fname:
            fname = fname.capitalize()
            # Validate
            input_valid = gen_member_data.check_name(fname)
    
    
    # Get user's middle name. Optional
    mname = ""
    input_valid = False
    while not input_valid:
        mname = add_member_input("\nOPTIONAL: Please enter the user's middle name or "
                              "<Enter> to skip> ")
        if mname:
            mname = mname.capitalize()
            input_valid = gen_member_data.check_name(mname)
        # If no name was entered, set input_valid to True
        else:
            input_valid = True
    
            
    # Get user's last name. Required.
    lname = ""
    input_valid = False
    while not lname or not input_valid:
        lname = add_member_input("\nREQUIRED: Please enter the user's last name> ")
        if lname:
            lname = lname.capitalize()
            # Validate
            input_valid = gen_member_data.check_name(lname)
      
    # Get user's birthday. Required
    dob = ""
    input_valid = False
    while not dob or not input_valid:
        dob = add_member_input("\nREQUIRED: Please enter the user's date of birth. (Ex: June 9 2002)> ")
        conv_dob = gen_member_data.convert_date(dob)
        # Validate
        input_valid = gen_member_data.check_dob(conv_dob)
    
    # Get user's address. Optional
    address = ""
    input_valid = False
    while not input_valid:
        address = add_member_input("\nOPTIONAL: Please enter the user's address or <Enter> to skip> ")
        # Validate address
        if address:
            input_valid = gen_member_data.check_address(address)
        # If no address was entered, set input_valid to True
        else:
            input_valid = True
    
    # Get user's membership status. Required. Options: {Basic, Silver, Gold, Platinum, None}
    status = ""
    input_valid = False
    while not status or not input_valid:
        status = add_member_input("\nREQUIRED: Please enter the user's status.\n"
                               "Options: {Basic, Silver, Gold, Platinum, None}> ")    
        if status:
            status = status.capitalize()
            # Validate
            input_valid = gen_member_data.check_status(status)
    
    
    # Get user's membership start date. Required
    start_date = ""
    input_valid = False
    while not input_valid:
        start_date = add_member_input("\nREQUIRED: Please enter the user's start date. (Ex: June 9 2002)\n"
                                   "Press <Enter> to select today's date or <q> to return to the main menu> ")
   
        # If no start_date was entered, set conv_date to today's date
        if not start_date:
            conv_start_date = gen_member_data.TODAY
        # Otherwise, convert the start_date to datetime.date
        else:
            conv_start_date = gen_member_data.convert_date(start_date)
         
        # Validate
        input_valid = gen_member_data.check_start_date(conv_start_date, conv_dob)

        
    # Get user's membership end date. Required if Status is None.
    end_date = ""
    input_valid = False
    while not input_valid:
        end_date = add_member_input("\nPlease enter the user's end date. (Ex: June 9 2002)\n"
                                 "Required if the member's status is None.\n"
                                 "If optional, press <Enter> to skip.> ")
        # Validate
        if end_date:
            conv_end_date = gen_member_data.convert_date(end_date)
            input_valid = gen_member_data.check_end_date(conv_end_date, conv_start_date)

        # If no end_date was entered and Status = none, set input_valid to True
        elif end_date == "" and status != 'None':
            input_valid = True
        
    # Get user's membership renewal date. Required
    renewal_date = ""
    input_valid = False
    while not input_valid:
        renewal_date = add_member_input("\nREQUIRED: Please enter the user's renewal date. (Ex: June 9 2024)\n"
                                   "Press <Enter> to select one year from the start date\n"
                                   "or press <q> to return to the main menu> ")
   
        # If no renewal_date was entered, make it one year from the start date
        if not renewal_date:
            conv_renewal_date = conv_start_date + relativedelta(years=1)
        # Otherwise, convert the renewal_date to datetime.date
        else:
            conv_renewal_date = gen_member_data.convert_date(renewal_date)
         
        # Validate
        input_valid = gen_member_data.check_renewal_date(conv_renewal_date, conv_start_date)

    # Get user's phone number. Required.
    pnumber = ""
    input_valid = False
    while not pnumber or not input_valid:
        pnumber = add_member_input("\nREQUIRED: Please enter the user's phone number (Format: 9999999999> ")
        # Validate
        input_valid = gen_member_data.check_phone_number(pnumber)
    
    # Get user's email address. Optional
    email = ""
    input_valid = False
    while not input_valid:
        email = add_member_input("\nOPTIONAL: Please enter the user's email address or "
                              "<Enter> to skip> ")
        if email:
            email = email.lower()
            input_valid = gen_member_data.check_email(email)
        # If no email address was entered, set input_valid to True
        else:
            input_valid = True
    
    # Get user's notes. Optional
    notes = add_member_input("\nOPTIONAL: Please enter any notes or <Enter> to skip> ")
    
    record = gen_member_data.Record(new_mem_num, fname, lname, dob, status,
                                    start_date, renewal_date, pnumber, middle=mname,
                                    address=address, end=end_date, email=email, notes=notes)
    
    record_df = pd.DataFrame.from_dict([record.as_dict()])

    member_df = pd.concat([member_df, record_df], ignore_index=True)
  
    member_df.to_csv(DATA_FILE, index=False)

    return 

def remove_member_help():
    """
    Prints help for the function.

    Returns
    -------
    None.

    """
    print("\nYou will be prompted to search for a user to remove. Removals are permanent.\n")
    
    input("Press <enter> to continue.")
    
    return


def remove_member():
    """
    Asks user to determine who to remove. Removes the user from the file.

    Returns
    -------
    None.

    """
    print("\n********************************************************************\n"
          "Removing a member.\n"
          "Select q to return to the main menu or h for help\n"
          "********************************************************************\n")
    # df storing user records
    global member_df
    
    # Search for matching user/s and their indices.
    found_df, idx = do_search()

    # Initialize idx to the first argument
    idx = idx[0]

    # If there is more than one match, have user pick one.
    if len(found_df) > 1:
        found_df, idx = choose_member(found_df)        
    
    # Member inforomation
    print(f"Membership Number: {found_df['Membership number'][idx]} \n"
          f"Name: {found_df['First name'][idx]} "
          f"{found_df['Last name'][idx]}\n")

    # There is now one match
    if len(found_df) == 1:
        # Initialize variable for choice
        choice = ""   
        
        # Loop until valid input.
        while choice != 'y' and choice != 'n':
            choice = remove_member_input("Remove member? (y/n)> ")
            if choice:
                choice = choice.lower()
         
        # If the user wants to remove the member.
        if choice == 'y':
            print("\n"
                  f"Removing Membership Number: {found_df['Membership number'][idx]}, "
                  f"Name: {found_df['First name'][idx]} "
                  f"{found_df['Last name'][idx]}")
            try:
                # Drop member from df
                member_df.drop(idx, inplace=True)
                # Write df to DATA_FILE
                member_df.to_csv(DATA_FILE, index=False)
                print("\nMember removed")
            except:
                print(f"Error removing Member number: {found_df['Membership number'][idx]}.")             
    return


def change_status_help():
    """
    Prints help for the function.

    Returns
    -------
    None.

    """
    print("\nYou will be asked to select a member. Then you will be asked the status to change to.\n"
          "If 'None' is chosen, the membership end date will be set today.\n"
          "This can be changed in 'Modify member data' if needed.")
    
    input("Press <enter> to continue.\n")
    
    return " "


def change_status():
    # df storing user records
    global member_df
    
    print("\n********************************************************************\n"
          "Changing membership status.\n"
          "Select q to return to the main menu or h for help\n"
          "********************************************************************\n")
    # Get df and indices of matches
    found_df, idx = do_search()
    
    # Valid choices for status
    valid_status = ['Basic', 'Silver', 'Gold', 'Platinum', 'None']

    # Necessary for turning into an integer
    idx = idx[0]
    
    # If more than one match, choose one.
    if len(found_df) > 1:
        found_df, idx = choose_member(found_df)
    
    # When a match is chosen
    if len(found_df) == 1:        
        user_status = member_df['Status'][idx]

        # Print chosen member
        print()

        # Loop to ensure proper y/n input only
        choice = ""                    
        while choice != 'y' and choice != 'n':
            choice = change_status_input("\nChange Status? (y/n)> ")
            if choice:
                choice = choice.lower()
        
        # If the user wants to change the member's status
        if choice == 'y':
            # Remove the user's status from the options to change to
            valid_status.remove(user_status)
            print()
            try:
                # Loop until input is valid
                status = False
                while not status:
                    # Get choice
                    new_status = change_status_input("What would you like to change Status to?\n"
                                               f"Options are: {valid_status}> ")

                    # Validate status
                    if new_status.capitalize() in valid_status and gen_member_data.check_status(new_status):
                        
                        # Change status
                        found_df['Status'] = new_status.capitalize()
                        new_renewal_date = datetime.datetime.now().date() + relativedelta(years=1)  
                        new_renewal_date = gen_member_data.convert_date_to_format(new_renewal_date)
                        # Set renewal date to one year from today
                        found_df['Renewal date'] = str(new_renewal_date)                         
                        status = True
                # If changing the status to none, set Member end date to today    
                print_pretty(found_df)
                if new_status == 'none':# and found_df['Membership end date'] == "":                    
                    today = gen_member_data.convert_date_to_format(datetime.datetime.now().date())
                    found_df['Membership end date'] = today
                # If changing from 'None', remove end date
                if user_status == 'None':
                    found_df['Membership end date'] = ""                        
                    
                print_pretty(found_df)
                # Remove old data
                member_df.drop(idx, inplace=True)  
                # Add new data to member_df
                member_df = pd.concat([member_df, found_df], ignore_index=True)               
                
                print("member_df:", member_df.tail(5))
                # Write data to file
                member_df.to_csv(DATA_FILE, index=False)
                print("\nStatus changed")
                # Print new member info
                
            except:
                print(f"Member number: {found_df['Membership number'][idx]} "
                      "not found")             
    #Couldn't find kendra
    
    return


def print_pretty(df):   
    """
    Prints in a nicer format

    Parameters
    ----------
    df : DataFrame
        User information.

    Returns
    -------
    None.

    """
    print(df.T)    
    
    return


# Dictionary to call check functions for each attribute
check_att = {
    'mbo': gen_member_data.check_mem_num, 
    'fname': gen_member_data.check_name,
    'mi': gen_member_data.check_name, 
    'lname': gen_member_data.check_name, 
    'dob': gen_member_data.check_dob, 
    'address': gen_member_data.check_address, 
    'status': gen_member_data.check_status, 
    'msd': gen_member_data.check_start_date, 
    'med': gen_member_data.check_end_date, 
    'rdate': gen_member_data.check_renewal_date,
    'phone': gen_member_data.check_phone_number, 
    'email': gen_member_data.check_email,
    'notes': gen_member_data.check_notes
    }


def check_for_duplicate(df):
    """
    Checks for a duplicate in member_df

    Parameters
    ----------
    df : DataFrame
        DataFrame to look for duplicate of.

    Returns
    -------
    found_df : DataFrame
        Matches to df.
    """

    print("Checking records for match to membership number, name, and birthday...")
    # To hold matches to df
    found_df = pd.DataFrame()
    
    # Check membership number first
    attribute = 'Membership number'
    value = df[attribute].to_string(index=False)
    found_df = member_df[member_df[attribute] == value]

    # If at least one match was found.
    if len(found_df) > 1:
        print(f"A member with membership number {value} already exists.")
        print_pretty(found_df)
        return found_df
    
    # Check date of birth
    attribute = 'Date of birth'
    value = df[attribute].to_string(index=False)
    found_df = member_df[member_df[attribute] == value]
    
    # If at least one match was found to dob, check found for match to Last name
    if len(found_df) > 0:
        # Check Last name
        attribute = 'Last name'
        value = df[attribute].to_string(index=False)
        found_df = found_df[found_df[attribute] == value]
        
        # Check found for match to Middle name
        if len(found_df) > 0:
            # Check Middle name
            attribute = 'Middle name'
            value = df[attribute].to_string(index=False)
            found_df = found_df[found_df[attribute] == value]
            
            # Check found for match to First name
            if len(found_df) > 0:
                # Check First name
                attribute = 'First name'
                value = df[attribute].to_string(index=False)
                found_df = found_df[found_df[attribute] == value]
                
                # If there are matches to dob, and all names
                if len(found_df) > 0:
                    # There is a record matching the name and birthday.
                    print("There is a pre-existing record matching name and birthday.\n")
                    print_pretty(found_df)
                    return found_df

    # If there are no matches
    print("There are no duplicate records.\n")
       
    return found_df    


def check_modify_for_duplicate(df):
    """
    Specific check for duplicates in modify_member

    Parameters
    ----------
    df : DataFrame
        Record to check for duplicate of.

    Returns
    -------
    found_df : DataFrame
        Holds any matches found.

    """    
    
    print("Checking records for match to membership number, name, and birthday...")
    
    # Holds any matches found
    found_df = pd.DataFrame()
    
    # Check membership number
    attribute = 'Membership number'
    value = df[attribute].to_string(index=False)
    found_df = member_df[member_df[attribute] == value]

    # If there is a match to membership number
    if len(found_df) > 1:
        print(f"A member with membership number {value} already exists.")
        print_pretty(found_df)
        return found_df
    
    # Check date of birth
    attribute = 'Date of birth'
    value = df[attribute].to_string(index=False)
    found_df = member_df[member_df[attribute] == value]
    
    if len(found_df) > 1:
        # Check Last name
        attribute = 'Last name'
        value = df[attribute].to_string(index=False)
        found_df = found_df[found_df[attribute] == value]
        
        if len(found_df) > 1:
            # Check Middle name
            attribute = 'Middle name'
            value = df[attribute].to_string(index=False)
            found_df = found_df[found_df[attribute] == value]
            
            if len(found_df) > 1:
                # Check First name
                attribute = 'First name'
                value = df[attribute].to_string(index=False)
                found_df = found_df[found_df[attribute] == value]
                
                if len(found_df) > 1:
                    # There is a record matching the name and birthday.
                    print("There is a pre-existing record matching name and birthday.\n")
                    print_pretty(found_df)
                    return found_df

    # No matches
    print("There are no duplicate records.\n")
       
    return found_df    


def check_modify_mbo_for_duplicate(df):
    """
    Specific check for duplicates in modify_member for mbo

    Parameters
    ----------
    df : DataFrame
        Record to check for duplicate of.

    Returns
    -------
    found_df : DataFrame
        Holds any matches found.

    """    
    
    print("Checking records for match to membership number, name, and birthday...")
    
    # Holds any matches found
    found_df = pd.DataFrame()
    
    # Check membership number
    attribute = 'Membership number'
    value = df[attribute].to_string(index=False)
    found_df = member_df[member_df[attribute] == value]

    # If there is a match to membership number
    if len(found_df) > 0:
        print(f"A member with membership number {value} already exists.")
        print_pretty(found_df)
        return found_df
    
    # Check date of birth
    attribute = 'Date of birth'
    value = df[attribute].to_string(index=False)
    found_df = member_df[member_df[attribute] == value]
    
    if len(found_df) > 1:
        # Check Last name
        attribute = 'Last name'
        value = df[attribute].to_string(index=False)
        found_df = found_df[found_df[attribute] == value]
        
        if len(found_df) > 1:
            # Check Middle name
            attribute = 'Middle name'
            value = df[attribute].to_string(index=False)
            found_df = found_df[found_df[attribute] == value]
            
            if len(found_df) > 1:
                # Check First name
                attribute = 'First name'
                value = df[attribute].to_string(index=False)
                found_df = found_df[found_df[attribute] == value]
                
                if len(found_df) > 1:
                    # There is a record matching the name and birthday.
                    print("There is a pre-existing record matching name and birthday.\n")
                    print_pretty(found_df)
                    return found_df

    # No matches
    print("There are no duplicate records.\n")
       
    return found_df 


def switch_check_att(att, key): 
    """
    Acts like a switch statement, matching the attribute abreviation to it's check function, with
    key as an input

    Parameters
    ----------
    att : str
        Attribute abreviation.
    key : str
        Value to pass to function.

    Returns
    -------
    function
        Check function for attribute.

    """
    att = att.lower()
    key = key.lower()
    
    return check_att.get(att)(key)


def choose_member(df):
    """
    User chooses member in the case of multiple users found.

    Parameters
    ----------
    df : DataFram
        DataFrame of members to choose from.

    Returns
    -------
    found_df : DataFrame
        The chosen match.
    idx : int
        Index in member_df of the chosen user.

    """
    
    # Loop until valid input    
    status = False
    while not status:                       
        print("Choose a member:")
        # Loop to make sure choice is valid
        valid_input = False
        while not valid_input:
            idx = submenu_input("\nThere is more than one match for those criteria.\n"
                                "Enter the index of the record you would like to change or "
                                "<q> to return to the main menu:> ")
            idx = int(idx)
            if idx in df.index:
                valid_input = True
                
        found_df = member_df.loc[int(idx)].to_frame().T
        status = True

    return found_df, idx


def modify_member_help():
    print("\nYou will be asked to select a member.\n"
    "Then you will use the key name of the attribute and enter a new value.\n"
    "Membership start dates (msd) cannot be changed.\n")
    
    input("Press <enter> to continue.")
    
    return " "


def modify_member():
    """
    Option to modify member data

    Returns
    -------
    None.

    """
    # df storing user records
    global member_df
    
    print("\n********************************************************************\n"
          "Modifying member data.\n"
          "Select q to return to the main menu or h for help\n"
          "********************************************************************\n")
    
    # Get matches to user search
    found_df, idx = do_search()
    
    # If no matches, exit
    if len(found_df) == 0:
        return
    # If there is more than one match, have user pick one.
    elif len(found_df) > 1:
        found_df, idx = choose_member(found_df)               
    
    # Loop to ensure only y/n input only
    choice = ""
    while choice != 'y' and choice != 'n':
        choice = modify_data_input("\nChange member data? (y/n)> ")
        if choice:
            choice = choice.lower()
    
    # If the user wants to change input
    if choice == 'y':            
        print()
        change_att = None
        while change_att is None:                
            attribute = modify_data_input("What attribute would you like to change? (ex: Mbo)> ")
            if attribute:
                attribute = attribute.lower()
                change_att = attributes.get(attribute)
                print("change_att:", change_att)
                if not change_att:
                    print(f"Attribute {attribute} does not exist.\n")
                    return
                        
        if attribute == "status":
            print("\nPlease use Upgrade/Downgrade membership from the main menu to change a user's Status.")
            return

        if attribute == "msd":
            print("\nMembership start dates cannot be changed.")
            return            
                            
        print(f"\nCurrent {change_att}: {found_df[change_att].to_string(index=False)}\n")

        # Loop until valid change is picked.
        valid_change = False
        while not valid_change:
            if attribute == "dob":
                new_att = modify_data_input("What would you like to change Date of birth to?\n"
                                        "(Format: June 11 2001)> ")
                valid_change = gen_member_data.check_dob(new_att)
            else:
                new_att = modify_data_input(f"What would you like to change {change_att} to? > ")
                if attribute == "med":
                    end_date = gen_member_data.convert_date(new_att)
                    start_date = found_df['Membership start date'].to_string(index=False)            
                    valid_change = gen_member_data.check_end_date(end_date, start_date)
                elif attribute == "rdate":
                    renewal_date = gen_member_data.convert_date(new_att)
                    start_date = found_df['Membership start date'].to_string(index=False)            
                    valid_change = gen_member_data.check_renewal_date(renewal_date, start_date)
                elif attribute == "mbo":
                    valid_change = gen_member_data.check_mem_num(new_att, member_df)
                else:
                    valid_change = switch_check_att(attribute, new_att)
                
            if not valid_change:
                print("\n\tYour input is invalid. Try again.\n")
            print()
                  
        #Change attribute of record to new_att            
        found_df[change_att][idx] = new_att.capitalize()
        print("check mod:", check_modify_mbo_for_duplicate(found_df))

        # If changing Name or Date of birth, check for duplicate records with matching Names and Dates of birth
        if not (attribute in {'fname', 'mi', 'lname', 'dob'} and len(check_modify_for_duplicate(found_df)) > 1):
            if not (attribute == 'mbo' and len(check_modify_mbo_for_duplicate(found_df)) > 0):
                member_df[change_att][idx] = new_att.capitalize()
                member_df.to_csv(DATA_FILE, index=False)
                print("Record changed:")  
                print_pretty(member_df.loc[idx])
            
    return


def check_for_file(path):
    """
    Checks for existence of file

    Parameters
    ----------
    path : str
        Path to file.

    Returns
    -------
    None.

    """    
    
    import os.path
    
    return(os.path.isfile(path))


def record_from_row(df):
    """
    Gets a Record (gen_member_data.py) from the row of data in a DataFrame

    Parameters
    ----------
    df : DataFrame
        DataFrame to convert to a record.

    Returns
    -------
    Record
        DataFrame in Record form.

    """
        
    r = df.to_dict('list')
    mbo = r['Membership number'][0]
    first = r['First name'][0]
    last = r['Last name'][0]
    dob = r['Date of birth'][0]
    status = r['Status'][0]
    start = r['Membership start date'][0]
    renewal = r['Renewal date'][0]
    phone = r['Phone'][0]
    middle = r['Middle name'][0]
    address = r['Address'][0]
    end = r['Membership end date'][0]
    email = r['Email'][0]
    notes = r['Notes'][0]    
    
    return gen_member_data.Record(mbo, first, last, dob, status, start, renewal, phone, middle=middle, 
                 address=address, end=end, email=email, notes=notes)


def check_df_record(df):
    """
    Checks a df that each record is valid.

    Reported to user:
    All the members who have missing required attributes. User is provided 
        2 options: Add them anyway / Don’t add them
    Number of members with invalid attribute values--not added
    All members who may exist already in the previous main file (same Mno or same name and 
        birth date).  User is provided following options:
        Overwrite the existing member data / Do not add these members.
    Total number of new members detected.  Append these members to existing file.

    Parameters
    ----------
    df : DataFrame
        DataFrame to check.

    Returns
    -------
    None.

    """
    # df storing user records
    global member_df
    import io
    from contextlib import redirect_stdout
    
    # Check for invalid attributes
    #   Notify user, but do not add.
    #   Keep track of how many of these there are.
    #   Add them to their own df.
   
    invalid_df = pd.DataFrame() 
    duplicates_df = pd.DataFrame()
    blanks_df = pd.DataFrame()
    num_new_members = 0
    
    # For each row of the df
    for idx in range(0, len(df.index)):
        # Get the row and make a record
        row_df = pd.DataFrame(df.iloc[idx]).copy()
        row_df = row_df.T
        print_pretty(row_df)
        print()
        
        # Create a Record from the row_df
        record = record_from_row(row_df)
        
        # Check for invalid attributes
        #   Notify user, but do not add.
        #   Keep track of how many of these there are.
        #   Add them to their own df.        
        
        if not gen_member_data.check_record(record, member_df):
            invalid_df = pd.concat([invalid_df, row_df], ignore_index=True)            
        
        # Check for duplicate (Mbo or name and dob)
        elif len(check_for_duplicate(row_df)) > 0:
            
            # Suppress printing, but get the df containing the duplicate/s
            trap = io.StringIO()
            with redirect_stdout(trap):
                found_df = check_for_duplicate(row_df)
            
            choice = ""
            while choice != 'y' and choice != 'n':
                choice = submenu_input("\n\tThis record is a duplicate. "
                                             "Would you like to replace the existing member data? (y/n) > ")
                if choice:
                    choice = choice.lower()

            if choice == 'y':
                # Delete duplicate record in member_df.
                member_df.drop([found_df.index[0]], inplace=True)
                # Add row_df to member_df
                member_df = pd.concat([member_df, row_df], ignore_index=True)
                # Write the file
                member_df.to_csv(DATA_FILE, index=False)
                num_new_members = num_new_members + 1

            elif choice == 'n':
                # Add row_df to duplicates and delete from df.
                duplicates_df = pd.concat([duplicates_df, row_df], ignore_index=True)

        else:
            # Check for blank required attributes
            required_att = {'Membership number', 'First name', 'Last name', 'Date of birth', 'Status',
                            'Membership start date', 'Renewal date'}
            
            no_blanks = True
            for att in required_att:
                if row_df[att].to_string(index=False) == "":
                    print("Blank required field.")
                    no_blanks = False
                    break
            
            if no_blanks:
                print("Passed all checks. Adding member.")
                # Add row_df to member_df
                member_df = pd.concat([member_df, row_df], ignore_index=True)
                # Write the file
                member_df.to_csv(DATA_FILE, index=False)
                num_new_members = num_new_members + 1
            else:
                # Loop to ensure y/n input only
                choice = ""
                while choice != 'y' and choice != 'n':
                    choice = submenu_input("Some required fields are blank. Add the record anyway? (y/n)> ")
                    if choice:
                        choice = choice.lower()

                if choice == 'y':
                    print("Adding member.")
                    # Add row_df to member_df
                    member_df = pd.concat([member_df, row_df], ignore_index=True)
                    # Write the file
                    member_df.to_csv(DATA_FILE, index=False)
                    num_new_members = num_new_members + 1
                    
                else:
                        print("Not adding member.")
                        blanks_df = pd.concat([blanks_df, row_df], ignore_index=True)          
        print("\n********************************************************************\n")

    print(f"There are {len(invalid_df)} invalid records in the file. They will not be added.")
    print(f"Adding {num_new_members} records...")
        
    """
    Membership number* (Mno^): 6 digit number
    Name: First name^*, middle name (MI^), Last name^*
    Date of birth*(DoB^): Date with format <Month DD Year> e.g. June 15 1996 
    Status^*: {Basic, Silver, Gold, Platinum, None}
    Membership start date* (msd^):
    Renewal date* (rdate^):
    Phone^*:  10 digit number with format (##########)
    """
    
    return


def import_help():
    print("\nImports new member data from IMPORT_FILE.\n"
          "This will allow user to import a new csv or a text file (in the correct format)\n"
          "to import new members or modify existing members. The new file members are validated.\n"
          "Reported to user:\n"
          "All the members who have missing required attributes. User is provided \n"
          "\t2 options: Add them anyway / Don’t add them\n"
          "Number of members with invalid attribute values--not added\n"
          "All members who may exist already in the previous main file (same Mno or same name and\n"
          "birth date).  User is provided following options:\n"
          "\tOverwrite the existing member data / Do not add these members.\n"
          "Total number of new members detected.  Append these members to existing file.\n")
    
    input("Press <enter> to continue.")
    
    return " "


def import_members():
    """
    Imports new member data from IMPORT_FILE.
    
    This will allow user to import a new csv or a text file (in the correct format) to import new 
    members or modify existing members. The new file members are validated.
    Reported to user:
    All the members who have missing required attributes. User is provided 
        2 options: Add them anyway / Don’t add them
    Number of members with invalid attribute values--not added
    All members who may exist already in the previous main file (same Mno or same name and 
        birth date).  User is provided following options:
        Overwrite the existing member data / Do not add these members.
    Total number of new members detected.  Append these members to existing file.

    Returns
    -------
    None.

    """
    # df storing user records
    global member_df
    
    print("\n********************************************************************\n"
          "Importing member data.\n"
          "Select q to return to the main menu or h for help\n"
          "********************************************************************\n")
    
    # For testing
    #filename = "memberdata2.csv"

    status = False
    while not status:    

        filename = import_input("What is the name of the import file? > ")
        status = check_for_file(filename)
        # If the file doesn't exist, print a warning
        if not status:
            print(f"\n{filename} does not exist.")
            main_menu()
    
    print(f"Importing data from {filename}.")
    
    # DataFrame with new data
    new_df = get_data(filename)
   
    # Checks the DataFrame for validity.
    check_df_record(new_df)
    
    return


def do_search():
    """
    Searches for members given user input

    Returns
    -------
    found_df : DataFrame
        DataFrame of matches.
    found_idx : Array of int
        Array of found indices

    """
    # df storing user records
    global member_df
    
    # Will hold the arguments from the input
    arg = []
    
    # Loop until a non-zero and even number of arguments
    while(len(arg) == 0 or len(arg) % 2 != 0):
        if len(arg) == 1 and arg[0].lower() == 'h':
            search_help()
        choice = search_input("Search attribute and value> ")
        if choice:
            choice = choice.lower()
            arg = re.split("\s", choice)
    
    # Store the attributes and keys in arrays
    attribute = arg[::2]
    key = arg[1::2]
    found_df = member_df.copy()
    found_idx = []
    idx = -1
    
    # Loop through attributes and keys and search in order, narrowing the data set each time
    for n in range(0, len(attribute)):
        search_att = attributes.get(attribute[n])

        if not search_att:
            print(f"\nAttribute {attribute[n]} does not exist.")
            found_df = []

            continue          
        
        search_key = str(key[n])
        
        found_df = found_df.loc[found_df[search_att].str.contains(search_key, case=False)]
    
        print(f"\nSorting by {search_att}: {search_key}")
    
        if not found_df.empty:
            if len(found_df) == 1:            
                for idx in range(0, len(member_df)):                   
                    if member_df.iloc[[idx]].equals(found_df):
                        print_pretty(found_df)
                        print()
            elif len(found_df) > 10:
                # Loop to ensure y/n input only
                choice = ""
                while choice != 'y' and choice != 'n':
                    choice = search_input("\nMore than 10 member matching the criteria. Print? (y/n)")                
                    if choice:
                        choice = choice.lower()
                    
                if choice == 'y':
                    print("\n", found_df)                                    
            else:                
                print(found_df, "\n")
            
            found_idx = found_df.index.values
                      
        else:
            print("No matches found.")
    
    return found_df, found_idx

            
def search_help():
    print("\nUser enters the following keys for the desired search attribute.\n"
          "Mbo: Membership number\n"
          "Fname: First name\n"
          "MI: Middle name\n"
          "Lname: Last name\n"
          "DoB: Date of birth\n"
          "Address: Address\n"
          "Status: Status\n"
          "msd: Membership start date\n"
          "med: Membership end date\n"
          "rdate: Renewal date\n"      
          "phone: Phone\n"
          "Email: Email\n"
          "Notes: Notes\n")
    
    input("Press <enter> to continue.")
    
    return " "


def find_member():
    """
    Runs menu choice for finding member

    Returns
    -------
    None.

    """
    
    print("\n********************************************************************\n"
      "Searching for a member.\n"
      "Select q to return to the main menu or h for help\n"
      "********************************************************************\n")

    do_search()
    
    return


def get_df_by_age():
    """
    Gets the users in member_df matching an age range.

    Age <min age*> < max age>  e.g.  Age 25 40 or Age 65  or Age 18 25 
    (Age 65 means all members with age 65 or above) (age only integer)

    Returns
    -------
    DataFrame
        DataFrame of members matching the requirement.

    """
    print("\nChanging by age range:\n")
    print("\tWhat age range would you like to change?\n")
    
    # Loop for valid input
    status = False
    while status == False:
        choice = submenu_input("Format should be <min age*> <max age>.\n"
                               "Ex: 25 40 (members between 25 and 40, inclusive)\n"
                               "\tor: 65 (all members with age 65 or above) > ")
        
        # Create an array of ages
        age = re.split("\s", choice)
        
        # For each of the ages in the array
        for idx in range(0, len(age)):
            # Check to make sure they are integers and that there are one or two of them.
            if age[idx].isdigit() and len(age) in range (1,3):
                if int(age[idx]) >= 0:
                    status = True
                else:
                    print("Input must be positive.")
                    main_menu()
                
    # Change age into a list of integers
    age = [eval(i) for i in age]
        
    # Determnine start dob and end dob based on range   
    # If there is one argument, that is the minimum age.
    if len(age) == 1:
        # The end date would be today minus age in years. The start date would be at most 200 years ago.
        start_date = datetime.datetime.now().date() - relativedelta(years=200)
        end_date = datetime.datetime.now().date() - relativedelta(years=int(age[0]))
    # If there are two arguments, find the start date and end date
    elif len(age) == 2:
        # Start date would be today minus the older age in years.
        start_date = datetime.datetime.now().date() - relativedelta(years=max(age))
        # End date would be today minus the younger age in years.
        end_date = datetime.datetime.now().date() - relativedelta(years=min(age))

    # DataFrame to store members whose age is in range.
    age_idx = []


    # Go through each row of member_df, find the members in the age range, and add them to age_df
    for idx in member_df.index:      
        #submenu_input('enter')
        # Get the row
        row_df = pd.DataFrame(member_df.iloc[idx])
        row_df = row_df.transpose()

        # Convert dob to datetime.datetime.date
        dob = gen_member_data.convert_date(member_df['Date of birth'][idx])

        # If dob is in range, add it to age_df                       
        if dob >= start_date and dob <= end_date:
            age_idx.append(idx)

    return member_df.iloc[age_idx]


def get_df_by_length():
    """
    Gets the users in member_df matching range of membership length
    
    Member <min period* in years in integer> <max period in years> e.g. member 1 10 or member 10 

    Returns
    -------
    DataFrame
        DataFrame of members matching the requirement.

    """
    print("Changing by membership length\n")
    print("\tWhat membership range would you like to change?\n")
    
    # Loop until valid input
    status = False
    while status == False:
        choice = submenu_input("Format should be <min length*> <max length>.\n"
                               "Ex: 1 10 (members who have been active between 1 and 10 years, inclusive)\n"
                               "\tor: 25 (all members who have been active for 25 years or more) > ")
        
        # Create an array of years
        years = re.split("\s", choice)
        
        # For each of the years in the array
        for idx in range(0, len(years)):
            # Check to make sure they are integers and that there are one or two of them.
            if years[idx].isdigit() and len(years) in range (1,3):
                if int(years[idx]) >= 0:
                    status = True
                else:
                    print("Input must be positive.")
                    main_menu()            
                
    # Change years into a list of integers
    years = [eval(i) for i in years]
        
    # Determnine start year and end year based on range   
    # If there is one argument, that is the minimum membership length.
    if len(years) == 1:
        # The end date would be today minus years. The start date would be at most 200 years ago.
        start_date = datetime.datetime.now().date() - relativedelta(years=200)
        end_date = datetime.datetime.now().date() - relativedelta(years=int(years[0]))
    # If there are two arguments, find the start date and end date
    elif len(years) == 2:
        # Start date would be today minus the older year in years.
        start_date = datetime.datetime.now().date() - relativedelta(years=max(years))
        # End date would be today minus the younger year  in years.
        end_date = datetime.datetime.now().date() - relativedelta(years=min(years))

    # DataFrame to store members whose Membership year is in range.
    years_df = pd.DataFrame()
    
    # Go through each row of member_df, find the members in the membership range and add them to years_df
    for idx in member_df.index:

        # Get the row
        row_df = pd.DataFrame(member_df.iloc[idx]).copy()
        row_df = row_df.T

        # Convert Membership start date to datetime.datetime.date
        msd = gen_member_data.convert_date(row_df['Membership start date'][idx])
        
        # If msd is in range, add it to years_df
        if msd >= start_date and msd <= end_date:
            years_df = pd.concat([years_df, row_df], ignore_index=False)
    
    return years_df

    
def get_df_by_status():
    """
    Gets the users in member_df matching a specific status    

    Status <all membership status*>  E.g. Status basic  or status basic premium or status none

    Returns
    -------
    DataFrame
        DataFrame of members matching the requirement.


    """
    print("Changing by membership status.")
    print("What membership status would you like to change?")
    
    # Loop until valid input
    input_status = False
    while input_status == False:
        choice = submenu_input("\t{'Basic', 'Silver', 'Gold', 'Platinum', 'None'} > ")
        if choice:
            choice = choice.lower()
            choices = {'basic', 'silver', 'gold', 'platinum', 'none'}
                                   
            # Check to make sure the input comes from the above list
            if choice in choices:
            #if choice in choices and re.match('^\\S*$', choice)
                input_status = True

    # DataFrame to store members whose status matches choice
    status_df = member_df[member_df["Status"] == choice.capitalize()]
        
    return status_df


def bulk_push(change_df, num_months):
    """
    Pushes the renewal date for a DataFrame of members. (input is given in integer months)

    Parameters
    ----------
    change_df : DataFrame
        DataFrame of members to modify.
    num_months : int
        Number of months to push renewal date.

    Returns
    -------
    None.

    """
    # df storing user records
    global member_df
    
    if num_months == 1:
        print(f"\nPushing all renewal dates by {num_months} month.")
    else:
        print(f"\nPushing all renewal dates by {num_months} months.")
 
    # For each row,
    # Go through each row of member_df
    for idx in range(0, len(change_df.index)):
        # Get the member_df index
        user_idx = change_df.index[idx]
        try:
            # Get the renewal date
            rdate = member_df['Renewal date'][user_idx]
            # Convert the date to datetime.datetime.date and add two months
            rdate = gen_member_data.convert_date(rdate) + relativedelta(months=num_months)
            # Change rdate back into <Month day year> format
            rdate = gen_member_data.convert_date_to_format(rdate)
            # Change the renewal date of member_df at idx
            member_df['Renewal date'][user_idx] = rdate

        except:
            print(f"The renewal date for Membership number {member_df['Membership number'][user_idx]} cannot be changed.")

    return


def bulk_status_change(change_df):
    """
    Changes status for a DataFrame of members

    Parameters
    ----------
    change_df : DataFrame
        DataFrame of members to modify.

    Returns
    -------
    None.

    """
 

    print("\nChanging all statuses.\n")

    print("What membership status would you like to change them to?")
    
    
    # Loop until valid input.
    input_status = False
    while input_status == False:
        choice = submenu_input("\t{'Basic', 'Silver', 'Gold', 'Platinum', 'None'} > ")
        if choice:
            choice = choice.lower()
            choices = {'basic', 'silver', 'gold', 'platinum', 'none'}
                                   
            # Check to make sure the input comes from the above list
            if choice in choices:
                # valid input
                input_status = True
    
    # If changing from None, erase the end date.
    #if member_df['Status'][change_df.index] == "None": #member_df.loc[change_df.index, "Status"] == "None":
    #   member_df.loc[change_df.index, "Membership end date"] = ""
    for idx in change_df.index:
        if member_df['Status'][idx] == "None":
            member_df["Membership end date"][idx] = ""
                                           
    # If status changed to None, change the Membership end date to today
    if choice == 'none':
        member_df.loc[change_df.index, "Membership end date"] = \
            gen_member_data.convert_date_to_format(datetime.datetime.now().date())
        
    # Change the status in member_df
    member_df.loc[change_df.index, "Status"] = choice.capitalize()
    
    print("Status changed.")

    return


def bulk_remove(change_df):
    """
    Remove members in change_df from member_df

    Parameters
    ----------
    change_df : DataFrame
        DataFrame of members to modify.

    Returns
    -------
    None.

    """
    # df storing user records
    global member_df
    
    print("\nRemoving all selected members.\n")
    
    # Verify user wants to remova the records
    choice = ""
    while choice != 'y' and choice != 'n':
        choice = submenu_input("Are you sure you would like to remove these members? Removal is permanent. (y/n) > ")
    
    try:
        member_df.drop(change_df.index, inplace=True)
        print("\nUsers have been deleted.\n")
    except:
        print("\n\tError deleting users.\n")
    
        
    return


def bulk_help():
    print("\nChoices for group to change:\n"
          "Members for a given age range\n"
          "Members who have been members for more than a certain period\n"
          "Members with certain membership status\n\n"
          "Choices for actions:\n"
          "Push the renewal date. (Input is given in integer months.)\n"
          "Change membership status\n"
          "Remove members\n\n"
          "Formats:"
          "Age <min age*> < max age>  e.g.  Age 25 40 or Age 65  or Age 18 25\n"
          "\t( Age 65 means all members with age 65 or above) (age only integer)\n"
          "Member <min period* in years in integer> <max period in years> \n"
          "\te.g. member 1 10 or member 10\n"
          "Status <all membership status*>  \n"
          "E.g. Status basic  or status basic premium or status none\n")
    
    input("Press <enter> to continue.")
    
    return " "


def bulk_operation():
    """
    Main function to run the bulk operation menu choice

    Returns
    -------
    None.

    """
    print("\n********************************************************************\n"
      "Bulk operation\n"
      "Select q to return to the main menu or h for help\n"
      "********************************************************************\n")
    
    # df storing user records
    global member_df
    
    # Loop until valid input
    action = ""
    while action != 'p' and action != 's' and action != 'r':
        action = bulk_input("Would you like to (p)ush renewal dates, change membership (s)tatus, "
                            "or (r)emove members? > ")
        if action:
            action = action.lower()
    
    change_df = pd.DataFrame()
    
    # Loop until valid input
    group = ""
    while group != 'a' and group != 'l' and group != 's':
        group = bulk_input("\nWhich group? (a)ge range, membership (l)ength, or membership (s)tatus? > ")

    # Group to sort by    
    # Age range    
    if group =='a':
        change_df = get_df_by_age()
    # Membership length
    elif group == 'l':
        change_df = get_df_by_length()
    # Member status
    elif group == 's':
        change_df = get_df_by_status()
    
    # Action to perform
    # Push renewal date
    if action == 'p':                
        valid_input = False
        while not valid_input:
            num_months = bulk_input("\n How many months would you like to push the renewal dates? > ")
            if num_months.isdigit() and int(num_months) > 0:
                valid_input = True
        bulk_push(change_df, int(num_months))
    # Change status
    elif action == 's':
        bulk_status_change(change_df)
    # Remove user/s
    elif action == 'r':                     
        bulk_remove(change_df)
    
    # Write updated DataFrame
    member_df.to_csv(DATA_FILE, index=False)
    
    return


def app_help():
    """
    Help for main menu

    Returns
    -------
    None.

    """
    print("\nOptions are:\n"
          "a. Add a new member: adds a new member; asks for all attributes but mbo\n"
          "b. Remove member: removes a member\n"
          "c. Upgrade/Downgrade membership: changes a member's status\n"
          "d. Modify member data: modifies a member's data\n"
          "e. Import members (csv or a text file): imports member data\n"
          "f. Search for a member: finds a member's record\n"
          "g. Bulk operation: pushes renewal date, changes status, or removes members of a group\n"
          "   Group options: members of an aga range, membership lengths of a range, membership status\n"
          "h. Help\n"
          "q. Quit application\n")

    return


def menu():
    """
    Prints main menu.

    Returns
    -------
    None.

    """
    print("\n********************************************************************\n"
          "\t\tWelcome to the Member Manager Application\n"
          "********************************************************************\n\n"
          "a. Add a new member\n"
          "b. Remove member\n"
          "c. Upgrade/Downgrade membership\n"
          "d. Modify member data\n"
          "e. Import members (csv or a text file)\n"
          "f. Search for a member\n"
          "g. Bulk operation\n"
          "h. Help (optional*)\n"
          "q. Quit application\n")


def get_choice():
    """Gets the choice

    Parameters
    ----------
    none

    Returns
    -------
    choice: str
        User menu choice
    
    """
    # Initialize choice
    choice = ""
    
    # While the string is empty or has special characters, get input again
    while(choice == "" or choice not in choices):
        # Get the input
        print("Please enter a choice (letter) from the menu> ", end="")
        choice = menuInput()
        choice = choice.lower()

    return choice

# Function names to switch from menu letter choice
choices = {
    'a': add_member,
    'b': remove_member,
    'c': change_status,
    'd': modify_member,
    'e': import_members,
    'f': find_member,
    'g': bulk_operation,
    'h': app_help,
    }


def switch_choice(choice):
    """
    Acts as a switch stament for user choice in the main menu.

    Parameters
    ----------
    choice : str
        Letter choice of main menu.

    Returns
    -------
    TYPE
        Function call to appropriate menu choice

    """
    return choices.get(choice)()


def handle_choice(choice:str):
    """
    Handles the user choice in the main menu.

    Parameters
    ----------
    choice : str
        DESCRIPTION.

    Returns
    -------
    None.

    """
    choice = choice.lower()    
    switch_choice(choice)
    
    return


def get_data(filename:str):
    """
    Reads the data from the data file into a DataFrame

    Parameters
    ----------
    filename : str
        Name of file to read into DataFrame

    Returns
    -------
    df : DataFrame
        DataFrame representation of the file.

    """
   
    # If the file doesn't exist, exit program
    if not check_for_file(filename):
        print(filename, "does not exist. Exiting program.")
        sys.exit(-1)   
    
    # Open file and read contents into df
    df = pd.read_csv(filename, keep_default_na=False)       

    return df


def main_menu():
    """
    Runs the main menu and handles user choice.

    Returns
    -------
    None.

    """
    menu()
    choice = get_choice()
    handle_choice(choice)
    input("\nPress <Enter> to continue")
    main_menu()
    
    return


def graph_by_status():
    """
    Status:  This will plot a bar graph of number of members vs membership status
    {'Basic', 'Silver', 'Gold', 'Platinum', 'None'}

    Returns
    -------
    None.

    """
    data = [
            member_df['Status'].value_counts()['Basic'],
            member_df['Status'].value_counts()['Silver'],
            member_df['Status'].value_counts()['Gold'],
            member_df['Status'].value_counts()['Platinum'],
            member_df['Status'].value_counts()['None']
           ]

    x_axis = np.arange(len(data))
    status_names = ['Basic', 'Silver', 'Gold', 'Platinum', 'None']
    fig, ax = plt.subplots()
    bars = ax.bar(status_names, data)
    ax.bar_label(bars)
    
    plt.bar(x_axis, data, label = 'Number')
    plt.xticks(x_axis, status_names)
    plt.title("Number of Members With Each Status")
    plt.xlabel("Status", fontsize='13')
    plt.ylabel("Number", fontsize='13')
    plt.legend()
    plt.show()
    
    return


def graph_by_age():
    """
    Age:  This will plot bar graph of number of active members 
    in each of the following age categories: 18-25, 25-35, 35-50, 50-65, >=65

    Returns
    -------
    None.

    """
    active_idx = member_df[member_df['Status'] != 'None'].index

    age_array = []
    
    for idx in active_idx:        
        # Get the birthday       
        dob = member_df['Date of birth'][idx]
        # Convert to datetime
        dob = gen_member_data.convert_date(dob)
        # Get today
        today = datetime.date.today()
        # If the birthday has already happened this year, the age is the difference in years
        if dob.month < today.month:
            age = today.year - dob.year
        elif dob.month == today.month:
            if dob.day <= today.day:
                age = today.year - dob.year
        # Else, the birthday is the difference in years minus one
        else:
            age = today.year - dob.year - 1
                   
        age_array.append(age)
    
    # Graph the number in each bin
    # Age categories: 18-25, 25-35, 35-50, 50-65, >=65
    bins = np.array([18, 25, 35, 50, 65, 120])
    # make the histogram    
    hist, bin_edges = np.histogram(age_array,bins)    
    # Prep subplots
    fig,ax = plt.subplots()          
    # Plot the histogram numbers against age ranges
    ax.bar(range(len(hist)),hist,width=1, label='Number',
           tick_label=['{} - {}'.format(bins[i],bins[i+1])
           for i,j in enumerate(hist)], edgecolor='black')
    # Format plot
    plt.title("Number of Active Members by Age")
    plt.xlabel("Age Range", fontsize='13')
    plt.ylabel("Number", fontsize='13')
    plt.legend()
    plt.show()
 
    return


def graph_by_year():
    """
    Year:  Bar graph of number of new members added and 
    number of members who left vs year {1981 to 2019}. 
    
    Both bars should be plotted side by side for each year in two different colors.

    Returns
    -------
    None.

    """
    start_array = []
    end_array = []
    
    # Get start date and end date for all in member_df
    for idx in member_df.index:
        # Get the start_date       
        start = member_df['Membership start date'][idx]
        # Convert to datetime
        start = gen_member_data.convert_date(start)
        # Add start year to start_array
        start_array.append(start.year)
        
        # Get the end_date
        end = member_df['Membership end date'][idx]
        if end != "":
            # Convert to datetime
            end = gen_member_data.convert_date(end)
            # Add start year to start_array
            end_array.append(end.year)
       
    year_array = range(1981, 2020)
    year_start_count = []
    year_end_count = []    
        
    for year in year_array:
        year_start_count.append(start_array.count(year))
        year_end_count.append(end_array.count(year))
       
    opacity = 0.4
    bar_width = 0.35
    
    plt.title("Number of Beginning and Ending Memberships by Year")
    plt.xlabel('Year')
    plt.ylabel('Number')
    plt.xticks(range(len(year_start_count)), year_array, rotation=90, fontsize = 8)
    
    bar1 = plt.bar(np.arange(len(year_start_count)) + bar_width, year_start_count, bar_width, 
                   align='center', alpha=opacity, color='b', label='Started')
    bar2 = plt.bar(range(len(year_end_count)), year_end_count, bar_width, 
                   align='center', alpha=opacity, color='r', label='Ended')    
    
    # Add counts above the two bar graphs
    for rect in bar1 + bar2:
        height = rect.get_height() + .1
        plt.text(rect.get_x() + rect.get_width() / 2.0, height, f'{height:.0f}', 
                 ha='center', va='bottom', fontsize=6)
    
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    return


def main_help():
    print("\nUse python Manage_members.py to run the program.\n"
          "options:\n"
          "\t--graph <type>\n"
          "Options for <type>:\n"
          "\t'Status': Plots a bar graph of number of members vs membership status\n"
          "\t'Age': plot bar graph of number of active members \n"
          "\tin each of the following age categories: 18-25, 25-35, 35-50, 50-65, >=65\n"
          "\t'Year': Makes a bar graph of number of new members added and \n"
          "\tthe number of members who left vs year {1981 to 2019}.\n")
    
    input("Press <enter> to continue.")
    
    return


def main(arg):
    """
    Runs the Manage_members.py application

    Parameters
    ----------
    arg : array of strings
        Command line arguments

    Returns
    -------
    None.

    """
    # df storing user records
    global member_df
    
    filename = DATA_FILE
    member_df = get_data(filename).astype("string")   
    
    #Eliminate program call from argument list
    if len(sys.argv) != 1:
        arg = sys.argv[1:]
    
    if len(arg) == 0:
    # Run the program
        main_menu() 
    # If there are 2 arguments other than the function call
    if len(arg) == 1:
        if arg[0].lower() == "-h":
            main_help()
            
    elif len(arg) == 2:
        # If the option is --graph, show the chosen graph
        if arg[0].lower() == "--graph":
            if arg[1] in functions_dict:
                functions_dict[arg[1]]()
               
    # Else, the argument/s is invalid
    else:
        print("Invalid argument")
        sys.exit(-1)
    
    return
 
    
# Dictionary for switching user choice for graph type
functions_dict = {
    'status': graph_by_status,
    'age': graph_by_age,
    'year': graph_by_year
    }
   
 
#arg = ['--graph', 'year']
#arg = ['--graph', 'age']
#arg = ['--graph', 'status']
arg = []
   
if __name__ == "__main__":
    main(arg)


