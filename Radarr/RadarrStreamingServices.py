import os, requests, dotenv, datetime, csv, json, urllib

"""
This script will export the streaming services for all series in Radarr. This is done through the TVDB API
This can be configured through a .env file or manually through the script.
"""

#Manual Config#
save = None
output = None
locale="GB"

#Variables#
letterboxd = "https://letterboxd.com/film/"

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
        response = requests.get(f"{os.getenv('RADARR_URL')}/api/v3/movie?apikey={os.getenv('RADARR_API_KEY')}")
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

def sanitize_string_for_url(string):
    string = string.replace(" & ", "-")
    string = string.replace(" ", "-")
    string = string.replace(":", "")
    string = string.replace("'", "")
    string = string.replace("!", "")
    string = string.replace("?", "")
    string = string.replace(".", "")
    string = string.replace(",", "")
    string = string.replace(";", "")
    return string.lower()
    

def save_worker():
    clear_screen()
    try:
        response = requests.get(f"{os.getenv('RADARR_URL')}/api/v3/movie?apikey={os.getenv('RADARR_API_KEY')}")
        if response.status_code == 200:
            data = response.json()
            with open(output, 'w', newline='') as csvfile:
                stream_writer = csv.writer(csvfile)
                stream_writer.writerow(["imdbId","Title","Service(s)"])
                print(["imdbId","Title","Service(s)"])
                for movie in data:
                    try:
                        services = get_data(str(sanitize_string_for_url(movie['title'])))
                        print([movie['imdbId'], movie['title'], services])
                        stream_writer.writerow([movie['imdbId'], movie['title'], services])
                        csvfile.flush()
                    except Exception as e:
                        print(f"{movie['title']} | {e}")
    
    except Exception as e:
        print(e)

def verbose_worker():
    clear_screen()
    try:
        response = requests.get(f"{os.getenv('RADARR_URL')}/api/v3/movie?apikey={os.getenv('RADARR_API_KEY')}")
        if response.status_code == 200:
            data = response.json()
            print(["imdbId","Name","Service(s)"])
            for movie in data:
                try:
                    services = get_data(str(sanitize_string_for_url(movie['title'])))
                    print([movie['imdbId'], movie['title'], services])
                except Exception as e:
                    print(f"{movie['title']} | {e}")
    
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
        file_name = f"RadarrServiceExport-{date_time}.csv"
        return os.path.join(output, file_name)  

def get_letterboxd_id(name):
    url = f"{letterboxd}{name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.text
        #Get the var filmData from data
        filmData = data[data.find("var filmData = ")+15:data.find("var filmData = ")+15+data[data.find("var filmData = ")+15:].find("};")+1]
        #get the id from filmData

        #Remove ' from the string
        filmData = filmData.replace("/",'')
        data = filmData.split(",")
        for i in data:
            if "id" in i:
                return i.split(":")[1]
    return None

def get_streaming_services(id):
    global locale
    services = []
    url = f"https://letterboxd.com/s/film-availability?filmId={id}&locale={locale}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        best = data["best"]
        stream = best["stream"]
        for service in stream:
            services.append(service["name"])
        return services
    return services

def get_data(name):
    return get_streaming_services(get_letterboxd_id(name))

if __name__ == '__main__':
    dotenv.load_dotenv()
    clear_screen()
    if validate_connection():
        print('Connection to Radarr successful.')
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
        print('Connection to Radarr failed.')
        exit()
