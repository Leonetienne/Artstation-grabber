#!/bin/python3
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
# To download posts from an artist:
# python3 grab-artist.py mixppl

# 2 minute timeout in case something gets stuck.
socket.setdefaulttimeout(120)

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
try:
    while not lastPageReached:
        logMsg(f"Fetching page {pageCounter} of {artist_name}...", "okndl", artist_name)
        projects_data = requests.get(f"https://www.artstation.com/users/{artist_name}/projects.json?page={pageCounter}", headers=project_fetch_headers)
        projects = projects_data.json()["data"]

        page_num_projects = len(projects)

        lastPageReached = page_num_projects < 50 # Each full page contains 50 projects. If it has less than 50, it is the last page

        if not lastPageReached:
            pageCounter = pageCounter + 1
            logMsg(f"Page contains {page_num_projects} projects...", "okndl", artist_name)
        else:
            logMsg(f"Page contains {page_num_projects} projects... That's the last page!", "okndl", artist_name)


        # For each project in all of the artists projects
        for project in projects:
            project_name    = project["title"]
            project_hash_id = project["hash_id"]

            logMsg(f"Found project '{project_name}' with id {project_hash_id}. Fetching more info about it...", "okndl", artist_name)

            # Have we already downloaded this post?
            if not isPostAlreadySaved(project_hash_id, artist_name):

                # Fetch information about the project
                project_info = requests.get(f"https://www.artstation.com/projects/{project_hash_id}.json", headers=project_fetch_headers)
                assets = project_info.json()["assets"]

                # For each asset in the project (might be multiple images)
                for asset in assets:
                    asset_type = asset["asset_type"]
                    asset_position = asset["position"]

                    # If the asset is an image
                    if asset_type == "image":
                        asset_image_url = asset["image_url"]
                        
                        # Generate a download filename
                        filename = artist_directory + slugify(project_name[:60] + "_" + project_hash_id + "_" + str(asset_position)) + "." + extensionFromUrl(asset_image_url)

                        logMsg(f"Found image-asset for project '{project_name}' [{project_hash_id}] at position {asset_position}. Downloading to '{filename}'...", "okdl", artist_name)

                        # Download it
                        downloadMedia(asset_image_url, filename)
                    else:
                        logMsg(f"Found non-image-asset for project '{project_name}' [{project_hash_id}] at position {asset_position}. Skipping...", "okdl", artist_name)

                # After downloading all assets, mark the project as downloaded.
                markPostAsSaved(project_hash_id, artist_name)

            # Project is already downloaded
            else:
                logMsg(f"Skipping project '{project_name}' [{project_hash_id}] because it is already downloaded.", "okndl", artist_name)

    logMsg(f"Finished all pages of {artist_name}... Total pages of this artist scanned: {pageCounter}", "okndl", artist_name)

except socket.timeout as exc:
    logMsg("Socket timeout of two minutes reached! We'll get 'em next time, boys!", "err", artist_name)
except BaseException as exc:
    logMsg("Failed for some reason!: " + repr(exc), "err", artist_name)
