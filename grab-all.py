import yaml
import os

with open("artists.yaml", "r") as yamlfile:
    try:
        config = yaml.safe_load(yamlfile)

        for artist in config:
            print(f"\033[92mGrabbing artist '{artist}'")
            os.system(f"python3 grab.py '{artist}'")

    except yaml.YAMLError as exc:
        print("You fucked up the yaml format.")
