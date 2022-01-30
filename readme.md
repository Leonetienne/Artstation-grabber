# Quick-and-dirty artstation sync
This is a personal and untested tool to keep (and update) local copies of artstation profiles via cli.
Project id's are saved in order to not re-download everything. This ensures that only new media will be downloaded in each cronjob instance.
No fancy bs going on. Just a simple script bodged together within 10 minutes at 3 AM.

Currently only working for images. Feel free to issue a pull request if you want more.

## Setup
Install required pip modules.
```bash
pip3 install request pyyaml
```
All scripts require Python3. Tested using 3.9.9.

## Running it
Here we have two scripts:
```bash
grab.py $artist-name
```
This will grab one individual profile, if it is not already downloaded.

```bash
grab-all.py
```
This will call `grab.py` on all artists listed in `artists.yaml`.

Files will be saved to `./downloads/{artist_name}/*.{ext}`.
Logs will be saved to `./logs/{artist_name}.txt`.
Download indices (to skip already downloaded projects) are kept in `./already_saved/{artist_name}.txt`.
