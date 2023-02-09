import os, requests, dotenv, datetime, csv

"""
This script will export the streaming services for all series in Sonarr. This is done through the TVDB API
This can be configured through a .env file or manually through the script.
"""

#Manual Config#
save = None
output = None

#Variables#
thetvdb = "https://api.thetvdb.com/series/"


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

def validate_connection():
    try:
        response = requests.get(f"{os.getenv('SONARR_URL')}/api/v3/series?apikey={os.getenv('SONARR_API_KEY')}")
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

def prompt_save():
    global save
    clear_screen()
    save = get_bool(input('Save output? (yes/No): '))
    if save != True and save != False:
        clear_screen()
        input('Invalid save response. Press Enter to continue.')
        prompt_save()
    else:
        if save:
            return True
        else:
            return False

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

def get_streaming_services(tvdbId):
    try:
        url = thetvdb + "filter?keys=network&tvdbId=" + tvdbId
        response = requests.get(thetvdb + tvdbId +"/filter?keys=network")
        if response.status_code == 200:
            data = response.json()
            service = (data['data']['network'])
            return service
        else:
            return "Error"
    except Exception as e:
        return f"Error | {e}"

def save_worker():
    clear_screen()
    try:
        response = requests.get(f"{os.getenv('SONARR_URL')}/api/v3/series?apikey={os.getenv('SONARR_API_KEY')}")
        if response.status_code == 200:
            data = response.json()
            with open(output, 'w', newline='') as csvfile:
                stream_writer = csv.writer(csvfile)
                stream_writer.writerow(["tvdbId","Name","Service(s)"])
                print(["tvdbId","Name","Service(s)"])
                for series in data:
                    try:
                        service = get_streaming_services(str(series['tvdbId']))
                        print([series['tvdbId'], series['title'], service])
                        stream_writer.writerow([series['tvdbId'], series['title'], service])
                        csvfile.flush()
                    except Exception as e:
                        print(f"{series['title']} | {e}")
    
    except Exception as e:
        print(e)

def verbose_worker():
    clear_screen()
    try:
        response = requests.get(f"{os.getenv('SONARR_URL')}/api/v3/series?apikey={os.getenv('SONARR_API_KEY')}")
        if response.status_code == 200:
            data = response.json()
            print(["tvdbId","Name","Service(s)"])
            for series in data:
                try:
                    service = get_streaming_services(str(series['tvdbId']))
                    print([series['tvdbId'], series['title'], service])
                except Exception as e:
                    print(f"{series['title']} | {e}")
    
    except Exception as e:
        print(e)

def prompt_save_path():
    global output
    clear_screen()
    save_path = input('Enter save path: ')
    validpath = is_valid_path(save_path)
    if not validpath:
        input('Invalid save path. Press Enter to continue.')
        prompt_save_path()
    else:
        if output is None:
            output = save_path
        date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"SonarrServiceExport-{date_time}.csv"
        return os.path.join(output, file_name)
    
if __name__ == '__main__':
    dotenv.load_dotenv()
    clear_screen()
    if validate_connection():
        print('Connection to Sonarr successful.')
        clear_screen()
        if save is None:
            prompt_save()

        if save:
            if output is None:
                output = prompt_save_path()
            else:
                print(f"Save path set to: {output}")
            
            save_worker()
            
        else:
            print('Output will not be saved.')
            verbose_worker()


    else:
        print('Connection to Sonarr failed.')
        exit()


