"""
This script will sync your Sonarr library with Overseer. This can help resolve issues where requests have failed to send to Sonarr
"""

import requests,os,dotenv

overseerr_url = None
overseerr_apikey = None

sonarr_url = None
sonarr_apikey = None
sonnarr_quality_profile_id = None
sonarr_root_folder_path = None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_environment_variables():
    global overseerr_url, overseerr_apikey, sonarr_url, sonarr_apikey, sonnarr_quality_profile_id, sonarr_root_folder_path

    dotenv.load_dotenv()

    overseerr_url = os.getenv("OVERSEERR_URL")
    overseerr_apikey = os.getenv("OVERSEERR_API_KEY")

    sonarr_url = os.getenv("SONARR_URL")
    sonarr_apikey = os.getenv("SONARR_API_KEY")

    sonnarr_quality_profile_id = os.getenv("SONARR_QUALITY_PROFILE_ID")
    sonarr_root_folder_path = os.getenv("SONARR_ROOT_FOLDER_PATH")

def get_overseer_requests(filter=None):
    global overseerr_url, overseerr_apikey
    if filter is None:
        filter = "all"
    url = f"{overseerr_url}/api/v1/request?take=99999999&skip=0&sort=added&filter={filter}"
    headers = {
        "accept": "application/json",
        "X-Api-Key": overseerr_apikey
    }

    response = requests.get(url, headers=headers)
    return response.json()

def get_series_title(tvdbId):
    url = f"https://api.thetvdb.com/series/{tvdbId}"
    headers = {
        "accept": "application/json",
    }

    response = requests.get(url, headers=headers)
    series_data = response.json()
    try:
        result = series_data['data']['seriesName']
        return result
    except:
        return 0

def sanitize_string_for_url(string):
    try:
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
    except:
        return string
    

def parse_overseer_requests(overseer_data):
    ids = []
    overseer_data = overseer_data['results']
    for show in overseer_data:
        if show['type'] == "tv":
            try:
                string = (show['media']['externalServiceSlug'])
                string = string + " | " + str((show['media']['tvdbId']))
                print(string)
                ids.append(((show['media']['tvdbId']), (show['media']['externalServiceSlug']),(show['profileId']),(show['rootFolder'])))
            except:
                if(show['media']['externalServiceSlug'] == None):
                    title = get_series_title(show['media']['tvdbId'])
                    if title == None:
                        print("Failed to get title for: " + str(show['media']['tvdbId']))
                    else:
                        ids.append(((show['media']['tvdbId']), (title),(show['profileId']),(show['rootFolder'])))

            
    return ids

def request_series(series):
    global sonarr_url, sonarr_apikey

    url = f"{sonarr_url}api/v3/series"
    headers = {
        "accept": "application/json",
        "X-Api-Key": sonarr_apikey
    }

    for show in series:
        if((show[1] == None) or (show[1] == show[0])):
            title = get_series_title(show[0])
            data = {
                "tvdbId": show[0],
                "title": sanitize_string_for_url(title),
                "qualityProfileId": show[2],
                "rootFolderPath": "/media/plex/series/General/",
            }
        else:
            data = {
                "tvdbId": show[0],
                "title": sanitize_string_for_url(show[1]),
                "qualityProfileId": 7,
                "rootFolderPath": "/media/plex/series/General/",
            }
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 201:
            print(f"Successfully added {data['title']} to Sonarr")
        else:
            if "This series has already been added" in response.text:
                pass
                #print(f"Series already added: {data['title']}")
            else:
                try:
                    print(f"Error adding series: {response.text}")
                except:
                    pass




if __name__ == '__main__':
    clear_screen()
    load_environment_variables()
    overseer_data = get_overseer_requests("all") #all, approved, pending, available, processing, failed
    ids = parse_overseer_requests(overseer_data)
    request_series(ids)