"""
This script will create a historical graph/CSV of the storage usage of your media library. This will be rounded to a daily basis.
You can configure the script below or prompts will be given to you when you run the script.
"""

import os,datetime,csv,pandas as pd,matplotlib.pyplot as plt


#Manual Config#
path = None # Format like r'RAW PATH HERE'
wantpng = True
outputPNG = None
OutputCSV = None
Verbose = None
sizeformat = None# KB,MB,GB,TB

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

def is_valid_path(path):
    global output
    # If the path is not given, use the current directory
    if path is None or path == '':
        output = os.getcwd()
        return True

    # Check if the path is valid
    if not os.path.isdir(path):
        return False
    else:
        return True

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

def prompt_save_path():
    global OutputCSV
    clear_screen()
    save_path = input('Enter CSV path: ')
    validpath = is_valid_path(save_path)
    if not validpath:
        input('Invalid save path. Press Enter to continue.')
        prompt_save_path()
    else:
        if OutputCSV is None:
            OutputCSV = save_path
        date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"HistoricSize-{date_time}.csv"
        return os.path.join(OutputCSV, file_name)  

def prompt_verbose():
    global Verbose
    clear_screen()
    Verbose = get_bool(input('Verbose? (yes/No): '))
    if Verbose != True and Verbose != False:
        input('Invalid response. Press Enter to continue.')
        prompt_verbose()
    else:
        return Verbose

def prompt_sizeformat():
    global sizeformat
    clear_screen()
    sizeformat = input('Size format? (KB/MB/GB/TB): ')
    if sizeformat != "KB" and sizeformat != "MB" and sizeformat != "GB" and sizeformat != "TB":
        input('Invalid response. Press Enter to continue.')
        prompt_sizeformat()
    else:
        return sizeformat

def want_png():
    clear_screen()
    does_want_png = get_bool(input('Save graph as PNG? (yes/No): '))
    if does_want_png != True and want_png != False:
        input('Invalid response. Press Enter to continue.')
        want_png()
    else:
        return does_want_png

def prompt_png_path():
    global outputPNG
    clear_screen()
    save_path = input('Enter PNG save path: ')
    validpath = is_valid_path(save_path)
    if not validpath:
        input('Invalid save path. Press Enter to continue.')
        prompt_save_path()
    else:
        if outputPNG is None:
            outputPNG = save_path
        date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"HistoricSize-{date_time}.png"
        outputPNG = os.path.join(outputPNG, file_name)
        return os.path.join(outputPNG, file_name)

def round_datetime_to_day(dt):
    return dt.date()

def format_size(size):
    if sizeformat == "KB":
        return size / 1024
    elif sizeformat == "MB":
        return size / 1024 / 1024
    elif sizeformat == "GB":
        return size / 1024 / 1024 / 1024
    elif sizeformat == "TB":
        return size / 1024 / 1024 / 1024 / 1024
    else:
        return size

def get_files(path, Verbose=False):
    files = []
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            mtime = os.path.getmtime(filepath)
            dt = datetime.datetime.fromtimestamp(mtime)
            rounded_dt = round_datetime_to_day(dt)
            size = os.path.getsize(filepath)
            size = format_size(size)
            if Verbose:
                print(f"File: {filepath} | Date: {dt} | Rounded: {rounded_dt} | Size: {size}")
            files.append((filepath, rounded_dt, size))
    return files

def get_total_size_by_date(files):
    global Verbose
    # sort the files by date
    sorted_files = sorted(files, key=lambda x: x[1])
    sizes_by_date = {}
    for file in sorted_files:
        date = file[1]
        size = file[2]
        if date in sizes_by_date:
            sizes_by_date[date] += size
        else:
            sizes_by_date[date] = size
    result = [(date, sizes_by_date[date]) for date in sorted(sizes_by_date.keys())]
    if Verbose:
        print(result)
    return result

def create_graph(files):
    global sizeformat
    total_size = 0
    data = []
    for file in files:
        total_size += file[1]
        data.append([file[0], total_size])
        
    df = pd.DataFrame(data, columns=['Date', f'Size ({sizeformat})'])
    fig, ax = plt.subplots(figsize=(10, 7))
    df.plot(x='Date', y=f'Size ({sizeformat})', ax=ax)
    plt.xticks(rotation=90, fontsize=8)
    fig.tight_layout()

def Worker():
    global path
    global OutputCSV
    global Verbose
    global wantpng
    global outputPNG

    files = get_files(path,Verbose)
    dates = get_total_size_by_date(files)

    if wantpng:
        create_graph(dates)
        plt.savefig(outputPNG)
    
    with open(OutputCSV, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Size'])
        total = 0
        for date in dates:
            total += date[1]
            writer.writerow([date[0], total])

if __name__ == "__main__":
    clear_screen()
    if path is None:
        prompt_path()

    if Verbose is None:
        Verbose = prompt_verbose()
    
    if sizeformat is None:
        sizeformat = prompt_sizeformat()
    
    if OutputCSV is None:
        OutputCSV = prompt_save_path() 

    if wantpng is None:
        wantpng = want_png()
    elif wantpng:
        if outputPNG is None:
            prompt_png_path()
    clear_screen()
    Worker()    


    
    
    


