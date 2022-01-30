import yaml
import os

with open("to-grab.yaml", "r") as yamlfile:
    try:
        config = yaml.safe_load(yamlfile)

        # Grab artists
        if "artists" in config:
            for artist in config["artists"]:
                print(f"\033[92mGrabbing artist '{artist}'")
                os.system(f"python3 grab-artist.py '{artist}'")
        
        # Grab search results
        if "searches" in config:
            for search in config["searches"]:
                print(f"\033[92mGrabbing search results for '{search['terms']}'")

                max_results = ""
                if "max" in search:
                    max_results = search["max"]

                os.system("python3 grab-search.py '" + search['terms'] + "' " + str(max_results))

    except yaml.YAMLError as exc:
        print("You fucked up the yaml format.")
