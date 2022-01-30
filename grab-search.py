import requests
import mimetypes
import sys
from pathlib import Path
from datetime import datetime
import time
import socket

from util import *
from headers import *

# SYNPOSIS:
# To download 100 (or fewer, if there aren't enough) artworks of the search term "game of thrones", call
# python3 grab-search.py "game of thrones" 100
# If max-projects isn't specified, it will fetch them all (beware! i really mean ALL! At this time, this would be over 12000 projects for our game of thrones example).

# 2 minute timeout in case something gets stuck.
socket.setdefaulttimeout(120)

search_terms = str.lower(sys.argv[1])
search_terms_filename = "search_" + slugify(search_terms)

max_projects = sys.maxsize
# Is max-posts specified?
if len(sys.argv) >= 3:
    max_projects = int(sys.argv[2])

# Create artist directory if it doesn't exist
artist_directory = "./downloads/" + search_terms_filename + "/"
Path(artist_directory).mkdir(parents=True, exist_ok=True)

# Create directory for already saved posts, and generate filename
Path("./already_saved/").mkdir(parents=True, exist_ok=True)

# Create directory for logging, and generate filename
Path("./logs/").mkdir(parents=True, exist_ok=True)

if max_projects == sys.maxsize:
    logMsg(f"Fetching search results for '{search_terms}'... Max projects to fetch: ALL OF THEM!", "okndl", search_terms_filename)
else:
    logMsg(f"Fetching search results for '{search_terms}'... Max projects to fetch: {max_projects}", "okndl", search_terms_filename)

# Request project info for artist
lastPageReached = False
pageCounter = 1
projectCounter = 0
try:
    while not lastPageReached:
        logMsg(f"Fetching search result page #{pageCounter} for '{search_terms}'...", "okndl", search_terms_filename)
        projects_data = requests.get(f"https://www.artstation.com/api/v2/search/projects.json?page={pageCounter}&per_page=50&sorting=relevance&query={search_terms.replace(' ', '+')}", headers=project_fetch_headers)
        projects = projects_data.json()["data"]
        result_size = projects_data.json()["total_count"]
        page_num_projects = len(projects)



        lastPageReached = page_num_projects < 50 # Each full page contains 50 projects. If it has less than 50, it is the last page

        if not lastPageReached:
            pageCounter = pageCounter + 1
            logMsg(f"Found {result_size} projects total (all pages). Of this {page_num_projects} on this page...", "okndl", search_terms_filename)
        else:
            logMsg(f"Found {result_size} projects total (all pages). Of this {page_num_projects} on this page... This is the last page!", "okndl", search_terms_filename)


        # For each project in all of the artists projects
        for project in projects:
            if projectCounter >= max_projects:
                logMsg(f"Reached project download limit of {max_projects}. Stopping...", "okndl", search_terms_filename)
                exit(0)

            project_name        = project["title"]
            project_hash_id     = project["hash_id"]
            project_artist_name = project["user"]["username"]
            project_artist_name_fullname = project["user"]["full_name"]

            logMsg(f"Found project '{project_name}' of artist '{project_artist_name_fullname}' (user-id=[{project_artist_name}]) with project id {project_hash_id}. Fetching more info about it...", "okndl", search_terms_filename)

            # Have we already downloaded this post?
            if not isPostAlreadySaved(project_hash_id, search_terms_filename):

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
                        filename = artist_directory + slugify(project_artist_name) + "_" + slugify(project_name[:60] + "_" + project_hash_id + "_" + str(asset_position)) + "." + extensionFromUrl(asset_image_url)

                        logMsg(f"Found image-asset for project '{project_name}' [{project_hash_id}] of artist '{project_artist_name_fullname}' (user-id=[{project_artist_name}]) at position {asset_position}. Downloading to '{filename}'...", "okdl", search_terms_filename)

                        # Download it
                        downloadMedia(asset_image_url, filename)
                    else:
                        logMsg(f"Found non-image-asset for project '{project_name}' [{project_hash_id}] of artist '{project_artist_name_fullname}' (user-id=[{project_artist_name}]) at position {asset_position}. Skipping...", "okdl", search_terms_filename)

                # After downloading all assets, mark the project as downloaded.
                markPostAsSaved(project_hash_id, search_terms_filename)
                projectCounter = projectCounter + 1

            # Project is already downloaded
            else:
                logMsg(f"Skipping project '{project_name}' [{project_hash_id}] of artist '{project_artist_name_fullname}' (user-id=[{project_artist_name}]) because it is already downloaded.", "okndl", search_terms_filename)

    logMsg(f"Finished all search result pages of '{search_terms}'... Total pages scanned: {pageCounter}", "okndl", search_terms_filename)

except socket.timeout as exc:
    logMsg("Socket timeout of two minutes reached! We'll get 'em next time, boys!", "err", search_terms_filename)
except SystemExit:
    # That's... why i'm here
    exit(0)
except BaseException as exc:
    logMsg("Failed for some reason!: " + repr(exc), "err", search_terms_filename)
