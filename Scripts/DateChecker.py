"""
File Dates Modifier Script

This script is used to modify the modification and creation dates of files in a given directory, this helps with plex having sorting issues with files that have a modification date in the future.

use the manual config to set the path, mode, and resolve. If you do not set the manual config, the script will prompt you for the path, mode, and resolve. 

The script is executed only if it is run as the main program, indicated by `if __name__ == '__main__':`.
"""

import os
from datetime import datetime, timedelta

#Manual Config#
path = None # Format like r'RAW PATH HERE'
Mode = 0 #0 = Unset, 1 = All, 2 = Future
Resolve = 0 #0 = Unset, 1 = Yes, 2 = No

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def prompt_path():
    clear_screen()
    global path
    if path is None:
        path = input('Enter path: ')
    
    if os.path.exists(path):
        if os.path.isfile(path):
            clear_screen()
            input('Path is a file, not a directory. Press Enter to continue.')
            prompt_path()
    else:
        clear_screen()
        input('Path does not exist. Press Enter to continue.')
        path = None
        prompt_path()

def prompt_mode():
    global Mode
    clear_screen()
    print('1 = All, 2 = Future')
    Mode = int(input('Enter Mode: '))
    if Mode != 1 and Mode != 2:
        clear_screen()
        input('Invalid Mode. Press Enter to continue.')
        prompt_mode()

def prompt_resolve():
    global Resolve
    clear_screen()
    print('1 = Yes, 2 = No')
    Resolve = int(input('Enter Resolve: '))
    if Resolve != 1 and Resolve != 2:
        clear_screen()
        input('Invalid Resolve. Press Enter to continue.')
        prompt_resolve()

def get_file_mod_dates(path):
    clear_screen()
    global Mode
    dates = []
    if Mode == 1:
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                mod_time = os.path.getmtime(file_path)
                dates.append((file_path, datetime.fromtimestamp(mod_time)))
        return sorted(dates, key=lambda x: x[1], reverse=True)
    elif Mode == 2:
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                mod_time = os.path.getmtime(file_path)
                if datetime.fromtimestamp(mod_time) > datetime.now():
                    dates.append((file_path, datetime.fromtimestamp(mod_time)))
        return sorted(dates, key=lambda x: x[1], reverse=True)
    else:
        print("Invalid Mode")
        return None

def get_file_creation_dates(path):
    clear_screen()
    global Mode
    dates = []
    if Mode == 1:
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                mod_time = os.path.getctime(file_path)
                dates.append((file_path, datetime.fromtimestamp(mod_time)))
        return sorted(dates, key=lambda x: x[1], reverse=True)
    elif Mode == 2:
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                mod_time = os.path.getctime(file_path)
                if datetime.fromtimestamp(mod_time) > datetime.now():
                    dates.append((file_path, datetime.fromtimestamp(mod_time)))
        return sorted(dates, key=lambda x: x[1], reverse=True)
    else:
        print("Invalid Mode")
        return None

def print_file_mod_dates(dates):
    for file_path, date in dates:
        print(f"{file_path} - {date}")

def resolve_file_mod_dates(dates):
    for file_path, date in dates:
        if date > datetime.now():
            print(f"{file_path} - {date}")
            os.utime(file_path, (os.path.getatime(file_path), datetime.now().timestamp()))

def resolve_file_creation_dates(dates):
    for file_path, date in dates:
        if date > datetime.now():
            print(f"{file_path} - {date}")
            os.utime(file_path, (datetime.now().timestamp(), os.path.getmtime(file_path)))

if __name__ == '__main__':

    if path is None:
        prompt_path()

    if Mode == 0:
        prompt_mode()

    if Resolve == 0:
        prompt_resolve()
    
    if Resolve == 1:
        resolve_file_creation_dates(get_file_creation_dates(path))
        resolve_file_mod_dates(get_file_mod_dates(path))
    elif Resolve == 2:
        print_file_mod_dates(get_file_creation_dates(path))
        print_file_mod_dates(get_file_mod_dates(path))

    print("Done!")
