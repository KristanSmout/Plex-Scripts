"""
Empty Folder Remover Script

This script is used to remove empty folders in a given directory.
"""

import os

#Manual Config#
path = None # Format like r'RAW PATH HERE'
delete = None
verbose = None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_bool(value):
    value = value.lower()
    if value in ['yes', 'true', '1']:
        return True
    elif value in ['no', 'false', '0']:
        return False
    else:
        return None

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

def prompt_delete():
    global delete
    clear_screen()
    delete = get_bool(input('Delete empty folders? (Yes/No): '))
    if delete != True and delete != False:
        clear_screen()
        input('Invalid delete. Press Enter to continue.')
        prompt_delete()

def prompt_verbose():
    global verbose
    clear_screen()
    verbose = get_bool(input('Verbose? (Yes/No): '))
    if verbose != True and verbose != False:
        clear_screen()
        input('Invalid verbose. Press Enter to continue.')
        prompt_verbose()

def delete_empty_folders(path, delete=False, verbose=False):
    for root, dirs, files in os.walk(path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                if delete:
                    os.rmdir(dir_path)
                    if verbose:
                        print(f"Deleted directory: {dir_path}")
                else:
                    if verbose:
                        print(f"Empty directory: {dir_path}")

if __name__ == '__main__':
    if path is None:
        prompt_path()
    
    if delete is None:
        prompt_delete()
    
    if verbose is None:
        prompt_verbose()
    
    delete_empty_folders(path, delete, verbose)