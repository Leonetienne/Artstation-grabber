import requests
import mimetypes
import os
import sys
import urllib.request
import unicodedata
import re
from pathlib import Path
from datetime import datetime
import time

# SYNPOSIS:
# To download posts from an artist:
# python3 grab.py mixppl

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def logMsg(msg, mode):

    col = 0
    prefix = 0

    if mode == "okdl":
        col = bcolors.OKCYAN
        prefix = "[OK_DL   ]"

    elif mode == "okndl":
        col = bcolors.OKBLUE
        prefix = "[OK_NO_DL]"

    elif mode == "warn":
        col = bcolors.WARNING
        prefix = "[WARNING ]"

    elif mode == "err":
        col = bcolors.FAIL
        prefix = "[ERROR   ]"
    else:
        print(bcolors.FAIL + "SUPPLIED INVALID LOG MODE!!! USE EITHER okdl, okndl, warn, or err!")

    timestamp = getCurrentTimestamp()

    # Log to console
    print(col + f"[{timestamp}][{artist_name}]: " + msg)

    # Log to logfile
    logfile = open("./logs/" + slugify(artist_name) + ".txt", "a") # Open existing or create
    logfile.write(prefix + " " + "[" + timestamp + "]: " + msg + "\n")
    logfile.close()


def extensionFromUrl(url):
    rurl = url[::-1]
    rext = ""
    for c in rurl:
        if c != '.':
            rext = rext + c
        else:
            break

    ext = rext[::-1]

    # Now remove the get parameters
    foundQuestionmark = False
    actualExt = ""
    for c in ext:
        if c == '?':
            foundQuestionmark = True

        if not foundQuestionmark:
            actualExt = actualExt + c

    return actualExt


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def getCurrentTimestamp():
    return datetime.utcfromtimestamp(time.time()).strftime("%m-%d-%Y %H-%M")

def isPostAlreadySaved(post_id):
    idset_filename = "./already_saved/" + slugify(artist_name) + ".txt"

    # Does the index file even exist yet?
    if not os.path.exists(idset_filename):
        return False

    # Open the index file
    index_file = open(idset_filename, "r") # Open existing or create

    # Store lines in array
    already_downloaded_post_ids = index_file.readlines()

    return (post_id + "\n") in already_downloaded_post_ids

def markPostAsSaved(post_id):
    idset_filename = "./already_saved/" + slugify(artist_name) + ".txt"

    # Open the index file
    index_file = open(idset_filename, "a") # Open existing or create
    index_file.write(post_id + "\n")
    index_file.close()


def downloadMedia(url, filename):
    # Prepare and execute query to download images
    opener = urllib.request.build_opener()
    opener.addheaders = image_request_headers
    urllib.request.install_opener(opener)
    source = urllib.request.urlretrieve(asset_image_url, filename)


project_fetch_headers = {
    'authority': 'www.artstation.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'de-DE,de;q=0.9',
    'authority': 'api.reddit.com'
}

image_request_headers = [
    ('authority', 'cdna.artstation.com'),
    ('pragma', 'no-cache'),
    ('cache-control', 'no-cache'),
    ('sec-ch-ua', '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"'),
    ('sec-ch-ua-mobile', '?0'),
    ('sec-ch-ua-platform', '"Windows"'),
    ('upgrade-insecure-requests', '1'),
    ('user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'),
    ('accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'),
    ('sec-fetch-site', 'none'),
    ('sec-fetch-mode', 'navigate'),
    ('sec-fetch-user', '?1'),
    ('sec-fetch-dest', 'document'),
    ('accept-language', 'de-DE,de;q=0.9')
]


artist_name = str.lower(sys.argv[1])

# Create artist directory if it doesn't exist
artist_directory = "./downloads/" + slugify(artist_name) + "/"
Path(artist_directory).mkdir(parents=True, exist_ok=True)

# Create directory for already saved posts, and generate filename
Path("./already_saved/").mkdir(parents=True, exist_ok=True)

# Create directory for logging, and generate filename
Path("./logs/").mkdir(parents=True, exist_ok=True)


# Request project info for artist
lastPageReached = False
pageCounter = 1
while not lastPageReached:
    logMsg(f"Fetching page {pageCounter} of {artist_name}...", "okndl")
    projects_data = requests.get(f"https://www.artstation.com/users/{artist_name}/projects.json?page={pageCounter}", headers=project_fetch_headers)
    projects = projects_data.json()["data"]

    page_num_projects = len(projects)

    lastPageReached = page_num_projects < 50 # Each full page contains 50 projects. If it has less than 50, it is the last page

    if not lastPageReached:
        pageCounter = pageCounter + 1
        logMsg(f"Page contains {page_num_projects} projects...", "okndl")
    else:
        logMsg(f"Page contains {page_num_projects} projects... That's the last page!", "okndl")


    # For each project in all of the artists projects
    for project in projects:
        project_name    = project["title"]
        project_hash_id = project["hash_id"]

        logMsg(f"Found project {project_name} with id {project_hash_id}. Fetching more info about it...", "okndl")

        # Have we already downloaded this post?
        if not isPostAlreadySaved(project_hash_id):

            # Fetch information about the project
            project_info = requests.get(f"https://www.artstation.com/projects/{project_hash_id}.json", headers=project_fetch_headers)
            assets = project_info.json()["assets"]

            # For each asset in the project (might be multiple images)
            for asset in assets:
                asset_type = asset["asset_type"]

                # If the asset is an image
                if asset_type == "image":
                    asset_image_url = asset["image_url"]
                    asset_position = asset["position"]
                    
                    # Generate a download filename
                    filename = artist_directory + slugify(project_name[:60] + "_" + project_hash_id + "_" + str(asset_position)) + "." + extensionFromUrl(asset_image_url)

                    logMsg(f"Found image-asset for project {project_name} [{project_hash_id}] at position {asset_position}. Downloading to '{filename}'...", "okdl")

                    # Download it
                    downloadMedia(asset_image_url, filename)
                else:
                    logMsg(f"Found non-image-asset for project {project_name} [{project_hash_id}] at position {asset_position}. Skipping...", "okdl")

            # After downloading all assets, mark the project as downloaded.
            markPostAsSaved(project_hash_id)

        # Project is already downloaded
        else:
            logMsg(f"Skipping project {project_name} [{project_hash_id}] because it is already downloaded.", "okndl")

logMsg(f"Finished all pages of {artist_name}... Total pages of this artist scanned: {pageCounter}", "okndl")
