"""
This script will sync your Radarr library with Overseer. This can help resolve issues where requests have failed to send to Sonarr
"""

import requests,os,dotenv

overseerr_url = None
overseerr_apikey = None

radarr_url = None
radarr_apikey = None
sonnarr_quality_profile_id = None
radarr_root_folder_path = None
tmdb_apikey = None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def load_environment_variables():
    global overseerr_url, overseerr_apikey, radarr_url, radarr_apikey, sonnarr_quality_profile_id, radarr_root_folder_path, tmdb_apikey

    dotenv.load_dotenv()

    overseerr_url = os.getenv("OVERSEERR_URL")
    overseerr_apikey = os.getenv("OVERSEERR_API_KEY")

    radarr_url = os.getenv("RADARR_URL")
    radarr_apikey = os.getenv("RADARR_API_KEY")

    sonnarr_quality_profile_id = os.getenv("RADARR_QUALITY_PROFILE_ID")
    radarr_root_folder_path = os.getenv("RADARR_ROOT_FOLDER_PATH")

    tmdb_apikey = os.getenv("TMDB_API_KEY")

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

def get_movie_title(tmdbId):
    global tmdb_apikey
    url = f"https://api.themoviedb.org/3/movie/{tmdbId}?api_key={tmdb_apikey}"
    headers = {
        "accept": "application/json",
    }

    response = requests.get(url, headers=headers)
    movie_data = response.json()
    try:
        result = movie_data['title']
        return result
    except:
        return 0

def parse_overseer_requests(overseer_data):
    ids = []
    overseer_data = overseer_data['results']
    for show in overseer_data:
        if show['type'] == "movie":
            try:
                string = (show['media']['externalServiceSlug'])
                string = string + " | " + str((show['media']['tmdbId']))
                print(string)
                ids.append(((show['media']['tvdbId']), (show['media']['externalServiceSlug'])))
            except:
                if(show['media']['externalServiceSlug'] == None):
                    title = get_series_title(show['media']['tvdbId'])
                    if title == None:
                        print("Failed to get title for: " + str(show['media']['tvdbId']))
                    else:
                        ids.append(((show['media']['tvdbId']), (title)))

            
    return ids

if __name__ == '__main__':
    clear_screen()
    load_environment_variables()
    overseer_data = get_overseer_requests("all") #all, approved, pending, available, processing, failed
    ids = parse_overseer_requests(overseer_data)